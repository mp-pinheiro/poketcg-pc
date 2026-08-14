#include "home/input_name.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "home/random.h"

/* DeckNamingScreen_KeyboardData sits immediately after the 25-byte routine in
 * its engine bank: label at $7019 (oracle-confirmed: index 0 returns $7019,
 * and every nonzero case differs from it by exactly 3*index). The routine only
 * computes the address; callers dereference it through the bus under the bank
 * they switched, so no rom_ptr here. */
#define DECKNAMING_KEYBOARD_DATA 0x7019u
/* <<< factory statics */

/* >>> factory DeckNamingScreen_GetCharInfoFromPos */
/* input_name.asm:1434-1452. Index into the 3-byte keyboard datum table from
 * cursor position hl (h = column, l = row): index = column * height + row,
 * where height = wNamingScreenKeyboardHeight and the `add e` wraparound is
 * kept exact in 8 bits. The `or a / ret z` pre-check means an index of 0
 * selects datum 0 itself -- unlike a counted copy loop, 0 is NOT maximum
 * here. de is push/popped and bc untouched (preserved); a and f are clobbered
 * loop residue and not part of the contract. */
uint16_t DeckNamingScreen_GetCharInfoFromPos(uint16_t hl)
{
	uint8_t row = (uint8_t)hl;
	uint8_t column = (uint8_t)(hl >> 8);
	uint16_t prod = HtimesL((uint16_t)((uint16_t)column << 8 | wNamingScreenKeyboardHeight));
	uint8_t index = (uint8_t)((uint8_t)prod + row);
	uint16_t addr = DECKNAMING_KEYBOARD_DATA;
	while (index != 0u) {
		addr = (uint16_t)(addr + 3u);
		index = (uint8_t)(index - 1u);
	}
	return addr;
}
/* <<< factory DeckNamingScreen_GetCharInfoFromPos */
