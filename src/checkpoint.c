#include "checkpoint.h"

#include "mem.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* The checkpoint files are the flat JSON arrays explore.py emits, so this reads
 * them with a scanner narrow enough to have no dependency: find "key":[ and
 * consume decimal bytes until the closing bracket. */

static const char *find_array(const char *text, const char *key)
{
	char pattern[64];
	int written = snprintf(pattern, sizeof pattern, "\"%s\":[", key);
	if (written < 0 || (size_t)written >= sizeof pattern)
		return NULL;
	const char *at = strstr(text, pattern);
	return at ? at + written : NULL;
}

static int read_bytes(const char *cursor, uint8_t *out, size_t count)
{
	if (!cursor)
		return -1;
	for (size_t i = 0; i < count; i++) {
		char *end = NULL;
		long value = strtol(cursor, &end, 10);
		if (end == cursor || value < 0 || value > 255)
			return -1;
		out[i] = (uint8_t)value;
		cursor = end;
		while (*cursor == ',' || *cursor == ' ')
			cursor++;
	}
	return 0;
}

static int read_number(const char *text, const char *key, long *out)
{
	char pattern[64];
	int written = snprintf(pattern, sizeof pattern, "\"%s\":", key);
	if (written < 0 || (size_t)written >= sizeof pattern)
		return -1;
	const char *at = strstr(text, pattern);
	if (!at)
		return -1;
	char *end = NULL;
	long value = strtol(at + written, &end, 10);
	if (end == at + written)
		return -1;
	*out = value;
	return 0;
}

int checkpoint_load(const char *path)
{
	if (!path)
		return -1;
	FILE *file = fopen(path, "rb");
	if (!file)
		return -1;
	if (fseek(file, 0, SEEK_END) != 0) {
		fclose(file);
		return -1;
	}
	long size = ftell(file);
	if (size <= 0 || fseek(file, 0, SEEK_SET) != 0) {
		fclose(file);
		return -1;
	}
	char *text = malloc((size_t)size + 1);
	if (!text) {
		fclose(file);
		return -1;
	}
	size_t read = fread(text, 1, (size_t)size, file);
	fclose(file);
	text[read] = '\0';

	int status = 0;
	status |= read_bytes(find_array(text, "wram"), g_wram, sizeof g_wram);
	status |= read_bytes(find_array(text, "hram"), g_hram, sizeof g_hram);
	status |= read_bytes(find_array(text, "io"), g_io, sizeof g_io);
	status |= read_bytes(find_array(text, "oam"), g_oam, sizeof g_oam);
	status |= read_bytes(find_array(text, "palette_ram"), g_pal, sizeof g_pal);
	status |= read_bytes(find_array(text, "vram_bank_0"), g_vram, 0x2000);
	status |= read_bytes(find_array(text, "vram_bank_1"), g_vram + 0x2000, 0x2000);
	status |= read_bytes(find_array(text, "sram"), g_sram, sizeof g_sram);

	long rom_bank = 0;
	long vram_bank = 0;
	if (read_number(text, "rom_bank", &rom_bank) == 0)
		g_rom_bank = (uint8_t)(rom_bank & 0x3F);
	if (read_number(text, "vram_bank", &vram_bank) == 0)
		g_vram_bank = (uint8_t)(vram_bank & 0x01);
	free(text);
	return status == 0 ? 0 : -1;
}
