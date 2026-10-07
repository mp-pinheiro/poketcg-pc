/* >>> part SYM_BOX_TOP_L */
#define SYM_BOX_TOP_L 0x18u
/* <<< part SYM_BOX_TOP_L */
/* >>> part SYM_BOX_TOP_R */
#define SYM_BOX_TOP_R 0x19u
/* <<< part SYM_BOX_TOP_R */
/* >>> part SYM_BOX_TOP */
#define SYM_BOX_TOP 0x1cu
/* <<< part SYM_BOX_TOP */
/* >>> part FW_SPACE */
#define FW_SPACE 0x70u
/* <<< part FW_SPACE */
/* >>> part SYM_BOX_BOTTOM */
#define SYM_BOX_BOTTOM 0x1du
/* <<< part SYM_BOX_BOTTOM */
/* --- factory ContinueDrawingTextBoxDMGorSGB */
/* --- factory DrawRegularTextBoxDMG */
/* === part draw_line */
/* >>> factory ContinueDrawingTextBoxDMG */
void ContinueDrawingTextBoxDMG(uint16_t *hl, uint8_t a, uint8_t b,
	uint8_t c, uint8_t d, uint8_t e)
{
	(void)a;
	(void)d;
	(void)e;
	uint8_t raw = (uint8_t)(c - 2u);
	uint32_t count = raw ? raw : 0x100u;
	do {
		draw_line(hl, 0u, 0x1eu, 0x1fu, b);
	} while (--count);
	draw_line(hl, 0x1du, 0x1au, 0x1bu, b);
}
/* <<< factory ContinueDrawingTextBoxDMG */
/* >>> factory DrawRegularTextBox */
void DrawRegularTextBox(uint16_t *hl, uint8_t a, uint8_t b, uint8_t c,
	uint8_t d, uint8_t e)
{
	if (wConsole == CONSOLE_CGB) {
		DrawRegularTextBoxCGB(hl, a, b, c, d, e);
		return;
	}
	*hl = DECoordToBGMap0Address(d, e);
	draw_line(hl, SYM_BOX_TOP, SYM_BOX_TOP_L, SYM_BOX_TOP_R, b);
	ContinueDrawingTextBoxDMG(hl, a, b, c, d, e);
}
/* <<< factory DrawRegularTextBox */
/* >>> factory ContinueDrawingTextBoxCGB */
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
	CopyCurrentLineTilesAndAttrCGB(hl, 0x1du, b, 0x1au, 0x1bu);
}
/* <<< factory ContinueDrawingTextBoxCGB */
/* >>> factory DrawLabeledTextBox */
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
	ContinueDrawingTextBoxDMG(hl, a, b, c, d, e);
}
/* <<< factory DrawLabeledTextBox */
