#include "home/process_text.h"
#include "home/switch_rom.h"
#include "home/text_box.h"

#include "home/copy.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/write_number.h"
#define TX_CTRL_START 0x05
#define TX_SYMBOL 0x05
#define TX_HALFWIDTH 0x06
#define TX_HIRAGANA 0x0e
#define TX_KATAKANA 0x0f
#define TX_CTRL_END 0x10
#define TILE_SIZE 16
#define TILE_SIZE_1BPP 8

void InitTextFormat(void)
{
	wFontWidth = 0;
	hTextLineCurPos = 0;
	wHalfWidthPrintState = 0;
	hJapaneseSyllabary = TX_KATAKANA;
}

uint8_t CaseHalfWidthLetter(uint8_t *e)
{
	uint8_t a = wUppercaseHalfWidthLetters;
	if (!a) return 0;
	a = *e;
	if (a < 0x60 || a >= 0x7b) return a;
	*e = (uint8_t)(a - ('a' - 'A'));
	return *e;
}

/* Returns the exit flag byte. The carry is the real output -- callers branch on it to
 * decide whether the pair was swapped -- so it has to be modelled rather than reported
 * as a bool in `a`, which the asm leaves holding path-dependent residue.
 * Every path ends on `or a` (Z from the value in a, carry clear) except the swap, which
 * ends on `scf`; the `cp` before it excludes equality, so Z is clear there. */
uint8_t ClassifyTextCharacterPair(uint8_t *d, uint8_t *e)
{
	if (wFontWidth)
		return wFontWidth ? 0x00 : 0x80;
	if (*e >= TX_CTRL_END && *e < 0x60 && hJapaneseSyllabary == TX_KATAKANA) {
		*d = TX_KATAKANA;
		return hJapaneseSyllabary ? 0x00 : 0x80;
	}
	if (*e < TX_CTRL_START) {
		uint8_t first = *e;
		*e = *d;
		*d = first;
		return 0x10;
	}
	/* a holds e on the >= $60 and >= TX_CTRL_START paths, and hJapaneseSyllabary on
	 * the wrong-syllabary path; only the latter can be zero and set Z. */
	uint8_t resid = (*e >= TX_CTRL_END && *e < 0x60) ? hJapaneseSyllabary : *e;
	*d = 0;
	return resid ? 0x00 : 0x80;
}

TextLength GetTextLengthInHalfTiles(uint16_t hl)
{
	TextLength out = {0, 0, 0};
	uint16_t p = hl;
	while (1) {
		uint8_t a = gb_read8(p++);
		if (!a) break;
		out.c++;
		if (a >= TX_CTRL_START && a < TX_CTRL_END) {
			if (a == TX_SYMBOL) {
				out.b++;
				out.c++;
				p++;
			}
			continue;
		}
		uint8_t e = a;
		uint8_t d = gb_read8(p);
		out.b++;
		if (!ClassifyTextCharacterPair(&d, &e)) continue;
		out.c++;
		p++;
	}
	out.a = (uint8_t)(0 - out.b);
	return out;
}

TextLength GetTextLengthInTiles(uint16_t hl)
{
	if (gb_read8(hl) == TX_HALFWIDTH) {
		TextLength out = GetTextLengthInHalfTiles(hl);
		out.b = (uint8_t)((out.b + 1) >> 1);
		out.a = (uint8_t)(0 - out.b);
		return out;
	}
	wFontWidth = 0;
	return GetTextLengthInHalfTiles(hl);
}

uint16_t GetFullWidthFontTileOffset(uint8_t d, uint8_t e)
{
	uint16_t base = 0x50u * TILE_SIZE_1BPP;
	if (d == TX_HIRAGANA) {
		d = 0;
	} else if (d == TX_KATAKANA) {
		base = 0;
		e = (uint8_t)(e - 0x10);
	}
	return (uint16_t)(base + (uint16_t)e * TILE_SIZE_1BPP);
}

uint16_t ConvertTileNumberToTileDataAddress(uint8_t *b, uint8_t *c)
{
	uint8_t n = (uint8_t)(*b ^ wTilePatternSelectorCorrection);
	uint16_t out = (uint16_t)(wTilePatternSelector + (uint16_t)n * TILE_SIZE);
	*b = wTilePatternSelector;
	*c = TILE_SIZE;
	return out;
}

/* `ld a, [hli]` is a bus read, so the font tables resolve under whichever ROM bank the
 * caller left mapped -- these routines never bank-switch for themselves. Indexing the
 * ROM image at the fonts' own bank instead would read data the hardware would not. */
static uint8_t font_byte(uint16_t address)
{
	return gb_read8(address);
}

FontTileResult CopyHalfWidthCharacterToDE(uint8_t a, uint16_t de)
{
	uint16_t source = (uint16_t)(0x6668u + (uint16_t)(uint8_t)(a - 0x20) * TILE_SIZE_1BPP);
	uint8_t last = 0;
	for (uint8_t i = 0; i < TILE_SIZE_1BPP; i++) {
		last = font_byte(source++);
		gb_write8(de, last);
		de = (uint16_t)(de + 2);
	}
return (FontTileResult){last, 0, 0, de, source};
}

FontTileResult CreateHalfWidthFontTile(uint8_t d, uint8_t e)
{
	uint8_t saved_bank = hBankROM;
	BankswitchROM(0x1d);
	CopyHalfWidthCharacterToDE(e, wTextTileBuffer_ADDR);
	CopyHalfWidthCharacterToDE(d, (uint16_t)(wTextTileBuffer_ADDR + 1));
	for (uint8_t i = 0; i < TILE_SIZE_1BPP; i++) {
		uint16_t right = (uint16_t)(wTextTileBuffer_ADDR + i * 2);
		uint8_t v = gb_read8(right);
		v = (uint8_t)((v << 4) | (v >> 4) | gb_read8((uint16_t)(right + 1)));
		gb_write8(right, v);
		gb_write8((uint16_t)(right + 1), v);
	}
	BankswitchROM(saved_bank);
return (FontTileResult){0x24, 0, 0, wTextTileBuffer_ADDR,
	(uint16_t)(wTextTileBuffer_ADDR + TILE_SIZE)};
}

FontTileResult CreateFullWidthFontTile(uint16_t hl)
{
	uint8_t saved_bank = hBankROM;
	BankswitchROM(0x1d);
	for (uint8_t i = 0; i < TILE_SIZE_1BPP; i++) {
		uint8_t v = font_byte((uint16_t)(hl + i));
		uint16_t dst = (uint16_t)(wTextTileBuffer_ADDR + i * 2);
		gb_write8(dst, v);
		gb_write8((uint16_t)(dst + 1), v);
	}
	BankswitchROM(saved_bank);
return (FontTileResult){0x25, 0, 0, wTextTileBuffer_ADDR,
	(uint16_t)(hl + TILE_SIZE_1BPP)};
}

FontTileResult CreateFullWidthFontTile_ConvertToTileDataAddress(uint8_t d, uint8_t e,
	uint8_t b)
{
	uint16_t offset = GetFullWidthFontTileOffset(d, e);
	CreateFullWidthFontTile((uint16_t)(0x4000u + offset));
	uint8_t c = TILE_SIZE;
	uint16_t address = ConvertTileNumberToTileDataAddress(&b, &c);
return (FontTileResult){wTilePatternSelector, wTilePatternSelector, c,
	wTextTileBuffer_ADDR, address};
}

uint8_t GenerateTextTile(uint8_t b, uint8_t d, uint8_t e)
{
	uint16_t source = wTextTileBuffer_ADDR;
	uint16_t destination;
	uint8_t c;
	if (wFontWidth) {
		CreateHalfWidthFontTile(d, e);
		destination = ConvertTileNumberToTileDataAddress(&b, &c);
	} else {
		FontTileResult tile = CreateFullWidthFontTile_ConvertToTileDataAddress(d, e, b);
		destination = tile.hl;
		c = TILE_SIZE;
	}
	SafeCopyDataDEtoHL(&source, &destination, c);
	return gb_read8((uint16_t)(source - 1));
}


uint8_t TwoByteNumberToTxSymbol_PadSpace(uint16_t hl)
{
	uint16_t p = wStringBuffer_ADDR;
	uint16_t value = hl;
	static const uint16_t places[] = {10000, 1000, 100, 10, 1};
	uint8_t digits[5];
	for (uint8_t i = 0; i < 5; i++) {
		gb_write8(p++, TX_SYMBOL);
		digits[i] = 0;
		while (value >= places[i]) { value = (uint16_t)(value - places[i]); digits[i]++; }
		gb_write8(p++, (uint8_t)(0x20 + digits[i]));
	}
	gb_write8(p, 0);
	uint8_t first = 0;
	while (first < 4 && digits[first] == 0) {
		gb_write8((uint16_t)(wStringBuffer_ADDR + 1 + first * 2), 0);
		first++;
	}
	return (uint8_t)(0x20 + digits[4]);
}


