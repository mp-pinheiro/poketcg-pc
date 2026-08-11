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
#define SYM_SPACE 0x00
#define SYM_0 0x20
#define FW_SPACE 0x70
#define TX_HALF2FULL 0x07
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
	uint16_t out = (uint16_t)(((uint16_t)wTilePatternSelector << 8) +
		(uint16_t)n * TILE_SIZE);
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


/* Returns the asm's two live exit registers: a is the FIRST non-SYM_0 digit byte
 * (SYM_0 when every digit was trimmed), and hl points one before it. bc and de are
 * pushed and popped, so they are preserved. */
NumberTextResult TwoByteNumberToTxSymbol_PadSpace(uint16_t value)
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



static ProcessTextResult text_result(uint8_t a, uint8_t d, uint8_t e, uint8_t f,
	uint16_t hl)
{
	return (ProcessTextResult){a, d, e, f, hl};
}

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


/* Exported: four callers outside this file (print_text.asm:289,
 * deck_machine.asm:970/1002, printer.asm:715). */
void Func_22ca(uint8_t d, uint8_t e)
{
	if (hffb0 & 1) {
		Func_235e(d, e);
		return;
	}
	ProcessTextResult out = Func_2325(d, e);
	if (!(out.f & 0x10)) {
		if (out.a) return;
		GenerateTextTile(hffa9, out.d, out.e);
	}
	if (!(hffb0 & 2))
		PlaceNextTextTile(gb_read8(hffa9_ADDR));
}

PlaceTextResult PlaceNextTextTile(uint8_t a)
{
	wCurTextTile = a;
	uint16_t address = (uint16_t)(hTextBGMap0Address |
		((uint16_t)gb_read8(0xffabu) << 8));
	address++;
	hTextBGMap0Address = (uint8_t)address;
	gb_write8(0xffabu, (uint8_t)(address >> 8));
	uint16_t destination = (uint16_t)(address - 1);
	uint16_t source = wCurTextTile_ADDR;
	SafeCopyDataDEtoHL(&source, &destination, 1);
	hTextLineCurPos++;
	return (PlaceTextResult){a, 0, 0, (uint8_t)(source >> 8), (uint8_t)source, hTextLineCurPos_ADDR};
}

ProcessTextResult TerminateHalfWidthText(uint8_t d, uint8_t e, uint16_t hl)
{
	/* Both early exits are `or a / ret z` (process_text.asm:264-269), so the Z
	 * flag is set on the way out; callers scf on top of it. */
	if (!wFontWidth || !wHalfWidthPrintState) return text_result(0, d, e, 0x80, hl);
	uint8_t pair = ' ';
	Func_22ca(d, pair);
	return text_result(0, d, e, 0, hl);
}

/* hTextBGMap0Address is a 16-bit pair at $FFAA/$FFAB; the asm carries the low-byte
 * add into the high byte with `adc $0`. */
static void next_line(void)
{
	uint8_t b = (uint8_t)(hTextHorizontalAlign + 32u);
	uint16_t bg = (uint16_t)((hTextBGMap0Address & 0xe0u) + b);

	hTextLineCurPos = 0;
	hTextBGMap0Address = (uint8_t)bg;
	gb_write8(0xffabu, (uint8_t)(gb_read8(0xffabu) + (bg >> 8)));
	wCurTextLine++;
}

/* `call z, .next_line` falls through into .next_line, so a DOUBLE_SPACED line
 * advances twice. */
static void end_of_line(uint16_t hl)
{
	TerminateHalfWidthText(0, 0, hl);
	if (!wLineSeparation)
		next_line();
	next_line();
}

ProcessTextResult ProcessSpecialTextCharacter(uint8_t a, uint16_t hl)
{
	if (a) {
		if (a == TX_HIRAGANA || a == TX_KATAKANA) {
			hJapaneseSyllabary = a;
			return text_result(0, 0, 0, 0, hl);
		}
		if (a == '\n') {
			end_of_line(hl);
			return text_result(0, 0, 0, 0, hl);
		}
		if (a == TX_SYMBOL) {
			/* forced HALF_WIDTH so the pending half-width pair is flushed
			 * before the symbol tile lands, then restored */
			uint8_t saved = wFontWidth;

			wFontWidth = 1;
			TerminateHalfWidthText(0, 0, hl);
			wFontWidth = saved;
			if (!hffb0)
				PlaceNextTextTile(gb_read8(hl));
			hl++;
			/* falls through to the shared line-length check */
		} else if (a == TX_HALFWIDTH) {
			wFontWidth = 1;
			return text_result(1, 0, 0, 0, hl);
		} else if (a == TX_HALF2FULL) {
			TerminateHalfWidthText(0, 0, hl);
			wFontWidth = 0;
			hJapaneseSyllabary = TX_KATAKANA;
			return text_result(TX_KATAKANA, 0, 0, 0, hl);
		} else {
			return text_result(a, 0, 0, 0x10, hl);
		}
	}

	/* .tx_end: TX_END and the symbol path share the end-of-line test */
	if (hTextLineLength && hTextLineCurPos == hTextLineLength)
		end_of_line(hl);
	return text_result(0, 0, 0, 0, hl);
}

uint16_t SetupText(uint8_t d, uint8_t e)
{
	wcd04 = (uint8_t)(d - 1);
	hffa8 = e;
	InitTextFormat();
	hffb0 = 0;
	hffa9 = 0;
	wTilePatternSelector = 0x88;
	wTilePatternSelectorCorrection = 0x80;
	for (uint16_t i = 0xc600; i != 0xc700; i++) gb_write8(i, 0);
	return 0xc600;
}

void InitTextPrinting(uint8_t d, uint8_t e)
{
	hTextHorizontalAlign = d;
	hTextLineLength = 0;
	wCurTextLine = 0;
	uint16_t bg = DECoordToBGMap0Address(d, e);
	hTextBGMap0Address = (uint8_t)bg;
	gb_write8(0xffabu, (uint8_t)(bg >> 8));
	InitTextFormat();
	wHalfWidthPrintState = 0;
}

void InitTextPrintingInTextbox(uint8_t a, uint8_t d, uint8_t e)
{
	InitTextPrinting(d, e);
	hTextLineLength = a;
}

static void process_text_core(uint16_t *hl)
{
	InitTextFormat();
	uint8_t a;
	while ((a = gb_read8((*hl)++)) != 0) {
		if (a >= TX_CTRL_START && a < TX_CTRL_END) {
			/* hl stays in a register across the asm's call, so whatever the
			 * handler leaves there -- past any payload byte it consumed -- is
			 * where the next character is read from. */
			*hl = ProcessSpecialTextCharacter(a, *hl).hl;
			continue;
		}
		uint8_t e = a;
		uint8_t d = gb_read8(*hl);
		uint8_t carry = ClassifyTextCharacterPair(&d, &e);
		if (carry & 0x10) (*hl)++;
		Func_22ca(d, e);
		*hl = ProcessSpecialTextCharacter(0, *hl).hl;
	}
	TerminateHalfWidthText(0, 0, *hl);
}

void ProcessText(uint16_t *hl)
{
	process_text_core(hl);
}

void InitTextPrinting_ProcessText(uint16_t *hl)
{
	uint8_t d = gb_read8(*hl); (*hl)++;
	uint8_t e = gb_read8(*hl); (*hl)++;
	InitTextPrinting(d, e);
	process_text_core(hl);
}

CopyTextResult CopyTextData(uint8_t a, uint16_t hl, uint16_t de)
{
	wTextMaxLength = a;

	uint8_t half = gb_read8(hl) == TX_HALFWIDTH;
	/* the half-width branch pads with an ascii space, the full-width one with its
	 * own space tile; `add a` doubling the budget is 8-bit, so it wraps */
	uint8_t fill = half ? ' ' : FW_SPACE;
	uint8_t d = half ? (uint8_t)(a * 2u) : a;
	uint16_t src = hl;
	uint16_t dst = de;
	uint8_t e = 0;
	int truncated = 0;

	for (;;) {
		uint8_t ch = gb_read8(src);

		if (!ch)
			break;
		src++;
		gb_write8(dst++, ch);
		/* a plain control character is copied but neither counts towards e nor
		 * spends budget: the asm jumps straight back to .loop */
		if (ch >= TX_CTRL_START && ch < TX_CTRL_END)
			continue;

		uint8_t pair_e = ch;
		uint8_t pair_d = gb_read8(src);

		if (ClassifyTextCharacterPair(&pair_d, &pair_e) & 0x10) {
			gb_write8(dst++, gb_read8(src));
			src++;
		}
		e++;
		if (--d == 0) {
			gb_write8(dst, 0); /* TX_END */
			truncated = 1;
			break;
		}
	}

	if (!truncated) {
		/* pad out the rest of the budget, then terminate. The asm brackets this
		 * with push hl / pop hl, so the exit pointer is the pre-fill one. */
		uint16_t end = dst;

		do {
			gb_write8(end++, fill);
		} while (--d);
		gb_write8(end, 0);
	}
	return (CopyTextResult){e, 0, e, dst};
}
