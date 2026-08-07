#include "home/print_text.h"

#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/process_text.h"
#include "home/switch_rom.h"
#include "mem.h"
#include "home/write_number.h"

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

static uint16_t write_text_header(uint16_t text)
{
	uint16_t header = text_header();

	gb_write8(header++, hJapaneseSyllabary);
	gb_write8(header++, wFontWidth);
	gb_write8(header++, hBankROM);
	gb_write8(header++, (uint8_t)text);
	gb_write8(header, (uint8_t)(text >> 8));
	return header;
}

uint16_t WriteToTextHeader(uint16_t text)
{
	return write_text_header(text);
}

uint16_t WriteToTextHeader_MoveToNext(uint16_t text)
{
	uint16_t header = write_text_header(text);
	wWhichTextHeader++;
	return header;
}

uint16_t ResetTxRam_WriteToTextHeader(uint16_t text)
{
	wWhichTextHeader = 0;
	wWhichTxRam2 = 0;
	wWhichTxRam3 = 0;
	hJapaneseSyllabary = 0x0f;
	return write_text_header(text);
}

uint8_t TwoByteNumberToText_CountLeadingZeros(uint16_t value, uint16_t *text)
{
	if (wFontWidth == 0) {
		uint8_t first = 0;
		TwoByteNumberToTxSymbol_PadSpace(value);
		while (first < 4 && (gb_read8((uint16_t)(wStringBuffer_ADDR + first * 2u + 1u)) == 0 ||
			gb_read8((uint16_t)(wStringBuffer_ADDR + first * 2u + 1u)) == 0x20))
			first++;
		*text = (uint16_t)(wStringBuffer_ADDR + first * 2u);
		return first == 4 ? 0 : gb_read8((uint16_t)(wStringBuffer_ADDR + first * 2u + 1u));
	}

	uint16_t destination = wStringBuffer_ADDR;
	TwoByteNumberToText(value, &destination);
	uint16_t p = wStringBuffer_ADDR;
	uint8_t count = 4;
	while (count && gb_read8(p) == '0') {
		p++;
		count--;
	}
	*text = p;
	return count;
}
uint16_t CopyText(uint16_t text_id, uint16_t *destination)
{
	uint8_t saved = hBankROM;
	uint16_t source = GetTextOffsetFromTextID(text_id);
	uint16_t dst = *destination;
	uint8_t value;

	do {
		value = gb_read8(source++);
		gb_write8(dst++, value);
	} while (value);
	BankswitchROM(saved);
	*destination = (uint16_t)(dst - 1u);
	return source;
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

