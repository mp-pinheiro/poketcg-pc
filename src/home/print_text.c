#include "home/print_text.h"

#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/process_text.h"
#include "home/duel.h"
#include "home/switch_rom.h"
#include "home/write_number.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/text_box.h"

/* HIGH(wOpponentDuelVariables), the value hWhoseTurn carries on the opponent's turn. */
#define OPPONENT_TURN ((uint8_t)(wOpponentDuelVariables_ADDR >> 8))

static uint16_t text_header(void)
{
	return (uint16_t)(wTextHeader1_ADDR + (uint8_t)(wWhichTextHeader * 5u));
}

uint16_t GetTextOffsetFromTextID(uint16_t text_id)
{
	uint16_t index = (uint16_t)(text_id * 3u);
	uint16_t table = (uint16_t)(0x4000u + index);
	uint8_t lo;
	uint8_t hi;
	uint8_t bank_bits;

	BankswitchROM(0x0d);
	lo = gb_read8(table);
	table++;
	hi = gb_read8(table);
	table++;
	bank_bits = gb_read8(table);
	BankswitchROM((uint8_t)(0x0d + (bank_bits << 2) + (hi >> 6)));
	return (uint16_t)(0x4000u | ((uint16_t)(hi & 0x3fu) << 8) | lo);
}

uint16_t GetPointerToTextHeader(void)
{
	return text_header();
}

uint16_t ReadTextHeader(void)
{
	uint16_t header = text_header();
	uint8_t bank;
	uint16_t text;

	hJapaneseSyllabary = gb_read8(header++);
	wFontWidth = gb_read8(header++);
	bank = gb_read8(header++);
	BankswitchROM(bank);
	text = gb_read8(header++);
	text |= (uint16_t)gb_read8(header) << 8;
	return text;
}

/* print_text.asm:179-192. `push hl / call GetPointerToTextHeader / pop bc` puts the
 * entry pointer's halves in b/c, and the final `ld [hl], b` has no inc after it, so
 * exit hl is header+4. */
static TextHeaderWrite write_text_header(uint16_t text)
{
	uint16_t header = text_header();

	gb_write8(header++, hJapaneseSyllabary);
	gb_write8(header++, wFontWidth);
	gb_write8(header++, hBankROM);
	gb_write8(header++, (uint8_t)text);
	gb_write8(header, (uint8_t)(text >> 8));
	return (TextHeaderWrite){(uint8_t)(text >> 8), (uint8_t)text, header};
}

TextHeaderWrite WriteToTextHeader(uint16_t text)
{
	return write_text_header(text);
}

/* print_text.asm:197-201. The tail is `ld hl, wWhichTextHeader / inc [hl]`, so the
 * exit pointer is that address, not the header the write advanced through. */
TextHeaderWrite WriteToTextHeader_MoveToNext(uint16_t text)
{
	TextHeaderWrite out = write_text_header(text);

	wWhichTextHeader++;
	out.hl = wWhichTextHeader_ADDR;
	return out;
}

TextHeaderWrite ResetTxRam_WriteToTextHeader(uint16_t text)
{
	wWhichTextHeader = 0;
	wWhichTxRam2 = 0;
	wWhichTxRam3 = 0;
	hJapaneseSyllabary = 0x0f;
	return write_text_header(text);
}

/* Contract fields are b, c, d, e, hl. b is preserved on both paths; c and de are
 * preserved on the full-width path only, so they come in to be echoed back out. */
LeadingZerosResult TwoByteNumberToText_CountLeadingZeros(uint16_t value, uint8_t c, uint16_t de)
{
	/* `jp z` is a tail call, and PadSpace pushes and pops both bc and de. */
	if (wFontWidth == 0)
		return (LeadingZerosResult){c, de, TwoByteNumberToTxSymbol_PadSpace(value).hl};

	de = wStringBuffer_ADDR;
	TwoByteNumberToText(value, &de); /* leaves de on the TX_END slot, five bytes along */

	uint16_t hl = wStringBuffer_ADDR;

	c = 4;
	while (gb_read8(hl) == '0') {
		hl++;
		if (--c == 0)
			break;
	}
	return (LeadingZerosResult){c, de, hl};
}

/* Returns the asm's three live exit registers: a (the restored bank on the text-ID
 * path, 0 on the name paths), de backed up onto the terminator, and hl past it. */
CopyTextResult CopyText(uint16_t text_id, uint16_t de)
{
	if (!text_id) {
		if (hWhoseTurn == OPPONENT_TURN)
			return CopyOpponentName(de);
		return CopyPlayerName(de);
	}

	uint8_t saved = hBankROM;
	uint16_t hl = GetTextOffsetFromTextID(text_id);
	uint8_t a;

	do {
		a = gb_read8(hl++);
		gb_write8(de++, a);
	} while (a);
	BankswitchROM(saved);
	de--;
	/* `pop af` restores the saved bank into a, and BankswitchROM preserves it. */
	return (CopyTextResult){saved, (uint8_t)(de >> 8), (uint8_t)de, hl};
}

uint8_t CountLinesOfTextFromID(uint16_t text_id)
{
	uint8_t saved = hBankROM;
	uint16_t text = GetTextOffsetFromTextID(text_id);
	uint8_t lines = 0;
	uint8_t value;

	do {
		value = gb_read8(text++);
		if (value == 0)
			break;
		if (value >= 0x10)
			continue;
		if (value < 0x06) {
			text++;
			continue;
		}
		if (value == 0x0a)
			lines++;
	} while (1);
	BankswitchROM(saved);
	return (uint8_t)(lines + 1);
}

/* The asm stores to wTxRam2 and wTxRam2 + 1. wTxRam2_b is a separate symbol two bytes
 * along ($CE41), not the high half of this pair, so writing it would miss $CE40. */
void LoadTxRam2(uint16_t text_id)
{
	gb_write8(wTxRam2_ADDR, (uint8_t)text_id);
	gb_write8((uint16_t)(wTxRam2_ADDR + 1), (uint8_t)(text_id >> 8));
}

void LoadTxRam3(uint16_t value)
{
	gb_write8(wTxRam3_ADDR, (uint8_t)value);
	gb_write8((uint16_t)(wTxRam3_ADDR + 1), (uint8_t)(value >> 8));
}

static ProcessTextHeaderResult header_result(uint8_t a, uint8_t d, uint8_t e,
	uint8_t f, uint16_t hl)
{
	return (ProcessTextHeaderResult){a, d, e, f, hl};
}

/* Returns the 16-bit value held in the slot, not the slot address: the asm finishes
 * with `ld a, [hli] / ld h, [hl] / ld l, a`. The index doubling is an 8-bit `add a`,
 * so it wraps. */
uint16_t HandleTxRam2Or3(uint16_t de, uint16_t hl)
{
	uint8_t index = gb_read8(hl);

	gb_write8(hl, (uint8_t)(index + 1u));

	uint16_t slot = (uint16_t)(de + (uint8_t)(index * 2u));

	return (uint16_t)(gb_read8(slot) | (uint16_t)gb_read8((uint16_t)(slot + 1u)) << 8);
}

/* a and de fall out of the callee; hl is the buffer address the asm pushed and popped. */
CopyTextResult CopyPlayerNameOrTurnDuelistName(void)
{
	uint16_t de = wStringBuffer_ADDR;
	CopyTextResult result = hWhoseTurn == OPPONENT_TURN ? CopyOpponentName(de)
							   : CopyPlayerName(de);

	result.hl = de;
	return result;
}
CopyTextResult CopyTextData_FromTextID(uint8_t a, uint16_t hl, uint16_t de)
{
	uint8_t saved = hBankROM;
	uint16_t source = GetTextOffsetFromTextID(hl);
	CopyTextResult result = CopyTextData(a, source, de);

	BankswitchROM(saved);
	/* `pop af` puts the entry bank back in a, overriding CopyTextData's count. */
	result.a = saved;
	return result;
}

/* d and e are live on entry: the TX_END path hands d to TerminateHalfWidthText,
 * and both are preserved across every path that does not set them itself. */
ProcessTextHeaderResult ProcessTextHeader(uint8_t d, uint8_t e)
{
	uint16_t text = ReadTextHeader();
	uint8_t a = gb_read8(text++);
	if (!a) {
		if (wWhichTextHeader) {
			wWhichTextHeader--;
			return ProcessTextHeader(d, e);
		}

		ProcessTextResult ended = TerminateHalfWidthText(d, e, text);
		return header_result(ended.a, ended.d, ended.e, 0x10, ended.hl);
	}
	if (a >= 0x05 && a < 0x10) {
		ProcessTextResult special = ProcessSpecialTextCharacter(a, text);
		if (special.f & 0x10) {
			if (a == 0x0b) {
				WriteToTextHeader_MoveToNext(text);
				hJapaneseSyllabary = 0x0f;
				wFontWidth = 0;
				uint16_t ptr = HandleTxRam2Or3(wTxRam2_ADDR, wWhichTxRam2_ADDR);
				WriteToTextHeader(ptr ? GetTextOffsetFromTextID(ptr) : wDefaultText_ADDR);
				return ProcessTextHeader(d, e);
			}
			if (a == 0x0c) {
				WriteToTextHeader_MoveToNext(text);
				uint16_t ptr = HandleTxRam2Or3(wTxRam3_ADDR, wWhichTxRam3_ADDR);
				WriteToTextHeader(TwoByteNumberToText_CountLeadingZeros(ptr, 0, 0).hl);
				return ProcessTextHeader(d, e);
			}
			if (a == 0x09) {
				WriteToTextHeader_MoveToNext(text);
				uint16_t out = CopyPlayerNameOrTurnDuelistName().hl;
				if (gb_read8(wStringBuffer_ADDR) != 0x06)
					ProcessSpecialTextCharacter(0x07, out);
				WriteToTextHeader(out);
				return ProcessTextHeader(d, e);
			}
		}
		WriteToTextHeader(text);
		return header_result(special.a, d, e, 0, text);
	}
	e = a;
	d = gb_read8(text);

	uint8_t carry = ClassifyTextCharacterPair(&d, &e);
	if (carry & 0x10)
		text++;
	Func_22ca(d, e);
	ProcessSpecialTextCharacter(0, text);
	WriteToTextHeader(text);
	return header_result(0, d, e, 0, text);
}

ProcessTextHeaderResult ProcessTextFromID(uint16_t hl)
{
	uint8_t saved = hBankROM;
	uint16_t text = GetTextOffsetFromTextID(hl);
	ProcessText(&text);
	BankswitchROM(saved);
	return header_result(0, 0, 0, 0, text);
}

ProcessTextHeaderResult ProcessTextFromPointerToID(uint16_t hl)
{
	uint8_t lo = gb_read8(hl++);
	uint8_t hi = gb_read8(hl);
	if (!(lo | hi))
		return header_result(0, 0, 0, 0, hl);
	return ProcessTextFromID((uint16_t)(lo | (uint16_t)hi << 8));
}

ProcessTextHeaderResult InitTextPrinting_ProcessTextFromID(uint8_t d, uint8_t e, uint16_t hl)
{
	InitTextPrinting(d, e);
	return ProcessTextFromID(hl);
}

ProcessTextHeaderResult InitTextPrinting_ProcessTextFromPointerToID(uint8_t d, uint8_t e, uint16_t hl)
{
	InitTextPrinting(d, e);
	return ProcessTextFromPointerToID(hl);
}

#define TEXT_SPEED_3 2u
#define PAD_B        0x02u

TextResult PlaceTextItems(uint16_t hl)
{
	uint8_t d;

	for (;;) {
		d = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (d & 0x80u)
			return (TextResult){0, 0, 0, d, 0, hl};
		uint8_t e = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		InitTextPrinting(d, e);
		(void)ProcessTextFromPointerToID(hl);
		hl = (uint16_t)(hl + 2u);
	}
}

static TextResult print_text_body(uint16_t text, uint8_t d, uint8_t e)
{
	uint8_t b = 0;
	uint8_t a = 0;
	uint16_t hl = ResetTxRam_WriteToTextHeader(text).hl;

	for (;;) {
		b = hKeysHeld;
		uint8_t speed = (uint8_t)(wTextSpeed + 1u);
		if (speed >= (uint8_t)(TEXT_SPEED_3 + 1u) || !(b & PAD_B)) {
			do {
				speed = (uint8_t)(speed - 1u);
				if (speed == 0u)
					break;
				DoFrame();
			} while (1);
		}
		ProcessTextHeaderResult ph = ProcessTextHeader(d, e);
		a = ph.a;
		d = ph.d;
		e = ph.e;
		hl = ph.hl;
		if (ph.f & 0x10u)
			break;
	}
	return (TextResult){a, b, 0, d, e, hl};
}

TextResult PrintText(uint16_t hl, uint8_t d, uint8_t e)
{
	if (hl == 0) {
		return print_text_body(wDefaultText_ADDR, d, e);
	}
	uint8_t saved = hBankROM;
	uint16_t text = GetTextOffsetFromTextID(hl);
	TextResult r = print_text_body(text, d, e);
	BankswitchROM(saved);
	r.a = saved;
	return r;
}

TextResult PrintTextNoDelay(uint16_t hl, uint8_t d, uint8_t e)
{
	uint8_t saved = hBankROM;
	uint16_t text = GetTextOffsetFromTextID(hl);

	ResetTxRam_WriteToTextHeader(text);
	uint16_t hout = 0;
	for (;;) {
		ProcessTextHeaderResult ph = ProcessTextHeader(d, e);
		d = ph.d;
		e = ph.e;
		hout = ph.hl;
		if (ph.f & 0x10u)
			break;
	}
	BankswitchROM(saved);
	return (TextResult){saved, 0, 0, d, e, hout};
}

TextResult DrawTextReadyLabeledOrRegularTextBox(uint16_t hl)
{
	uint8_t b = 20;
	uint8_t c = 6;
	uint8_t d = 0;
	uint8_t e = 12;

	AdjustCoordinatesForBGScroll(&d, &e);
	if (wIsTextBoxLabeled) {
		uint16_t label = (uint16_t)(gb_read8(wTextBoxLabel_ADDR)
			| (uint16_t)gb_read8((uint16_t)(wTextBoxLabel_ADDR + 1u)) << 8);
		DrawLabeledTextBox(&label, (uint8_t)label, b, c, d, e);
	} else {
		uint16_t box = hl;
		DrawRegularTextBox(&box, wIsTextBoxLabeled, b, c, d, e);
		EnableLCD();
	}
	d = 1;
	e = 14;
	AdjustCoordinatesForBGScroll(&d, &e);
	InitTextPrintingInTextbox(19, d, e);
	return (TextResult){19, 0, 0, d, e, hl};
}
