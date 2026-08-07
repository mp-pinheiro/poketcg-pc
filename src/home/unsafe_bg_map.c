#include "home/unsafe_bg_map.h"

#include "home/empty_screen.h"
#include "mem.h"

void UnsafeWriteDataBlockToBGMap0(uint16_t *hl, uint16_t *de)
{
	uint8_t x = gb_read8((*hl)++);
	uint8_t y = gb_read8((*hl)++);
	uint16_t addr = BCCoordToBGMap0Address(x, y);
	uint8_t a;

	*de = addr;
	*hl = addr; /* asm BCCoordToBGMap0Address leaves the address in hl, so the
		     * scan below reads VRAM, not the WRAM struct */
	do {
		a = gb_read8((*hl)++);
		if (a)
			gb_write8((*de)++, a);
	} while (a);
}
