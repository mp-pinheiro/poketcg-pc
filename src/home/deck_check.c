#include "home/deck_check.h"

#include "generated/wram.h"
#include "home/bg_map.h"
#include "home/random.h"
#include "home/sound.h"
/* >>> factory statics */
#define SYM_SPACE 0x00u
#define SYM_CURSOR_R 0x0Fu

#include "home/deck_check.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#define B_PAD_DOWN_MASK 0x80u
#define B_PAD_UP_MASK 0x40u
#define B_PAD_LEFT_MASK 0x20u
#define B_PAD_RIGHT_MASK 0x10u
#define PAD_A_MASK 0x01u
#define PAD_B_MASK 0x02u
#define B_CURSOR_BLINK_PERIOD 4u
#define CURSOR_BLINK_PERIOD_MASK 0x0Fu
#define MENU_CANCEL 0xFFu
#define MENU_CONFIRM 0x01u
#define SFX_CURSOR 0x01u
/* <<< factory statics */

#define SFX_CONFIRM 0x02u
#define SFX_CANCEL 0x03u

DrawCheckMenuCursorResult DrawCheckMenuCursor(uint8_t a)
{
	uint16_t product = HtimesL((uint16_t)((uint16_t)wCheckMenuCursorXPosition << 8 | 10u));
	uint8_t b = (uint8_t)(product + 1u);
	uint8_t c = (uint8_t)((uint8_t)(wCheckMenuCursorYPosition << 1) + 14u);

	WriteByteToBGMap0(a, b, c);
	return (DrawCheckMenuCursorResult){a, a, a == 0 ? 0x80u : 0};
}

void PlaySFXConfirmOrCancel(uint8_t a)
{
	uint8_t sfx_id = (uint8_t)(a + 1u) == 0 ? SFX_CANCEL : SFX_CONFIRM;
	PlaySFX(sfx_id);
}

/* >>> factory EraseCheckMenuCursor */
/* deck_check.asm:95-97 */
DrawCheckMenuCursorResult EraseCheckMenuCursor(void)
{
	return DrawCheckMenuCursor(SYM_SPACE);
}
/* <<< factory EraseCheckMenuCursor */

/* >>> factory DisplayCheckMenuCursor */
/* deck_check.asm:123-125 */
DrawCheckMenuCursorResult DisplayCheckMenuCursor(void)
{
	return DrawCheckMenuCursor(SYM_CURSOR_R);
}
/* <<< factory DisplayCheckMenuCursor */

/* >>> factory HandleCheckMenuInput */
HandleCheckMenuInputResult HandleCheckMenuInput(void)
{
	wMenuInputSFX = 0u;
	uint8_t d = wCheckMenuCursorXPosition;
	uint8_t e = wCheckMenuCursorYPosition;

	uint8_t pad = hDPadHeld;
	if (pad != 0u) {
		uint8_t moved = 0u;
		if ((pad & B_PAD_LEFT_MASK) != 0u) {
			d ^= 0x01u;
			moved = 1u;
		} else if ((pad & B_PAD_RIGHT_MASK) != 0u) {
			d ^= 0x01u;
			moved = 1u;
		} else if ((pad & B_PAD_UP_MASK) != 0u) {
			e ^= 0x01u;
			moved = 1u;
		} else if ((pad & B_PAD_DOWN_MASK) != 0u) {
			e ^= 0x01u;
			moved = 1u;
		}
		if (moved != 0u) {
			wMenuInputSFX = SFX_CURSOR;
			(void)EraseCheckMenuCursor();
			wCheckMenuCursorXPosition = d;
			wCheckMenuCursorYPosition = e;
			wCheckMenuCursorBlinkCounter = 0u;
		}
	}

	uint8_t keys = hKeysPressed;
	uint8_t ab = (uint8_t)(keys & (PAD_A_MASK | PAD_B_MASK));
	if (ab != 0u) {
		if ((ab & PAD_A_MASK) != 0u) {
			(void)DisplayCheckMenuCursor();
			(void)PlaySFXConfirmOrCancel(MENU_CONFIRM);
			return (HandleCheckMenuInputResult){MENU_CONFIRM, 0x10u};
		}
		(void)PlaySFXConfirmOrCancel(MENU_CANCEL);
		return (HandleCheckMenuInputResult){MENU_CANCEL, 0x90u};
	}

	if (wMenuInputSFX != 0u)
		PlaySFX(wMenuInputSFX);

	uint8_t old_counter = wCheckMenuCursorBlinkCounter;
	wCheckMenuCursorBlinkCounter = (uint8_t)(old_counter + 1u);
	uint8_t masked = (uint8_t)(old_counter & CURSOR_BLINK_PERIOD_MASK);
	if (masked != 0u)
		return (HandleCheckMenuInputResult){masked, 0x20u};

	if ((wCheckMenuCursorBlinkCounter & (1u << B_CURSOR_BLINK_PERIOD)) == 0u) {
		DrawCheckMenuCursorResult r = DrawCheckMenuCursor(SYM_CURSOR_R);
		return (HandleCheckMenuInputResult){r.a, r.f};
	}
	DrawCheckMenuCursorResult r2 = EraseCheckMenuCursor();
	return (HandleCheckMenuInputResult){r2.a, r2.f};
}
/* <<< factory HandleCheckMenuInput */
