#include "home/text_box.h"

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "mem.h"
#include "ppu.h"

#define TX_SYMBOL 0x05
#define TX_HALF2FULL 0x07
#define TX_END 0x00
#define SYM_BOX_TOP_L 0x18
#define SYM_BOX_TOP_R 0x19
#define SYM_BOX_TOP 0x1c
#define FW_SPACE 0x70
#define CONSOLE_CGB 0x02

void SafeCopyDataDEtoHL(uint16_t *de, uint16_t *hl, uint8_t c)
{
	uint32_t count = c ? c : 0x100;
	uint16_t source = *de;
	uint16_t destination = *hl;

	do {
		gb_write8(destination++, gb_read8(source++));
	} while (--count);

	*de = source;
	*hl = destination;
}

uint16_t DECoordToBGMap0Address(uint8_t d, uint8_t e)
{
	uint16_t offset = (uint16_t)((uint16_t)e * TILEMAP_W + d);

	return (uint16_t)(0x9800u + offset);
}

void AdjustCoordinatesForBGScroll(uint8_t *d, uint8_t *e)
{
	uint8_t x = (uint8_t)((hSCX >> 3) & 0x1f);
	uint8_t y = (uint8_t)((hSCY >> 3) & 0x1f);

	*d = (uint8_t)(*d + x);
	*e = (uint8_t)(*e + y);
}

void CopyLine(uint16_t *hl, uint8_t a, uint8_t b, uint8_t d, uint8_t e)
{
	uint16_t destination = *hl;
	uint8_t middle_raw = (uint8_t)(b - 2);
	uint32_t middle = middle_raw ? middle_raw : 0x100;

	gb_write8(destination++, d);
	do {
		gb_write8(destination++, a);
	} while (--middle);
	gb_write8(destination++, e);

	*hl = (uint16_t)(*hl + TILEMAP_W);
}

static void draw_line(uint16_t *hl, uint8_t middle, uint8_t left, uint8_t right,
	uint8_t width)
{
	CopyLine(hl, middle, width, left, right);
}

void ContinueDrawingTextBoxDMGorSGB(uint16_t *hl, uint8_t a, uint8_t b,
	uint8_t c, uint8_t d, uint8_t e)
{
	(void)a;
	(void)d;
	(void)e;
	uint8_t raw = (uint8_t)(c - 2u);
	uint32_t count = raw ? raw : 0x100u;
	do {
		draw_line(hl, 0, 0x1e, 0x1f, b);
	} while (--count);
	draw_line(hl, 0x1d, 0x1a, 0x1b, b);
}

void DrawRegularTextBoxDMG(uint16_t *hl, uint8_t a, uint8_t b, uint8_t c,
	uint8_t d, uint8_t e)
{
	*hl = DECoordToBGMap0Address(d, e);
	draw_line(hl, 0x1c, 0x18, 0x19, b);
	ContinueDrawingTextBoxDMGorSGB(hl, a, b, c, d, e);
}

void DrawRegularTextBox(uint16_t *hl, uint8_t a, uint8_t b, uint8_t c,
	uint8_t d, uint8_t e)
{
	if (wConsole == CONSOLE_CGB)
		DrawRegularTextBoxCGB(hl, a, b, c, d, e);
	else
		DrawRegularTextBoxDMG(hl, a, b, c, d, e);
}

void ContinueDrawingTextBoxCGB(uint16_t *hl, uint8_t a, uint8_t b, uint8_t c,
	uint8_t d, uint8_t e)
{
	(void)a;
	(void)d;
	(void)e;
	uint8_t raw = (uint8_t)(c - 2u);
	uint32_t count = raw ? raw : 0x100u;
	do {
		uint16_t row = *hl;
		draw_line(hl, 0, 0x1e, 0x1f, b);
		*hl = row;
		hBankVRAM = 1;
		gb_write8(0xff4f, 1);
		/* asm: ld e,a / ld d,a / xor a -- the frame type is the two BORDER attrs and
		 * the middle of the row is filled with 0, not with the frame type. */
		draw_line(hl, 0, wTextBoxFrameType, wTextBoxFrameType, b);
		hBankVRAM = 0;
		gb_write8(0xff4f, 0);
	} while (--count);
	/* The bottom border goes through CopyCurrentLineTilesAndAttrCGB, which falls into
	 * CopyCurrentLineAttrCGB -- and that one has no `xor a`, so unlike a body row the
	 * whole bottom row's attributes are the frame type, not just its two borders. */
	CopyCurrentLineTilesAndAttrCGB(hl, 0x1d, b, 0x1a, 0x1b);
}

void DrawRegularTextBoxCGB(uint16_t *hl, uint8_t a, uint8_t b, uint8_t c,
	uint8_t d, uint8_t e)
{
	*hl = DECoordToBGMap0Address(d, e);
	CopyCurrentLineTilesAndAttrCGB(hl, 0x1c, b, 0x18, 0x19);
	ContinueDrawingTextBoxCGB(hl, a, b, c, d, e);
}

void CopyCurrentLineTilesAndAttrCGB(uint16_t *hl, uint8_t a, uint8_t b,
	uint8_t d, uint8_t e)
{
	uint16_t row = *hl;
	CopyLine(hl, a, b, d, e);
	*hl = row;
	CopyCurrentLineAttrCGB(hl, a, b, d, e);
}

void CopyCurrentLineAttrCGB(uint16_t *hl, uint8_t a, uint8_t b,
	uint8_t d, uint8_t e)
{
	(void)a;
	(void)d;
	(void)e;
	hBankVRAM = 1;
	gb_write8(0xff4f, 1);
	CopyLine(hl, wTextBoxFrameType, b, wTextBoxFrameType, wTextBoxFrameType);
	hBankVRAM = 0;
	gb_write8(0xff4f, 0);
}

/* Draws a b x c box at de whose top border carries the text labelled by hl.
 * The SGB colorisation tail (ColorizeTextBoxSGB) is dropped along with the rest of
 * the SGB path, as DrawRegularTextBoxSGB and AttrBlkPacket_TextBox already are. */
void DrawLabeledTextBox(uint16_t *hl, uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	uint16_t label = wLabeledTextBoxTopBorder_ADDR;

	gb_write8(label++, TX_SYMBOL);
	gb_write8(label++, SYM_BOX_TOP_L);
	gb_write8(label++, FW_SPACE);

	CopyTextResult copied = CopyText(*hl, label);
	TextLength length = GetTextLengthInTiles((uint16_t)(wLabeledTextBoxTopBorder_ADDR + 3u));

	/* GetTextLengthInTiles preserves de, so the asm's `ld l, e / ld h, d` picks up
	 * CopyText's exit de -- the terminator it just wrote, not its source pointer. */
	label = (uint16_t)((uint16_t)copied.d << 8 | copied.e);
	gb_write8(label++, TX_HALF2FULL);
	gb_write8(label++, FW_SPACE);

	/* The `pop de` here pops the bc that was pushed, so d is the caller's width.
	 * The subtraction is 8-bit, and the asm skips the run entirely when it is 0. */
	uint8_t remaining = (uint8_t)(b - length.b - 4u);

	if (remaining) {
		do {
			gb_write8(label++, TX_SYMBOL);
			gb_write8(label++, SYM_BOX_TOP);
		} while (--remaining);
	}
	gb_write8(label++, TX_SYMBOL);
	gb_write8(label++, SYM_BOX_TOP_R);
	gb_write8(label, TX_END);

	InitTextPrinting(d, e);

	uint16_t text = wLabeledTextBoxTopBorder_ADDR;

	ProcessText(&text);

	if (wConsole == CONSOLE_CGB) {
		*hl = DECoordToBGMap0Address(d, e);
		CopyCurrentLineAttrCGB(hl, a, b, d, e);
		e++;
		ContinueDrawingTextBoxCGB(hl, a, b, c, d, e);
		return;
	}
	e++;
	*hl = DECoordToBGMap0Address(d, e);
	ContinueDrawingTextBoxDMGorSGB(hl, a, b, c, d, e);
}
