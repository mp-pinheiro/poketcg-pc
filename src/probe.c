/* poketcg_probe: one JSON request on stdin, one JSON response on stdout.
 *
 *   in : {"fn":"UpdateRNGSources","a":170,"f":240,"b":187,"c":204,"d":221,"e":238,
 *         "hl":4660,"wram":{"51914":"12","51915":"34","51916":"56"}}
 *   out: {"a":196,"f":0,"b":187,"c":204,"d":221,"e":238,"hl":4660,
 *         "wram":{"51914":"88","51915":"4c","51916":"57"}}
 *
 * "wram" keys are decimal Game Boy addresses and values are lowercase hex byte
 * strings of any even length; writes and read-back go through the whole bus, so
 * HRAM (hBankROM = 65408) and SRAM work through the same field. An optional
 * "read" object maps decimal addresses to byte counts read back after the call
 * without seeding them first. The response echoes every requested span, in
 * request order, under "wram".
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "mem.h"
#include "probe.h"

#define MAX_SPANS 64
#define MAX_SPAN_BYTES 8192
#define MAX_NAME 96

struct span {
	uint16_t addr;
	uint16_t len;
};

static const char *js;

static void die(const char *msg)
{
	printf("{\"error\":\"%s\"}\n", msg);
	exit(1);
}

static void ws(void)
{
	while (*js == ' ' || *js == '\t' || *js == '\n' || *js == '\r')
		js++;
}

static int eat(char c)
{
	ws();
	if (*js == c) {
		js++;
		return 1;
	}
	return 0;
}

static void need(char c)
{
	if (!eat(c))
		die("malformed json");
}

/* Copies a JSON string literal into out (NUL-terminated). No escape handling:
 * every key and value in this protocol is hex, decimal or a pret symbol name. */
static size_t jstr(char *out, size_t cap)
{
	need('"');
	size_t n = 0;
	while (*js && *js != '"') {
		if (n + 1 >= cap)
			die("string too long");
		out[n++] = *js++;
	}
	need('"');
	out[n] = '\0';
	return n;
}

static long jnum(void)
{
	ws();
	char *end;
	long v = strtol(js, &end, 10);
	if (end == js)
		die("expected number");
	js = end;
	return v;
}

static int hexdig(char c)
{
	if (c >= '0' && c <= '9')
		return c - '0';
	if (c >= 'a' && c <= 'f')
		return c - 'a' + 10;
	if (c >= 'A' && c <= 'F')
		return c - 'A' + 10;
	return -1;
}

/* Skips one value of any type without interpreting it. */
static void jskip(void)
{
	ws();
	if (*js == '"') {
		char scratch[MAX_SPAN_BYTES];
		jstr(scratch, sizeof scratch);
	} else if (*js == '{' || *js == '[') {
		char open = *js++, close = open == '{' ? '}' : ']';
		int depth = 1;
		while (*js && depth) {
			if (*js == '"') {
				char scratch[MAX_SPAN_BYTES];
				jstr(scratch, sizeof scratch);
				continue;
			}
			if (*js == open)
				depth++;
			else if (*js == close)
				depth--;
			js++;
		}
	} else {
		while (*js && *js != ',' && *js != '}' && *js != ']')
			js++;
	}
}

static char *read_stdin(void)
{
	size_t cap = 1 << 16, len = 0;
	char *buf = malloc(cap);
	if (!buf)
		die("out of memory");
	for (;;) {
		if (len + 1 >= cap) {
			cap *= 2;
			char *grown = realloc(buf, cap);
			if (!grown)
				die("out of memory");
			buf = grown;
		}
		size_t n = fread(buf + len, 1, cap - len - 1, stdin);
		len += n;
		if (n == 0)
			break;
	}
	buf[len] = '\0';
	return buf;
}

int main(void)
{
	char *input = read_stdin();
	js = input;

	char fn[MAX_NAME] = { 0 };
	struct span spans[MAX_SPANS];
	size_t nspans = 0;
	ProbeState st = { 0 };

	mem_reset();

	const char *rom = getenv("POKETCG_ROM");
	if (rom && *rom && rom_load(rom) != 0)
		die("cannot read $POKETCG_ROM");

	need('{');
	if (!eat('}')) {
		do {
			char key[MAX_NAME];
			jstr(key, sizeof key);
			need(':');
			if (strcmp(key, "fn") == 0) {
				jstr(fn, sizeof fn);
			} else if (strcmp(key, "a") == 0) {
				st.a = (uint8_t)jnum();
			} else if (strcmp(key, "f") == 0) {
				st.f = (uint8_t)jnum() & 0xF0; /* the low nibble of F is always 0 */
			} else if (strcmp(key, "b") == 0) {
				st.b = (uint8_t)jnum();
			} else if (strcmp(key, "c") == 0) {
				st.c = (uint8_t)jnum();
			} else if (strcmp(key, "d") == 0) {
				st.d = (uint8_t)jnum();
			} else if (strcmp(key, "e") == 0) {
				st.e = (uint8_t)jnum();
			} else if (strcmp(key, "hl") == 0) {
				st.hl = (uint16_t)jnum();
			} else if (strcmp(key, "wram") == 0) {
				need('{');
				if (!eat('}')) {
					do {
						char addr_s[MAX_NAME], hex[MAX_SPAN_BYTES];
						jstr(addr_s, sizeof addr_s);
						need(':');
						size_t hn = jstr(hex, sizeof hex);
						if (hn % 2)
							die("wram value needs an even hex digit count");
						if (nspans == MAX_SPANS)
							die("too many wram spans");
						uint16_t at = (uint16_t)strtoul(addr_s, NULL, 10);
						for (size_t i = 0; i < hn; i += 2) {
							int hi = hexdig(hex[i]), lo = hexdig(hex[i + 1]);
							if (hi < 0 || lo < 0)
								die("wram value is not hex");
							gb_write8((uint16_t)(at + i / 2),
								  (uint8_t)(hi << 4 | lo));
						}
						spans[nspans].addr = at;
						spans[nspans].len = (uint16_t)(hn / 2);
						nspans++;
					} while (eat(','));
					need('}');
				}
			} else if (strcmp(key, "read") == 0) {
				need('{');
				if (!eat('}')) {
					do {
						char addr_s[MAX_NAME];
						jstr(addr_s, sizeof addr_s);
						need(':');
						long n = jnum();
						if (n < 0 || n > MAX_SPAN_BYTES / 2)
							die("read length out of range");
						if (nspans == MAX_SPANS)
							die("too many wram spans");
						spans[nspans].addr =
							(uint16_t)strtoul(addr_s, NULL, 10);
						spans[nspans].len = (uint16_t)n;
						nspans++;
					} while (eat(','));
					need('}');
				}
			} else if (strcmp(key, "sram") == 0) {
				need('{');
				if (!eat('}')) {
					do {
						char bank_s[MAX_NAME];
						jstr(bank_s, sizeof bank_s);
						need(':');
						unsigned bank = (unsigned)strtoul(bank_s, NULL, 10);
						if (bank > 3)
							die("sram bank out of range");
						g_sram_bank = (uint8_t)bank;
						g_sram_enabled = 1;
						need('{');
						if (!eat('}')) {
							do {
								char addr_s[MAX_NAME], hex[MAX_SPAN_BYTES];
								jstr(addr_s, sizeof addr_s);
								need(':');
								size_t hn = jstr(hex, sizeof hex);
								if (hn % 2)
									die("sram value needs an even hex digit count");
								uint16_t at = (uint16_t)strtoul(addr_s, NULL, 10);
								if (at < 0xA000 || (size_t)at + hn / 2 > 0xC000)
									die("sram span outside $A000-$BFFF");
								for (size_t i = 0; i < hn; i += 2) {
									int hi = hexdig(hex[i]), lo = hexdig(hex[i + 1]);
									if (hi < 0 || lo < 0)
										die("sram value is not hex");
									g_sram[(size_t)bank * 0x2000 + (at - 0xA000) + i / 2] =
										(uint8_t)(hi << 4 | lo);
								}
							} while (eat(','));
							need('}');
						}
					} while (eat(','));
					need('}');
				}
			} else {
				jskip();
			}
		} while (eat(','));
		need('}');
	}

	if (!fn[0])
		die("missing \"fn\"");
	ProbeFn call = probe_lookup(fn);
	if (!call) {
		printf("{\"error\":\"unknown routine: %s\"}\n", fn);
		return 1;
	}

	call(&st);

	printf("{\"a\":%u,\"f\":%u,\"b\":%u,\"c\":%u,\"d\":%u,\"e\":%u,\"hl\":%u,\"wram\":{",
	       st.a, st.f, st.b, st.c, st.d, st.e, st.hl);
	for (size_t i = 0; i < nspans; i++) {
		printf("%s\"%u\":\"", i ? "," : "", spans[i].addr);
		for (uint16_t k = 0; k < spans[i].len; k++)
			printf("%02x", *gb_ptr((uint16_t)(spans[i].addr + k)));
		printf("\"");
	}
	printf("}}\n");

	free(input);
	rom_free();
	return 0;
}
