/* poketcg_probe: one JSON request on stdin, one JSON response on stdout.
 *
 *   in : {"fn":"UpdateRNGSources","a":170,"f":240,"b":187,"c":204,"d":221,"e":238,
 *         "hl":4660,"wram":{"51914":"12","51915":"34","51916":"56"}}
 *   out: {"a":196,"f":0,"b":187,"c":204,"d":221,"e":238,"hl":4660,
 *         "wram":{"51914":"88","51915":"4c","51916":"57"},"sram":{}}
 *
 * "wram" keys are decimal Game Boy addresses and values are lowercase hex byte
 * strings of any even length; writes and read-back go through the whole bus, so
 * HRAM (hBankROM = 65408) and SRAM work through the same field. An optional
 * "read" object maps decimal addresses to byte counts read back after the call
 * without seeding them first. "sram" seeds a bank explicitly:
 * {"sram":{"<bank 0-3>":{"<decimal addr>":"<hex>"}}}, writing g_sram directly so
 * the seed does not depend on g_sram_bank/g_sram_enabled at request time. An
 * optional "sread" object, {"sread":{"<bank>":{"<decimal addr>":<count>}}}, reads
 * banked SRAM back after the call the same way, independent of the bank/enable
 * latch at return. The response echoes every requested span, in request order,
 * under "wram"; sread spans come back grouped by bank under "sram", after "wram".
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "mem.h"
#include "probe.h"

#define MAX_SPANS 256
#define MAX_SPAN_BYTES 8192
#define MAX_NAME 96

struct span {
	uint16_t addr;
	uint16_t len;
};

struct vread_span {
	uint8_t bank;
	uint16_t addr;
	uint16_t len;
};

struct sread_span {
	uint8_t bank;
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
	struct sread_span sreads[MAX_SPANS];
	size_t nsreads = 0;
	struct vread_span vreads[MAX_SPANS];
	size_t nvreads = 0;
	int ramg = -1; /* -1 = leave whatever the seeds left; 0/1 = force the latch */
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
			} else if (strcmp(key, "ramg") == 0) {
				/* Applied after every seed, whatever the key order: the "sram"
				 * seed enables the latch as a side effect, so this is the only
				 * way to enter with non-zero SRAM and the latch off. */
				ramg = jnum() != 0;
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
						if (nspans + nsreads == MAX_SPANS)
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
						if (nspans + nsreads == MAX_SPANS)
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
			} else if (strcmp(key, "sread") == 0) {
				need('{');
				if (!eat('}')) {
					do {
						char bank_s[MAX_NAME];
						jstr(bank_s, sizeof bank_s);
						need(':');
						unsigned bank = (unsigned)strtoul(bank_s, NULL, 10);
						if (bank > 3)
							die("sread bank out of range");
						need('{');
						if (!eat('}')) {
							do {
								char addr_s[MAX_NAME];
								jstr(addr_s, sizeof addr_s);
								need(':');
								long n = jnum();
								if (n < 0 || n > MAX_SPAN_BYTES / 2)
									die("sread length out of range");
								uint16_t at = (uint16_t)strtoul(addr_s, NULL, 10);
								if (at < 0xA000 || (size_t)at + (size_t)n > 0xC000)
									die("sread span outside $A000-$BFFF");
								if (nspans + nsreads == MAX_SPANS)
									die("too many wram spans");
								sreads[nsreads].bank = (uint8_t)bank;
								sreads[nsreads].addr = at;
								sreads[nsreads].len = (uint16_t)n;
								nsreads++;
							} while (eat(','));
							need('}');
						}
					} while (eat(','));
					need('}');
				}
			} else if (strcmp(key, "vread") == 0) {
				need('{');
				if (!eat('}')) {
					do {
						char bank_s[MAX_NAME];
						jstr(bank_s, sizeof bank_s);
						need(':');
						unsigned bank = (unsigned)strtoul(bank_s, NULL, 10);
						if (bank > 1)
							die("vread bank out of range");
						need('{');
						if (!eat('}')) {
							do {
								char addr_s[MAX_NAME];
								jstr(addr_s, sizeof addr_s);
								need(':');
								long n = jnum();
								if (n < 0 || n > MAX_SPAN_BYTES / 2)
									die("vread length out of range");
								uint16_t at = (uint16_t)strtoul(addr_s, NULL, 10);
								if (at < 0x8000 || (size_t)at + (size_t)n > 0xA000)
									die("vread span outside $8000-$9FFF");
								if (nspans + nvreads == MAX_SPANS)
									die("too many wram spans");
								vreads[nvreads].bank = (uint8_t)bank;
								vreads[nvreads].addr = at;
								vreads[nvreads].len = (uint16_t)n;
								nvreads++;
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

	if (ramg >= 0)
		g_sram_enabled = ramg;

	call(&st);

	printf("{\"a\":%u,\"f\":%u,\"b\":%u,\"c\":%u,\"d\":%u,\"e\":%u,\"hl\":%u,\"wram\":{",
	       st.a, st.f, st.b, st.c, st.d, st.e, st.hl);
	for (size_t i = 0; i < nspans; i++) {
		printf("%s\"%u\":\"", i ? "," : "", spans[i].addr);
		for (uint16_t k = 0; k < spans[i].len; k++)
			printf("%02x", *gb_ptr((uint16_t)(spans[i].addr + k)));
		printf("\"");
	}
	printf("},\"sram\":{");
	{
		int first_bank = 1;
		for (size_t i = 0; i < nsreads;) {
			size_t j = i;
			printf("%s\"%u\":{", first_bank ? "" : ",", sreads[i].bank);
			first_bank = 0;
			for (int first_entry = 1; j < nsreads && sreads[j].bank == sreads[i].bank; j++, first_entry = 0) {
				printf("%s\"%u\":\"", first_entry ? "" : ",", sreads[j].addr);
				/* Direct g_sram index, not gb_ptr: must bypass g_sram_bank /
				 * g_sram_enabled, matching PyBoy's rambanks[bank, x] capture. */
				for (uint16_t k = 0; k < sreads[j].len; k++)
					printf("%02x", g_sram[(size_t)sreads[j].bank * 0x2000 +
							       (sreads[j].addr - 0xA000) + k]);
				printf("\"");
			}
			printf("}");
			i = j;
		}
	}
	printf("},\"vram\":{");
	{
		int first_bank = 1;
		for (size_t i = 0; i < nvreads;) {
			size_t j = i;
			printf("%s\"%u\":{", first_bank ? "" : ",", vreads[i].bank);
			first_bank = 0;
			for (int first_entry = 1; j < nvreads && vreads[j].bank == vreads[i].bank; j++, first_entry = 0) {
				printf("%s\"%u\":\"", first_entry ? "" : ",", vreads[j].addr);
				/* Direct g_vram index, not gb_ptr: must bypass g_vram_bank, so a
				 * routine that restores bank 0 before returning cannot hide what
				 * it wrote to bank 1. */
				for (uint16_t k = 0; k < vreads[j].len; k++)
					printf("%02x", g_vram[(size_t)vreads[j].bank * 0x2000 +
							       (vreads[j].addr - 0x8000) + k]);
				printf("\"");
			}
			printf("}");
			i = j;
		}
	}
	printf("}}\n");

	free(input);
	rom_free();
	return 0;
}
