#include "home/bg_map.h"

#include "mem.h"
#include "ppu.h"

static uint16_t bg_map0_address(uint8_t x, uint8_t y)
{
	return (uint16_t)(0x9800u + (uint16_t)y * TILEMAP_W + x);
}

void SafeCopyDataHLtoDE(uint16_t *hl, uint16_t *de, uint8_t b)
{
	uint32_t n = b ? b : 0x100;
	uint16_t src = *hl, dst = *de;

	do {
		gb_write8(dst++, gb_read8(src++));
	} while (--n);

	*hl = src;
	*de = dst;
}

void WriteDataBlockToBGMap0(uint16_t *hl, uint16_t *de, uint8_t *a, uint8_t *b, uint8_t *c)
{
	uint8_t x = gb_read8((*hl)++);
	uint8_t y = gb_read8((*hl)++);
	uint16_t data = *hl;
	uint16_t source = data;
	uint8_t length = 0xff;

	do {
		length++;
		*a = gb_read8(*hl);
		(*hl)++;
	} while (*a != 0);

	*de = bg_map0_address(x, y);
	/* `or a / jr z, .move_to_next`: a zero-length block copies nothing at all. Without
	 * this the count underflows and the copy runs away over its own source. */
	if (length) {
		uint32_t n = length;
		do {
			*a = gb_read8(source++);
			gb_write8((*de)++, *a);
		} while (--n);
	}

	*b = 0;
	*c = (uint8_t)(length + 1);
	*hl = (uint16_t)(data + (uint8_t)(length + 1));
}

void WriteDataBlocksToBGMap0(uint16_t *hl, uint16_t *de, uint8_t *a, uint8_t *b, uint8_t *c)
{
	do {
		WriteDataBlockToBGMap0(hl, de, a, b, c);
	} while ((gb_read8(*hl) & 0x80) == 0);
}

void WriteByteToBGMap0(uint8_t a, uint8_t b, uint8_t c)
{
	gb_write8(bg_map0_address(b, c), a);
}

/* Not an alias of WriteByteToBGMap0: HblankCopyDataHLtoDE ends on `ldh a, [rSTAT] /
 * and STAT_MODE`, and its loop only exits when that is zero, so exit a is always 0. */
uint8_t HblankWriteByteToBGMap0(uint8_t a, uint8_t b, uint8_t c)
{
	gb_write8(bg_map0_address(b, c), a);
	return 0;
}

void CopyDataToBGMap0(uint8_t a, uint16_t *hl, uint16_t *de, uint8_t b, uint8_t c)
{
	*de = bg_map0_address(b, c);
	SafeCopyDataHLtoDE(hl, de, a);
}
