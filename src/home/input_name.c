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

#include "home/sound.h"

#define MENU_CANCEL 0xFFu
#define SFX_CONFIRM 0x02u
#define SFX_CANCEL  0x03u
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

/* >>> factory ClearMemory_Bank6 */
/* input_name.asm:32-44. Fills `a` bytes at hl with zero. The loop is
 * post-tested via `dec b`/`jr nz`, so a == 0 wraps to 256 writes. The asm
 * push/pops af, bc and hl, so no register is produced: the adapter leaves
 * the probe state untouched. */
void ClearMemory_Bank6(uint8_t a, uint16_t hl)
{
	uint32_t n = a ? a : 0x100u;
	for (uint32_t i = 0; i < n; i++)
		gb_write8(hl++, 0u);
}
/* <<< factory ClearMemory_Bank6 */

/* >>> factory DrawTextboxForKeyboard */
/* input_name.asm:243-252. Forwards the caller's a and hl (text pointer) to
 * DrawRegularTextBox with the keyboard area's geometry: x=0 (d), y=3 (e),
 * w=20 (b), h=15 (c). The wrapper itself clobbers bc/de and whatever the
 * callee leaves in af, so only the callee's advanced hl is a load-bearing
 * output and is written back through the pointer. */
void DrawTextboxForKeyboard(uint16_t *hl, uint8_t a)
{
	DrawRegularTextBox(hl, a, 20u, 15u, 0u, 3u);
}
/* <<< factory DrawTextboxForKeyboard */
