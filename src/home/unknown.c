#include "home/unknown.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/bg_map.h"
#include "home/deck_check.h"
#include "home/random.h"
#include "home/sound.h"

#define PAD_A 0x01u
#define PAD_B 0x02u
#define PAD_RIGHT 0x10u
#define PAD_LEFT 0x20u
#define PAD_UP 0x40u
#define PAD_DOWN 0x80u

#define B_CURSOR_BLINK_PERIOD 0x04u
#define CURSOR_BLINK_PERIOD_MASK 0x0fu
#define MENU_CANCEL 0xffu
#define MENU_CONFIRM 0x01u
#define SFX_CURSOR 0x01u

/* Tile ids verified against the real ROM's BG map writes: the blinking
 * check-menu cursor is tile $0f and the blank it is erased with is $00. */
#define SYM_CURSOR_R 0x0fu
#define SYM_SPACE 0x00u

/* unknown.asm:126-142 (.draw_tile). Column/row come straight from the
 * stored cursor position, exactly as the asm re-reads it after any move. */
static void draw_check_menu_cursor_tile(uint8_t tile)
{
	uint16_t product = HtimesL((uint16_t)(((uint16_t)wCheckMenuCursorXPosition << 8) | 10u));
	uint8_t col = (uint8_t)((product & 0xffu) + 1u);
	uint8_t row = (uint8_t)((uint16_t)(wCheckMenuCursorYPosition * 2u) + 14u);

	WriteByteToBGMap0(tile, col, row);
}
/* <<< factory statics */

/* >>> factory Func_18661 */
/* unknown.asm:1-150. Unreferenced check-menu cursor handler: reads only
 * memory (hDPadHeld, hKeysPressed, wCheckMenuCursor*), so it takes no
 * register inputs and reports just the exit a and flags. The blink test
 * masks the pre-increment counter (`ld a,[hl]` before `inc [hl]`) while
 * the cursor/blank choice tests bit 4 of the post-increment value. The
 * two PlaySFXConfirmOrCancel calls are the ROM's wrong-bank bug (it
 * should use the _Bank6 form), so no case drives those paths: the real
 * ROM executes whatever is mapped at that address instead. */
CheckMenuInputResult Func_18661(void)
{
	uint8_t x = wCheckMenuCursorXPosition;
	uint8_t y = wCheckMenuCursorYPosition;
	uint8_t dpad = hDPadHeld;
	uint8_t moved = 0u;

	wMenuInputSFX = 0;

	if (dpad != 0) {
		if ((dpad & (PAD_LEFT | PAD_RIGHT)) != 0) {
			x = (uint8_t)(x ^ 1u);
			moved = 1u;
		} else if ((dpad & (PAD_UP | PAD_DOWN)) != 0) {
			y = (uint8_t)(y ^ 1u);
			moved = 1u;
		}
	}

	if (moved != 0) {
		wMenuInputSFX = SFX_CURSOR;
		/* RAM still holds the old position here, so this erases the
		 * cursor where it was before the flip. */
		draw_check_menu_cursor_tile(SYM_SPACE);
		wCheckMenuCursorXPosition = x;
		wCheckMenuCursorYPosition = y;
		wCheckMenuCursorBlinkCounter = 0;
	}

	if ((hKeysPressed & (PAD_A | PAD_B)) != 0) {
		uint8_t button;

		if ((hKeysPressed & PAD_A) != 0) {
			draw_check_menu_cursor_tile(SYM_CURSOR_R);
			button = MENU_CONFIRM;
		} else {
			button = MENU_CANCEL;
		}
		PlaySFXConfirmOrCancel(button);
		/* scf */
		return (CheckMenuInputResult){button, 0x10u};
	}

	if (wMenuInputSFX != 0)
		PlaySFX(wMenuInputSFX);

	uint8_t old_count = wCheckMenuCursorBlinkCounter;
	uint8_t phase = (uint8_t)(old_count & CURSOR_BLINK_PERIOD_MASK);
	uint8_t new_count = (uint8_t)(old_count + 1u);

	wCheckMenuCursorBlinkCounter = new_count;
	if (phase != 0)
		return (CheckMenuInputResult){phase, 0x20u}; /* ret nz: and sets H */

	uint8_t tile = ((new_count & (uint8_t)(1u << B_CURSOR_BLINK_PERIOD)) != 0)
		? SYM_SPACE : SYM_CURSOR_R;

	draw_check_menu_cursor_tile(tile);
	/* or a */
	return (CheckMenuInputResult){tile, (uint8_t)(tile != 0 ? 0x00u : 0x80u)};
}
/* <<< factory Func_18661 */
