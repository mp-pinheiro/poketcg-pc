/* >>> part includes */
#include "home/process_text.h"
#include "home/switch_rom.h"
#include "home/text_box.h"

#include "home/copy.h"
#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/write_number.h"
/* <<< part includes */
/* --- part BANK_FONTS */
/* --- part includes_SYM_SPACE */
/* >>> part SYM_SPACE */
#define SYM_SPACE 0x00u
/* <<< part SYM_SPACE */
/* >>> part SYM_0 */
#define SYM_0 0x20u
/* <<< part SYM_0 */
/* >>> part FW_SPACE */
#define FW_SPACE 0x70u
/* <<< part FW_SPACE */
/* >>> part TILE_SIZE */
#define TILE_SIZE 16u
/* <<< part TILE_SIZE */
/* >>> factory CaseHalfWidthLetter */
uint8_t CaseHalfWidthLetter(uint8_t *e)
{
	uint8_t a = wUppercaseHalfWidthLetters;
	if (!a) return 0;
	a = *e;
	if (a < 0x60u || a >= 0x7bu) return a;
	*e = (uint8_t)(a - ('a' - 'A'));
	return *e;
}
/* <<< factory CaseHalfWidthLetter */
/* >>> factory GetFullWidthFontTileOffset */
FullWidthOffsetResult GetFullWidthFontTileOffset(uint8_t d, uint8_t e)
{
	uint16_t base = 0x50u * TILE_SIZE_1BPP;
	uint8_t a = d;
	uint8_t b = 0x02u;
	uint8_t c = 0x80u;
	if (d == TX_HIRAGANA) {
		d = 0u;
		a = TX_HIRAGANA;
	} else if (d == TX_KATAKANA) {
		base = 0u;
		e = (uint8_t)(e - 0x10u);
		d = 0u;
		a = e;
		b = 0u;
		c = 0u;
	}
	uint16_t hl = (uint16_t)((((uint16_t)d << 8) | e) * TILE_SIZE_1BPP + base);
	return (FullWidthOffsetResult){a, b, c, d, e, hl};
}
/* <<< factory GetFullWidthFontTileOffset */
/* >>> factory CopyHalfWidthCharacterToDE */
FontTileResult CopyHalfWidthCharacterToDE(uint8_t a, uint16_t de)
{
	uint16_t source = (uint16_t)(HalfWidthFont_ADDR +
		(uint16_t)(uint8_t)(a - 0x20u) * TILE_SIZE_1BPP);
	uint8_t last = 0;
	for (uint8_t i = 0; i < TILE_SIZE_1BPP; i++) {
		last = font_byte(source++);
		gb_write8(de, last);
		de = (uint16_t)(de + 2u);
	}
	return (FontTileResult){last, 0u, 0u, de, source};
}
/* <<< factory CopyHalfWidthCharacterToDE */
/* >>> factory CreateHalfWidthFontTile */
FontTileResult CreateHalfWidthFontTile(uint8_t d, uint8_t e)
{
	uint8_t saved_bank = hBankROM;
	BankswitchROM(HalfWidthFont_BANK);
	CopyHalfWidthCharacterToDE(e, wTextTileBuffer_ADDR);
	CopyHalfWidthCharacterToDE(d, (uint16_t)(wTextTileBuffer_ADDR + 1u));
	uint8_t last = 0u;
	for (uint8_t i = 0u; i < TILE_SIZE_1BPP; i++) {
		uint16_t right = (uint16_t)(wTextTileBuffer_ADDR + i * 2u);
		uint8_t left = gb_read8(right);
		uint8_t pair = gb_read8((uint16_t)(right + 1u));
		last = (uint8_t)((left << 4) | (left >> 4) | pair);
		gb_write8(right, last);
		gb_write8((uint16_t)(right + 1u), last);
	}
	BankswitchROM(saved_bank);
	return (FontTileResult){(uint8_t)(HalfWidthFont_BANK - 1u), 0u, 0u, wTextTileBuffer_ADDR,
		(uint16_t)(wTextTileBuffer_ADDR + TILE_SIZE)};
}
/* <<< factory CreateHalfWidthFontTile */
/* >>> factory CreateFullWidthFontTile */
FontTileResult CreateFullWidthFontTile(uint16_t hl)
{
	uint16_t bank_stack = (uint16_t)((uint16_t)hBankROM << 8);
	BankpushROMResult pushed = BankpushROM(Fonts_BANK, 0u, 0u, 0u, 0u, 0u, hl);
	uint16_t src = pushed.hl;
	uint8_t last = 0u;
	uint16_t dst = wTextTileBuffer_ADDR;
	for (uint8_t i = 0u; i < TILE_SIZE_1BPP; i++) {
		last = gb_read8((uint16_t)(src + i));
		gb_write8(dst++, last);
		gb_write8(dst++, last);
	}
	(void)BankpopROM(0u, 0u, 0u, 0u, (uint16_t)(src + TILE_SIZE_1BPP),
		bank_stack, (uint16_t)(((uint16_t)pushed.a << 8) | pushed.f));
	(void)last;
	return (FontTileResult){(uint8_t)(Fonts_BANK - 1u), 0u, 0u, wTextTileBuffer_ADDR,
		(uint16_t)(src + TILE_SIZE_1BPP)};
}
/* <<< factory CreateFullWidthFontTile */
/* >>> factory CreateFullWidthFontTile_ConvertToTileDataAddress */
FontTileResult CreateFullWidthFontTile_ConvertToTileDataAddress(uint8_t d, uint8_t e,
	uint8_t b)
{
	FullWidthOffsetResult offset = GetFullWidthFontTileOffset(d, e);
	CreateFullWidthFontTile(offset.hl);
	uint8_t c = TILE_SIZE;
	uint16_t address = ConvertTileNumberToTileDataAddress(&b, &c);
return (FontTileResult){wTilePatternSelector, wTilePatternSelector, c,
	wTextTileBuffer_ADDR, address};
}
/* <<< factory CreateFullWidthFontTile_ConvertToTileDataAddress */
/* --- factory TwoByteNumberToTxSymbol_PadSpace */
/* === factory GenerateTextTile */
/* >>> factory TwoByteNumberToTxSymbol_TrimLeadingZeros */
/* Returns the asm's two live exit registers: a is the FIRST non-SYM_0 digit byte
 * (SYM_0 when every digit was trimmed), and hl points one before it. bc and de are
 * pushed and popped, so they are preserved. */
NumberTextResult TwoByteNumberToTxSymbol_TrimLeadingZeros(uint16_t value)
{
	static const uint16_t places[] = {10000, 1000, 100, 10, 1};
	uint16_t p = wStringBuffer_ADDR;
	uint8_t a = SYM_0;

	for (uint8_t i = 0; i < 5; i++) {
		gb_write8(p++, TX_SYMBOL);
		a = SYM_0;
		while (value >= places[i]) {
			value = (uint16_t)(value - places[i]);
			a++;
		}
		gb_write8(p++, a);
	}
	gb_write8(p, 0); /* TX_END */

	uint16_t hl = wStringBuffer_ADDR;
	uint8_t e = 5;

	for (;;) {
		hl++;
		a = gb_read8(hl);
		if (a != SYM_0)
			break;
		gb_write8(hl, SYM_SPACE);
		hl++;
		if (--e == 0) {
			/* every digit was a zero: put the last one back */
			hl--;
			gb_write8(hl, SYM_0);
			break;
		}
	}
	hl--;
	return (NumberTextResult){a, hl};
}
/* <<< factory TwoByteNumberToTxSymbol_TrimLeadingZeros */
/* >>> factory Func_235e */
ProcessTextResult Func_235e(uint8_t d, uint8_t e)
{
	if (wFontWidth) {
		CaseHalfWidthLetter(&e);
		d = wHalfWidthPrintState;
		if (!d) {
			wHalfWidthPrintState = e;
			return text_result(1, d, e, 0, 0);
		}
		wHalfWidthPrintState = 0;
	}
	uint8_t i = hffa9;
	for (;;) {
		uint8_t key = gb_read8((uint16_t)(0xc600u + i));
		if (!key) return text_result(0, d, e, 0x80, 0);
		if (key == e && gb_read8((uint16_t)(0xc700u + i)) == d) break;
		i = gb_read8((uint16_t)(0xc800u + i));
	}
	/* `cp l` leaves N set on a hit; `scf` sets C, clears N/H, leaves Z. */
	if (hffa9 == i)
		return text_result(i, d, e, 0x90, 0);

	uint8_t old = hffa9;
	uint8_t prev = gb_read8((uint16_t)(0xc900u + i));
	uint8_t next = gb_read8((uint16_t)(0xc800u + i));

	gb_write8((uint16_t)(0xc900u + old), i);
	hffa9 = i;
	gb_write8((uint16_t)(0xc900u + i), 0);
	gb_write8((uint16_t)(0xc800u + i), old);
	gb_write8((uint16_t)(0xc800u + prev), next);
	if (next)
		gb_write8((uint16_t)(0xc900u + next), prev);
	/* `inc c / dec c` leaves N set; `scf` sets C, clears N/H, leaves Z.
	 * Z is set only when next == 0 (the inc/dec pair returns to zero). */
	uint8_t f = (uint8_t)(0x10 | (next ? 0 : 0x80));
	return text_result(old, d, e, f, 0);
}
/* <<< factory Func_235e */
/* >>> factory Func_2325 */
ProcessTextResult Func_2325(uint8_t d, uint8_t e)
{
	ProcessTextResult found = Func_235e(d, e);

	if (found.f & 0x10 || found.a)
		return found;

	uint8_t index;

	if (hffa8 == wcd04) {
		/* cache full: walk to the tail and reuse that node */
		index = hffa9;
		while (gb_read8((uint16_t)(0xc800u + index)))
			index = gb_read8((uint16_t)(0xc800u + index));
		gb_write8((uint16_t)(0xc800u + gb_read8((uint16_t)(0xc900u + index))), 0);
	} else {
		/* allocate the next node, stepping over index 0: it is the terminator */
		wcd04++;
		if (!wcd04)
			wcd04++;
		index = wcd04;
	}

	uint8_t old = hffa9;

	hffa9 = index;
	gb_write8((uint16_t)(0xc900u + old), index);
	gb_write8((uint16_t)(0xc800u + index), old);
	gb_write8((uint16_t)(0xc600u + index), found.e);
	gb_write8((uint16_t)(0xc700u + index), found.d);
	return text_result(0, found.d, found.e, 0x80, 0);
}
/* <<< factory Func_2325 */
/* >>> factory ProcessSpecialTextCharacter */
ProcessTextResult ProcessSpecialTextCharacter(uint8_t a, uint16_t hl)
{
	if (a) {
		if (a == TX_HIRAGANA || a == TX_KATAKANA) {
			hJapaneseSyllabary = a;
			return text_result(0u, 0u, 0u, 0u, hl);
		}
		if (a == '\n') {
			end_of_line(hl);
			return text_result(0u, 0u, 0u, 0u, hl);
		}
		if (a == TX_SYMBOL) {
			uint8_t saved = wFontWidth;
			wFontWidth = HALF_WIDTH;
			TerminateHalfWidthText(0u, 0u, hl);
			wFontWidth = saved;
			if (!hffb0)
				PlaceNextTextTile(gb_read8(hl));
			hl++;
		} else if (a == TX_HALFWIDTH) {
			wFontWidth = HALF_WIDTH;
			return text_result(HALF_WIDTH, 0u, 0u, 0u, hl);
		} else if (a == TX_HALF2FULL) {
			TerminateHalfWidthText(0u, 0u, hl);
			wFontWidth = FULL_WIDTH;
			hJapaneseSyllabary = TX_KATAKANA;
			a = TX_KATAKANA;
		} else {
			return text_result(a, 0u, 0u, 0x10u, hl);
		}
	}
	if (hTextLineLength && hTextLineCurPos == hTextLineLength)
		end_of_line(hl);
	return text_result(0u, 0u, 0u, 0u, hl);
}
/* <<< factory ProcessSpecialTextCharacter */
/* >>> factory SetupText */
uint16_t SetupText(uint8_t d, uint8_t e)
{
	wcd04 = (uint8_t)(d - 1);
	hffa8 = e;
	InitTextFormat();
	hffb0 = 0;
	hffa9 = 0;
	wTilePatternSelector = 0x88;
	wTilePatternSelectorCorrection = 0x80;
	for (uint16_t i = wc600_ADDR; i != wc700_ADDR; i++)
		gb_write8(i, 0u);
	return wc600_ADDR;
}
/* <<< factory SetupText */
/* --- part InitTextPrinting_ProcessText */
