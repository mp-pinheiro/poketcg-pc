/* >>> part includes */
#include "home/print_text.h"

#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/rom.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/process_text.h"
#include "home/duel.h"
#include "home/switch_rom.h"
#include "home/write_number.h"
#include "home/frames.h"
#include "home/menus.h"
#include "home/lcd.h"
#include "home/text_box.h"
/* <<< part includes */
/* >>> factory GetTextOffsetFromTextID */
uint16_t GetTextOffsetFromTextID(uint16_t text_id)
{
	uint16_t index = (uint16_t)(text_id * 3u);
	uint16_t table = (uint16_t)(TextOffsets_ADDR + index);
	uint8_t lo;
	uint8_t hi;
	uint8_t bank_bits;

	BankswitchROM(TextOffsets_BANK);
	lo = gb_read8(table);
	table++;
	hi = gb_read8(table);
	table++;
	bank_bits = gb_read8(table);
	BankswitchROM((uint8_t)(TextOffsets_BANK + (bank_bits << 2) + (hi >> 6)));
	return (uint16_t)(0x4000u | ((uint16_t)(hi & 0x3fu) << 8) | lo);
}
/* <<< factory GetTextOffsetFromTextID */
/* >>> factory TwoByteNumberToText_CountLeadingZeros */
/* Contract fields are b, c, d, e, hl. b is preserved on both paths; c and de are
 * preserved on the full-width path only, so they come in to be echoed back out. */
LeadingZerosResult TwoByteNumberToText_CountLeadingZeros(uint16_t value, uint8_t c, uint16_t de)
{
	/* `jp z` is a tail call, and TwoByteNumberToTxSymbol_TrimLeadingZeros pushes and pops both bc and de. */
	if (wFontWidth == 0)
		return (LeadingZerosResult){c, de, TwoByteNumberToTxSymbol_TrimLeadingZeros(value).hl};

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
/* <<< factory TwoByteNumberToText_CountLeadingZeros */
