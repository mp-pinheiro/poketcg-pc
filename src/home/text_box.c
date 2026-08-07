#include "home/text_box.h"

#include "generated/hram.h"
#include "mem.h"
#include "ppu.h"

void SafeCopyDataDEtoHL(uint16_t *de, uint16_t *hl, uint8_t c)
{
	uint32_t count = c ? c : 0x100;
	uint16_t source = *de;
	uint16_t destination = *hl;

	do {
		gb_write8(destination++, gb_read8(source++));
	} while (--count);

	*de = source;
	*hl = destination;
}

uint16_t DECoordToBGMap0Address(uint8_t d, uint8_t e)
{
	uint16_t offset = (uint16_t)((uint16_t)e * TILEMAP_W + d);

	return (uint16_t)(0x9800u + offset);
}

void AdjustCoordinatesForBGScroll(uint8_t *d, uint8_t *e)
{
	uint8_t x = (uint8_t)((hSCX >> 3) & 0x1f);
	uint8_t y = (uint8_t)((hSCY >> 3) & 0x1f);

	*d = (uint8_t)(*d + x);
	*e = (uint8_t)(*e + y);
}

void CopyLine(uint16_t *hl, uint8_t a, uint8_t b, uint8_t d, uint8_t e)
{
	uint16_t destination = *hl;
	uint8_t middle_raw = (uint8_t)(b - 2);
	uint32_t middle = middle_raw ? middle_raw : 0x100;

	gb_write8(destination++, d);
	do {
		gb_write8(destination++, a);
	} while (--middle);
	gb_write8(destination++, e);

	*hl = (uint16_t)(*hl + TILEMAP_W);
}
