/* --- part BANK_FONTS */
/* --- part includes_SYM_SPACE */
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
/* --- part InitTextPrinting_ProcessText */
