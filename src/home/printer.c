#include "home/printer.h"

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"

#include "home/process_text.h"
#include "generated/wram.h"

#include "home/switch_sram.h"
#include "home/process_text.h"
#include "generated/wram.h"

#include "generated/sram.h"
#include "generated/wram.h"

#include "home/printer.h"
#include "generated/wram.h"

#include "generated/hram.h"

#include "home/printer.h"
#include "mem.h"

#include "home/printer.h"
#define PRINTERPKT_DATA 0x04u
#define TRUE 0x01u
#define SGFXBUFFER5_ADDR 0xB400u

#include "generated/wram.h"
#include "home/menus.h"
#include "home/process_text.h"
#include "home/bg_map.h"
#include "home/core.h"
#define SYM_CROSS 0x2Du

#include "home/menus.h"
#define PleaseMakeSureToTurnGameBoyPrinterOffText 0x027bu
/* <<< factory statics */

#define rSB 0xFF01u
#define rSC 0xFF02u
#define SC_INTERNAL 0x01u
#define SC_START 0x80u

SendNextPrinterPacketByteResult SendNextPrinterPacketByte(void)
{
	uint16_t ptr = (uint16_t)(gb_read8(wSerialDataPtr_ADDR) |
				   (gb_read8((uint16_t)(wSerialDataPtr_ADDR + 1u)) << 8));
	uint8_t byte = gb_read8(ptr);
	uint16_t advanced = (uint16_t)(ptr + 1u);
	gb_write8((uint16_t)(wSerialDataPtr_ADDR + 1u), (uint8_t)(advanced >> 8));
	gb_write8(wSerialDataPtr_ADDR, (uint8_t)advanced);

	uint16_t sum = (uint16_t)(gb_read8(wPrinterPacketChecksum_ADDR) + byte);
	gb_write8(wPrinterPacketChecksum_ADDR, (uint8_t)sum);
	uint8_t hi = (uint8_t)(gb_read8((uint16_t)(wPrinterPacketChecksum_ADDR + 1u)) +
				(sum > 0xFFu ? 1u : 0u));
	gb_write8((uint16_t)(wPrinterPacketChecksum_ADDR + 1u), hi);

	SendByteThroughSerialData(byte);
	return (SendNextPrinterPacketByteResult){(uint8_t)(advanced >> 8), byte};
}

void SendByteThroughSerialData(uint8_t a)
{
	gb_write8(rSB, a);
	gb_write8(rSC, SC_INTERNAL);
	gb_write8(rSC, (uint8_t)(SC_START | SC_INTERNAL));
}

static void increment_sequence(void)
{
	gb_write8(wPrinterPacketSequence_ADDR, (uint8_t)(gb_read8(wPrinterPacketSequence_ADDR) + 1u));
}

static ExecutePrinterPacketSequenceResult send_checksum_byte(uint8_t byte, uint8_t d, uint8_t e)
{
	SendByteThroughSerialData(byte);
	increment_sequence();
	return (ExecutePrinterPacketSequenceResult){0x81u, d, e};
}

static ExecutePrinterPacketSequenceResult send_rest_of_data_section(void)
{
	SendNextPrinterPacketByteResult r = SendNextPrinterPacketByte();

	uint8_t lo = gb_read8(wPrinterPacketDataSize_ADDR);
	gb_write8(wPrinterPacketDataSize_ADDR, (uint8_t)(lo - 1u));
	if (lo == 0) {
		uint8_t hi = gb_read8((uint16_t)(wPrinterPacketDataSize_ADDR + 1u));
		gb_write8((uint16_t)(wPrinterPacketDataSize_ADDR + 1u), (uint8_t)(hi - 1u));
	}

	uint8_t remaining = (uint8_t)(gb_read8(wPrinterPacketDataSize_ADDR) |
				       gb_read8((uint16_t)(wPrinterPacketDataSize_ADDR + 1u)));
	if (remaining == 0) {
		increment_sequence();
		return (ExecutePrinterPacketSequenceResult){0, r.d, r.e};
	}
	return (ExecutePrinterPacketSequenceResult){remaining, r.d, r.e};
}

ExecutePrinterPacketSequenceResult ExecutePrinterPacketSequence(uint8_t a, uint8_t d, uint8_t e)
{
	switch (a) {
	case 1:
	case 2:
	case 3:
	case 4:
	case 5: {
		SendNextPrinterPacketByteResult r = SendNextPrinterPacketByte();
		increment_sequence();
		return (ExecutePrinterPacketSequenceResult){0x81u, r.d, r.e};
	}
	case 6: {
		increment_sequence();
		uint8_t lo = gb_read8(wPrinterPacketDataSize_ADDR);
		uint8_t hi = gb_read8((uint16_t)(wPrinterPacketDataSize_ADDR + 1u));
		if (lo != 0 || hi != 0) {
			gb_write8(wSerialDataPtr_ADDR, gb_read8(wPrinterPacketDataPtr_ADDR));
			gb_write8((uint16_t)(wSerialDataPtr_ADDR + 1u),
				  gb_read8((uint16_t)(wPrinterPacketDataPtr_ADDR + 1u)));
			return send_rest_of_data_section();
		}
		increment_sequence();
		return send_checksum_byte(gb_read8(wPrinterPacketChecksum_ADDR), d, e);
	}
	case 7:
		return send_rest_of_data_section();
	case 8:
		return send_checksum_byte(gb_read8(wPrinterPacketChecksum_ADDR), d, e);
	case 9:
		return send_checksum_byte(gb_read8((uint16_t)(wPrinterPacketChecksum_ADDR + 1u)), d, e);
	case 10:
		return send_checksum_byte(0, d, e);
	case 11:
		gb_write8(wSerialTransferData_ADDR, gb_read8(rSB));
		return send_checksum_byte(0, d, e);
	case 12:
	default:
		gb_write8(wPrinterStatus_ADDR, gb_read8(rSB));
		gb_write8(wPrinterPacketSequence_ADDR, 0);
		return (ExecutePrinterPacketSequenceResult){0, d, e};
	}
}

/* >>> factory Func_1a14b */
Func_1a14bResult Func_1a14b(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)a;
	wce9d = 0x01u;
	return (Func_1a14bResult){
		.a = 0x01u,
		.f = (uint8_t)((f & 0x80u) | 0x10u),
		.b = b,
		.c = c,
		.d = d,
		.e = e,
		.hl = hl,
	};
}
/* <<< factory Func_1a14b */

/* >>> factory Func_1a025 */
void Func_1a025(void)
{
	SetupText(0x40u, 0xBFu);
	wTilePatternSelector = 0xA4u;
	wTilePatternSelectorCorrection = 0x00u;
}
/* <<< factory Func_1a025 */

/* >>> factory ResetPrinterCommunicationSettings */
ResetPrinterCommunicationSettingsResult ResetPrinterCommunicationSettings(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)d;
	(void)e;
	(void)hl;
	BankswitchSRAM(wTempPrinterSRAM);
	DisableSRAM();
	uint16_t result_hl = SetupText(0x30u, 0xBFu);
	return (ResetPrinterCommunicationSettingsResult){
		.a = a,
		.f = f,
		.b = b,
		.c = c,
		.d = 0x30u,
		.e = 0xBFu,
		.hl = result_hl,
	};
}
/* <<< factory ResetPrinterCommunicationSettings */

/* >>> factory ClearPrinterGfxBuffer */
ClearPrinterGfxBufferResult ClearPrinterGfxBuffer(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)a;
	(void)f;
	(void)b;
	(void)c;
	(void)hl;
	uint16_t target = sGfxBuffer0_ADDR;
	uint16_t count = 0x0400u;
	do {
		gb_write8(target, 0u);
		target = (uint16_t)(target + 1u);
		count = (uint16_t)(count - 1u);
	} while (count != 0);
	gb_write8(wce9f_ADDR, 0u);
	return (ClearPrinterGfxBufferResult){
		.a = 0x00u,
		.f = 0x80u,
		.b = 0x00u,
		.c = 0x00u,
		.d = d,
		.e = e,
		.hl = target,
	};
}
/* <<< factory ClearPrinterGfxBuffer */

/* >>> factory GetPrinterContrastSerialData */
GetPrinterContrastSerialDataResult GetPrinterContrastSerialData(void)
{
	static const uint8_t contrast_level_data[5] = {0x00u, 0x20u, 0x40u, 0x60u, 0x7Fu};
	uint8_t level = wPrinterContrastLevel;
	uint8_t h_val = contrast_level_data[level];
	uint16_t hl = (uint16_t)(((uint16_t)h_val << 8) | 0xE4u);
	return (GetPrinterContrastSerialDataResult){level, hl};
}
/* <<< factory GetPrinterContrastSerialData */

/* >>> factory PrepareForPrinterCommunications */
PrepareForPrinterCommunicationsResult PrepareForPrinterCommunications(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	ResetSerial();
	wPrinterNumberLineFeeds = 0x10u;
	EnableSRAM();
	wPrinterContrastLevel = sPrinterContrastLevel;
	DisableSRAM();
	wTempPrinterSRAM = hBankSRAM;
	BankswitchSRAM(0x01u);
	EnableSRAM();
	ClearPrinterGfxBufferResult r = ClearPrinterGfxBuffer(a, f, b, c, d, e, hl);
	return (PrepareForPrinterCommunicationsResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory PrepareForPrinterCommunications */

/* >>> factory CheckDataCompression */
CheckDataCompressionResult CheckDataCompression(uint8_t c, uint16_t hl)
{
	uint16_t entry_hl = hl;
	uint8_t e = c;
	uint8_t a = c;
	uint8_t b;
	uint8_t d;
	uint8_t z_flag;

	if (a < 4u) {
		goto no_carry;
	}

	b = c;
	a = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	if (a != gb_read8(hl)) {
		goto literal_copy;
	}
	hl = (uint16_t)(hl + 1u);
	if (a != gb_read8(hl)) {
		goto literal_copy;
	}
	hl = (uint16_t)(hl + 1u);

	c = (uint8_t)(c - 3u);
	e = 3u;
	for (;;) {
		if (a != gb_read8(hl)) {
			z_flag = 0u;
			goto set_carry;
		}
		hl = (uint16_t)(hl + 1u);
		e = (uint8_t)(e + 1u);
		c = (uint8_t)(c - 1u);
		if (c == 0u) {
			z_flag = 1u;
			goto set_carry;
		}
		if (e & 0x20u) {
			z_flag = 0u;
			goto set_carry;
		}
	}

set_carry:
	return (CheckDataCompressionResult){a, e, (uint8_t)((z_flag ? 0x80u : 0u) | 0x10u), entry_hl};

literal_copy:
	hl = entry_hl;
	c = b;
	e = 1u;
	a = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	c = (uint8_t)(c - 1u);
	if (c == 0u) {
		goto no_carry;
	}
reset_same_value_count:
	d = 2u;
next_byte:
	e = (uint8_t)(e + 1u);
	c = (uint8_t)(c - 1u);
	if (c == 0u) {
		goto no_carry;
	}
	if (e & 0x80u) {
		goto no_carry;
	}
	if (a == gb_read8(hl)) {
		hl = (uint16_t)(hl + 1u);
		d = (uint8_t)(d - 1u);
		if (d != 0u) {
			goto next_byte;
		}
		e = (uint8_t)(e - 3u);
		goto no_carry;
	}
	a = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	goto reset_same_value_count;

no_carry:
	return (CheckDataCompressionResult){a, e, (uint8_t)(a == 0u ? 0x80u : 0u), entry_hl};
}
/* <<< factory CheckDataCompression */

/* >>> factory CompressDataForPrinterSerialTransfer */
CompressDataForPrinterSerialTransferResult CompressDataForPrinterSerialTransfer(void)
{
	uint16_t hl = SGFXBUFFER5_ADDR;
	uint16_t de = (uint16_t)(SGFXBUFFER5_ADDR + 0x280u);
	uint16_t remaining = 0x280u;

	for (;;) {
		uint8_t count = (remaining > 0xFFu) ? 0xFFu : (uint8_t)remaining;
		CheckDataCompressionResult r = CheckDataCompression(count, hl);
		uint8_t found = r.e;
		uint8_t carry = (uint8_t)(r.f & 0x10u) != 0u;

		if (carry) {
			gb_write8(de, (uint8_t)(((uint8_t)(found - 2u)) | 0x80u));
			de = (uint16_t)(de + 1u);
			gb_write8(de, gb_read8(hl));
			de = (uint16_t)(de + 1u);
			hl = (uint16_t)(hl + found);
		} else {
			gb_write8(de, (uint8_t)(found - 1u));
			de = (uint16_t)(de + 1u);
			for (uint8_t i = 0u; i < found; i++) {
				gb_write8(de, gb_read8(hl));
				hl = (uint16_t)(hl + 1u);
				de = (uint16_t)(de + 1u);
			}
		}

		remaining = (uint16_t)(remaining - found);
		if (remaining == 0u) {
			break;
		}
	}

	uint16_t hl_out = (uint16_t)(SGFXBUFFER5_ADDR + 0x280u);
	uint16_t bc_out = (uint16_t)(de - hl_out);
	return (CompressDataForPrinterSerialTransferResult){bc_out, hl_out, PRINTERPKT_DATA, TRUE};
}
/* <<< factory CompressDataForPrinterSerialTransfer */

/* >>> factory LoadCardInfoForPrinter */
void LoadCardInfoForPrinter(uint8_t b, uint8_t c, uint16_t *hl)
{
	uint16_t saved_hl = *hl;
	uint8_t x = (uint8_t)(wPrinterHorizontalOffset | 0x40u);
	uint8_t d = 3u;
	if (wPrintOnlyStarRarity == 0u) {
		uint16_t total = wPrinterTotalCardCount_ADDR;
		uint8_t total_count = gb_read8(total);
		total = (uint16_t)(total + 1u);
		total_count = (uint8_t)(total_count | gb_read8(total));
		if (total_count == 0u)
			DrawCardSymbol(d, x);
	}
	CopyCardNameAndLevel(14u, b, c, d, x);
	InitTextPrinting(d, x);
	uint16_t text = wDefaultText_ADDR;
	ProcessText(&text);
	x = (uint8_t)(wPrinterHorizontalOffset | 0x40u);
	uint8_t bg_column = x;
	uint8_t bg_row = 16u;
	WriteByteToBGMap0(SYM_CROSS, bg_row, bg_column);
	bg_row = (uint8_t)(bg_row + 1u);
	WriteTwoDigitNumberInTxSymbol_PadSpace(wPrinterCardCount, bg_row, bg_column, d, x, text);
	*hl = saved_hl;
}
/* <<< factory LoadCardInfoForPrinter */

/* >>> factory PrinterMenu_QuitPrint */
uint8_t PrinterMenu_QuitPrint(uint16_t w0)
{
	(void)w0;
	WaitResult result = DrawWideTextBox_WaitForInput(PleaseMakeSureToTurnGameBoyPrinterOffText);
	return result.f;
}
/* <<< factory PrinterMenu_QuitPrint */
