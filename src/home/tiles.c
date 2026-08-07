#include "home/tiles.h"

#include "mem.h"
#include "ppu.h"

static uint16_t bg_map0_address(uint16_t xy)
{
	uint8_t x = (uint8_t)(xy >> 8);
	uint8_t y = (uint8_t)xy;
	return (uint16_t)(0x9800u + (uint16_t)y * TILEMAP_W + x);
}

void FillRectangle(uint8_t a, uint8_t b, uint8_t c, uint16_t de, uint16_t hl)
{
	uint16_t dst = bg_map0_address(de);
	uint8_t row_tile = a;
	uint32_t rows = c ? c : 0x100;
	uint32_t cols = b ? b : 0x100;

	do {
		uint8_t tile = row_tile;
		uint16_t pos = dst;
		uint32_t n = cols;

		do {
			gb_write8(pos++, tile);
			tile = (uint8_t)(tile + (uint8_t)hl);
		} while (--n);
		dst = (uint16_t)(dst + TILEMAP_W);
		row_tile = (uint8_t)(row_tile + (uint8_t)(hl >> 8));
	} while (--rows);
}

void Copy1bppTiles(uint16_t *hl, uint16_t *de)
{
	uint16_t src = *de;
	uint16_t dst = *hl;
	uint32_t n = 128u * 8u;

	do {
		uint8_t value = gb_read8(src++);
		gb_write8(dst++, value);
		gb_write8(dst++, value);
	} while (--n);

	*de = src;
	*hl = dst;
}
