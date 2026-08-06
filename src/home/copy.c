#include "home/copy.h"

#include "mem.h"

/* The wLCDC bit-7 path (copy.asm:6-23) matches .next_tile for every c != 0, but at
 * c == 0 it adds bc = $0000 (copy.asm:13,19) and never advances hl/de. This port always
 * takes .next_tile. */
void CopyGfxData(uint16_t *hl, uint16_t *de, uint8_t b, uint8_t c)
{
	uint32_t blocks = b ? b : 0x100;
	uint32_t len = c ? c : 0x100;
	uint16_t src = *hl, dst = *de;

	do {
		uint32_t n = len;
		do {
			gb_write8(dst++, gb_read8(src++));
		} while (--n);
	} while (--blocks);

	*hl = src;
	*de = dst;
}

/* copy.asm:49-57. `dec bc / ld a, c / or b / jr nz` tests after the store, so
 * bc == 0 copies 65536 bytes rather than none. */
void CopyDataHLtoDE(uint16_t *hl, uint16_t *de, uint16_t bc)
{
	uint32_t n = bc ? bc : 0x10000;
	uint16_t src = *hl, dst = *de;

	do {
		gb_write8(dst++, gb_read8(src++));
	} while (--n);

	*hl = src;
	*de = dst;
}

/* copy.asm:38-46 */
void CopyDataHLtoDE_SaveRegisters(uint16_t hl, uint16_t de, uint16_t bc)
{
	CopyDataHLtoDE(&hl, &de, bc);
}
