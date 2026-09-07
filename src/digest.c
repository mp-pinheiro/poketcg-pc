#include "digest.h"

#include "mem.h"

#include <stdlib.h>
#include <string.h>

typedef struct {
	const char *name;
	const uint8_t *bytes;
	uint32_t length;
	uint8_t *mask;
} DigestRegion;

static DigestRegion g_regions[4];
static uint8_t g_scratch_copy[0x4000];
static FILE *g_sink;
static uint32_t g_crc_table[256];

static void crc_init(void)
{
	for (uint32_t i = 0; i < 256u; i++) {
		uint32_t c = i;
		for (int k = 0; k < 8; k++)
			c = (c & 1u) ? 0xEDB88320u ^ (c >> 1) : c >> 1;
		g_crc_table[i] = c;
	}
}

static uint32_t crc32_bytes(const uint8_t *data, uint32_t length)
{
	uint32_t c = 0xFFFFFFFFu;
	for (uint32_t i = 0; i < length; i++)
		c = g_crc_table[(c ^ data[i]) & 0xFFu] ^ (c >> 8);
	return c ^ 0xFFFFFFFFu;
}

static DigestRegion *region_named(const char *name, size_t length)
{
	for (size_t i = 0; i < 4; i++)
		if (strlen(g_regions[i].name) == length &&
		    memcmp(g_regions[i].name, name, length) == 0)
			return &g_regions[i];
	return NULL;
}

static int load_mask(const char *path)
{
	FILE *file = fopen(path, "r");
	char line[256];
	if (!file)
		return -1;
	while (fgets(line, sizeof line, file)) {
		char *cursor = line;
		while (*cursor == ' ' || *cursor == '\t')
			cursor++;
		if (*cursor == '#' || *cursor == '\n' || *cursor == '\0')
			continue;
		char *name = cursor;
		while (*cursor && *cursor != ' ' && *cursor != '\t')
			cursor++;
		if (!*cursor) {
			fclose(file);
			return -1;
		}
		DigestRegion *region = region_named(name, (size_t)(cursor - name));
		char *end = NULL;
		unsigned long start = strtoul(cursor, &end, 0);
		unsigned long stop = strtoul(end, &end, 0);
		if (!region || end == cursor || stop < start) {
			fclose(file);
			return -1;
		}
		if (stop > region->length)
			stop = region->length;
		for (unsigned long i = start; i < stop; i++)
			region->mask[i] = 1u;
	}
	fclose(file);
	return 0;
}

int digest_open(const char *sink_path, const char *mask_path)
{
	static uint8_t wram_mask[0x2000], hram_mask[0x80], oam_mask[0xA0], vram_mask[0x4000];
	g_regions[0] = (DigestRegion){"wram", g_wram, sizeof wram_mask, wram_mask};
	g_regions[1] = (DigestRegion){"hram", g_hram, sizeof hram_mask, hram_mask};
	g_regions[2] = (DigestRegion){"oam", g_oam, sizeof oam_mask, oam_mask};
	g_regions[3] = (DigestRegion){"vram", g_vram, sizeof vram_mask, vram_mask};
	crc_init();
	if (mask_path && load_mask(mask_path) != 0)
		return -1;
	g_sink = fopen(sink_path, "wb");
	return g_sink ? 0 : -1;
}

void digest_anchor(uint32_t ordinal)
{
	uint8_t record[16];
	(void)ordinal;
	if (!g_sink)
		return;
	for (size_t r = 0; r < 4; r++) {
		const DigestRegion *region = &g_regions[r];
		memcpy(g_scratch_copy, region->bytes, region->length);
		for (uint32_t i = 0; i < region->length; i++)
			if (region->mask[i])
				g_scratch_copy[i] = 0u;
		uint32_t crc = crc32_bytes(g_scratch_copy, region->length);
		record[r * 4 + 0] = (uint8_t)crc;
		record[r * 4 + 1] = (uint8_t)(crc >> 8);
		record[r * 4 + 2] = (uint8_t)(crc >> 16);
		record[r * 4 + 3] = (uint8_t)(crc >> 24);
	}
	fwrite(record, 1, sizeof record, g_sink);
}

int digest_close(void)
{
	int status = 0;
	if (g_sink) {
		if (fclose(g_sink) != 0)
			status = -1;
		g_sink = NULL;
	}
	return status;
}
