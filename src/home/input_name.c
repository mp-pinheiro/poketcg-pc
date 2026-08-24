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

#include "mem.h"

/* engine/input_name.asm */
#define TX_KATAKANA 0x0fu

#include "home/random.h"

#define PLAYER_NAMING_SCREEN_KEYBOARD_DATA 0x6bafu

#include "home/sound.h"

#include "generated/wram.h"
#include "home/random.h"
#include "home/objects.h"

#include "generated/wram.h"

#include "home/input_name.h"
#include "home/bg_map.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/input_name.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/input_name.h"
#include "home/sound.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define B_CURSOR_BLINK_PERIOD_800 4u
#define CURSOR_BLINK_PERIOD_MASK_800 0x0Fu
#define MENU_CANCEL_800 0xFFu
#define SFX_CURSOR_800 0x01u
#define PADF_DOWN_800 0x80u
#define PADF_UP_800 0x40u
#define PADF_LEFT_800 0x20u
#define PADF_RIGHT_800 0x10u
#define PAD_A_800 0x01u
#define PAD_B_800 0x02u

#include "home/input_name.h"
#include "home/process_text.h"
#include "generated/wram.h"
#include "mem.h"
#define CHAR_UNDERBAR_ADDR 0x68F2u
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

/* >>> factory TransformCharacter */
/* input_name.asm:751-800. Transforms the last character of wNamingScreenBuffer
 * through the 4-byte-entry table at hl. Characters are stored in the buffer
 * big-endian (set byte first) but carried in de byte-swapped: e = set byte,
 * d = index byte. A TX_KATAKANA set byte is decremented to hiragana before the
 * lookup. Table entries are [match_index, match_set, result_set, result_index];
 * a zero match_index terminates the walk. Failure (zero length or no matching
 * entry) exits with carry+Z set (f = $90) and de holding the buffer-derived pair
 * (the caller's de when the length is zero); success exits with f = the `or a`
 * Z bit of the matched set byte. hl is left advanced: past the terminator on
 * failure, on the matched entry's last byte on success. bc is preserved. */
TransformCharacterResult TransformCharacter(uint16_t hl, uint8_t d, uint8_t e)
{
	uint8_t len = wNamingScreenBufferLength;
	if (len == 0u)
		return (TransformCharacterResult){hl, d, e, 0x90u};
	uint16_t last = (uint16_t)(wNamingScreenBuffer_ADDR + (uint8_t)(len - 2u));
	e = gb_read8(last);
	d = gb_read8((uint16_t)(last + 1u));
	if (e == TX_KATAKANA)
		e = (uint8_t)(e - 1u);
	for (;;) {
		uint8_t t0 = gb_read8(hl++);
		if (t0 == 0u)
			return (TransformCharacterResult){hl, d, e, 0x90u};
		uint8_t t1 = gb_read8(hl);
		if (t0 == d && t1 == e) {
			hl = (uint16_t)(hl + 1u);
			e = gb_read8(hl);
			hl = (uint16_t)(hl + 1u);
			d = gb_read8(hl);
			return (TransformCharacterResult){hl, d, e, (uint8_t)((t1 == 0u) ? 0x80u : 0x00u)};
		}
		hl = (uint16_t)(hl + 3u);
	}
}
/* <<< factory TransformCharacter */

/* >>> factory PlayerNamingScreen_GetCharInfoFromPos */
/* input_name.asm:808-835 */
uint16_t PlayerNamingScreen_GetCharInfoFromPos(uint16_t hl)
{
	uint8_t height = wNamingScreenKeyboardHeight;
	uint16_t product = HtimesL((uint16_t)((hl & 0xff00u) | height));
	uint8_t index = (uint8_t)(product + (uint8_t)hl);

	return (uint16_t)(PLAYER_NAMING_SCREEN_KEYBOARD_DATA +
		(uint16_t)index * 6u);
}
/* <<< factory PlayerNamingScreen_GetCharInfoFromPos */

/* >>> factory PlaySFXConfirmOrCancel_Bank6 */
void PlaySFXConfirmOrCancel_Bank6(uint8_t a)
{
	uint8_t sfx_id = (uint8_t)(a + 1u) == 0 ? SFX_CANCEL : SFX_CONFIRM;
	PlaySFX(sfx_id);
}
/* <<< factory PlaySFXConfirmOrCancel_Bank6 */

/* >>> factory PlayerNamingScreen_AdjustCursorPosition */
void PlayerNamingScreen_AdjustCursorPosition(uint8_t a)
{
	uint8_t saved_a = a;
	ZeroObjectPositions();
	if (saved_a == wInvisibleCursorTile)
		return;
	uint8_t length_half = (uint8_t)(wNamingScreenBufferLength >> 1);
	uint8_t max_length = wNamingScreenBufferMaxLength;
	uint8_t half_max = (uint8_t)(max_length >> 1);
	uint8_t position = length_half;
	if (position == half_max)
		position = (uint8_t)(position - 1u);
	position = (uint8_t)(position + wNamingScreenNamePosition);
	uint16_t product = HtimesL((uint16_t)(0x0800u | position));
	uint8_t d = (uint8_t)((uint8_t)product + 8u);
	SetOneObjectAttributes(0x18u, d, 0u, 0u);
}
/* <<< factory PlayerNamingScreen_AdjustCursorPosition */

/* >>> factory DeckNamingScreen_AdjustCursorPosition */
void DeckNamingScreen_AdjustCursorPosition(uint8_t a)
{
	uint8_t saved_a = a;
	ZeroObjectPositions();
	if (saved_a == wInvisibleCursorTile)
		return;
	uint8_t d = wNamingScreenBufferLength;
	uint8_t max_length = wNamingScreenBufferMaxLength;
	if (d == max_length)
		d = (uint8_t)(d - 1u);
	d = (uint8_t)(d - 1u);
	uint8_t name_position = wNamingScreenNamePosition;
	d = (uint8_t)(d + (uint8_t)(name_position << 1));
	uint16_t product = HtimesL((uint16_t)(0x0400u | d));
	d = (uint8_t)((uint8_t)product + 8u);
	SetOneObjectAttributes(0x18u, d, 0u, 0u);
}
/* <<< factory DeckNamingScreen_AdjustCursorPosition */

/* >>> factory PlayerNamingScreen_DrawCursor */
PlayerNamingScreen_DrawCursorResult PlayerNamingScreen_DrawCursor(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t saved_a = a;
	uint16_t char_info = PlayerNamingScreen_GetCharInfoFromPos((uint16_t)((uint16_t)gb_read8(wNamingScreenCursorX_ADDR) << 8 | gb_read8(wNamingScreenCursorY_ADDR)));
	gb_write8(0x2000u, 0x06u);
	uint8_t tile = gb_read8(char_info++);
	c = tile;
	b = (uint8_t)(gb_read8(char_info) - 1u);
	PlayerNamingScreen_AdjustCursorPosition(saved_a);
	WriteByteToBGMap0(saved_a, b, c);
	return (PlayerNamingScreen_DrawCursorResult){saved_a, (uint8_t)(saved_a == 0u ? 0x80u : 0u), b, c, d, saved_a, char_info};
}
/* <<< factory PlayerNamingScreen_DrawCursor */

/* >>> factory DeckNamingScreen_DrawCursor */
DeckNamingScreen_DrawCursorResult DeckNamingScreen_DrawCursor(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t saved_a = a;
	uint16_t char_info = DeckNamingScreen_GetCharInfoFromPos((uint16_t)((uint16_t)gb_read8(wNamingScreenCursorX_ADDR) << 8 | gb_read8(wNamingScreenCursorY_ADDR)));
	gb_write8(0x2000u, 0x06u);
	uint8_t tile = gb_read8(char_info++);
	c = tile;
	b = (uint8_t)(gb_read8(char_info) - 1u);
	DeckNamingScreen_AdjustCursorPosition(saved_a);
	WriteByteToBGMap0(saved_a, b, c);
	return (DeckNamingScreen_DrawCursorResult){saved_a, (uint8_t)(saved_a == 0u ? 0x80u : 0u), b, c, d, saved_a, char_info};
}
/* <<< factory DeckNamingScreen_DrawCursor */

/* >>> factory DeckNamingScreen_DrawInvisibleCursor */
DeckNamingScreen_DrawCursorResult DeckNamingScreen_DrawInvisibleCursor(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t a = gb_read8(wInvisibleCursorTile_ADDR);
	return DeckNamingScreen_DrawCursor(a, f, b, c, d, e, hl);
}
/* <<< factory DeckNamingScreen_DrawInvisibleCursor */

/* >>> factory DeckNamingScreen_DrawVisibleCursor */
DeckNamingScreen_DrawCursorResult DeckNamingScreen_DrawVisibleCursor(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t a = gb_read8(wVisibleCursorTile_ADDR);
	return DeckNamingScreen_DrawCursor(a, f, b, c, d, e, hl);
}
/* <<< factory DeckNamingScreen_DrawVisibleCursor */

/* >>> factory PlayerNamingScreen_DrawInvisibleCursor */
PlayerNamingScreen_DrawCursorResult PlayerNamingScreen_DrawInvisibleCursor(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t a = gb_read8(wInvisibleCursorTile_ADDR);
	return PlayerNamingScreen_DrawCursor(a, f, b, c, d, e, hl);
}
/* <<< factory PlayerNamingScreen_DrawInvisibleCursor */

/* >>> factory PlayerNamingScreen_DrawVisibleCursor */
PlayerNamingScreen_DrawCursorResult PlayerNamingScreen_DrawVisibleCursor(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t a = gb_read8(wVisibleCursorTile_ADDR);
	return PlayerNamingScreen_DrawCursor(a, f, b, c, d, e, hl);
}
/* <<< factory PlayerNamingScreen_DrawVisibleCursor */

/* >>> factory PlayerNamingScreen_CheckButtonState */
PlayerNamingScreen_DrawCursorResult PlayerNamingScreen_CheckButtonState(void)
{
	gb_write8(wMenuInputSFX_ADDR, 0u);
	uint8_t dpad = gb_read8(hDPadHeld_ADDR);
	uint8_t newX = 0u, newY = 0u;
	int did_move = 0;

	if (dpad != 0u) {
		uint8_t b = dpad;
		uint8_t c = gb_read8(wNamingScreenKeyboardHeight_ADDR);
		uint8_t h = gb_read8(wNamingScreenCursorX_ADDR);
		uint8_t l = gb_read8(wNamingScreenCursorY_ADDR);
		uint8_t a = l;

		if (b & PADF_UP_800) {
			a = (uint8_t)(a - 1u);
			if (a & 0x80u)
				a = (uint8_t)(c - 1u);
			newY = a;
			newX = h;
			did_move = 1;
		} else if (b & PADF_DOWN_800) {
			a = (uint8_t)(a + 1u);
			if (a >= c)
				a = 0u;
			newY = a;
			newX = h;
			did_move = 1;
		} else {
			c = gb_read8(wNamingScreenNumColumns_ADDR);
			a = h;
			if (b & PADF_LEFT_800) {
				uint8_t saved = a;
				if (l == 6u) {
					uint16_t hl_in = (uint16_t)(((uint16_t)h << 8) | l);
					uint16_t base = PlayerNamingScreen_GetCharInfoFromPos(hl_in);
					uint8_t entry = gb_read8((uint16_t)(base + 5u));
					uint8_t sub = (uint8_t)(entry - 1u);
					a = (uint8_t)(saved - sub);
					if (a == 0xFFu) {
						newX = (uint8_t)(c - 2u);
						did_move = 1;
						goto done_dir;
					}
					if (a == 0xFEu) {
						newX = (uint8_t)(c - 3u);
						did_move = 1;
						goto done_dir;
					}
				} else {
					a = saved;
				}
				a = (uint8_t)(a - 1u);
				if (a & 0x80u)
					a = (uint8_t)(c - 1u);
				newX = a;
				did_move = 1;
			} else if (b & PADF_RIGHT_800) {
				uint8_t saved = a;
				if (l == 6u) {
					uint16_t hl_in = (uint16_t)(((uint16_t)h << 8) | l);
					uint16_t base = PlayerNamingScreen_GetCharInfoFromPos(hl_in);
					uint8_t entry = gb_read8((uint16_t)(base + 4u));
					uint8_t sub = (uint8_t)(entry - 1u);
					a = (uint8_t)(saved + sub);
				} else {
					a = saved;
				}
				a = (uint8_t)(a + 1u);
				if (a < c) {
					newX = a;
				} else {
					uint8_t c1 = (uint8_t)(c + 1u);
					if (a < c1) {
						newX = 0u;
					} else {
						uint8_t c2 = (uint8_t)(c1 + 1u);
						newX = (a < c2) ? 1u : 2u;
					}
				}
				did_move = 1;
			}
		}
	}

done_dir:
	if (did_move) {
		uint16_t hl_pos = (uint16_t)(((uint16_t)newX << 8) | newY);
		uint16_t base2 = PlayerNamingScreen_GetCharInfoFromPos(hl_pos);
		uint16_t entry_addr = (uint16_t)(base2 + 3u);
		if (gb_read8(wd009_ADDR) == 2u)
			entry_addr = (uint16_t)(entry_addr + 2u);
		uint8_t d_reg = gb_read8(entry_addr);

		(void)PlayerNamingScreen_DrawInvisibleCursor(0u, 0u, 0u, 0u, 0u, 0u);

		gb_write8(wNamingScreenCursorY_ADDR, newY);
		gb_write8(wNamingScreenCursorX_ADDR, newX);
		gb_write8(wCheckMenuCursorBlinkCounter_ADDR, 0u);

		if (d_reg == 6u)
			return PlayerNamingScreen_CheckButtonState();
		gb_write8(wMenuInputSFX_ADDR, SFX_CURSOR_800);
	}

	{
		uint8_t keys = gb_read8(hKeysPressed_ADDR);
		if (keys & (PAD_A_800 | PAD_B_800)) {
			uint8_t press_a = (keys & PAD_A_800) ? 0u : MENU_CANCEL_800;
			(void)PlaySFXConfirmOrCancel_Bank6(press_a);
			return PlayerNamingScreen_DrawVisibleCursor(0x10u, 0u, 0u, 0u, 0u, 0u);
		}
		uint8_t sfx = gb_read8(wMenuInputSFX_ADDR);
		if (sfx != 0u)
			PlaySFX(sfx);

		uint8_t old_blink = gb_read8(wCheckMenuCursorBlinkCounter_ADDR);
		gb_write8(wCheckMenuCursorBlinkCounter_ADDR, (uint8_t)(old_blink + 1u));
		if ((old_blink & CURSOR_BLINK_PERIOD_MASK_800) != 0u)
			return (PlayerNamingScreen_DrawCursorResult){old_blink, 0u, 0u, 0u, 0u, 0u, 0u};

		uint8_t vis_tile = gb_read8(wVisibleCursorTile_ADDR);
		return PlayerNamingScreen_DrawCursor(vis_tile, 0u, 0u, 0u, 0u, 0u, 0u);
	}
}
/* <<< factory PlayerNamingScreen_CheckButtonState */

/* >>> factory PrintPlayerNameFromInput */
void PrintPlayerNameFromInput(void)
{
	uint8_t d = wNamingScreenNamePosition;
	uint8_t e = gb_read8((uint16_t)(wNamingScreenNamePosition_ADDR + 1u));
	InitTextPrinting(d, e);

	uint8_t max_len = wNamingScreenBufferMaxLength;
	uint8_t offset = (uint8_t)(0x15u - max_len);
	uint16_t underbar_hl = (uint16_t)(CHAR_UNDERBAR_ADDR + offset);
	ProcessText(&underbar_hl);

	InitTextPrinting(d, e);
	uint16_t buf_hl = wNamingScreenBuffer_ADDR;
	ProcessText(&buf_hl);
}
/* <<< factory PrintPlayerNameFromInput */
