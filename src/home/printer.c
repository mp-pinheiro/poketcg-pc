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

#include "generated/sram.h"
#include "generated/wram.h"
#include "home/bg_map.h"
#include "home/core.h"
#include "home/printer.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "home/text_box.h"
#define CARDPAGETYPE_NOT_PLAY_AREA 0x00u
#define RetreatWeakResistData 0x4000u
#define SYM_SPACE 0x00u
#define SYM_No 0x01u
#define TYPE_ENERGY 0x08u

#include "home/menus.h"
#include "home/lcd.h"
#include "home/load_animation.h"
#include "home/sprite_vblank.h"
#define SCENE_GAMEBOY_PRINTER_TRANSMITTING 0x11u
#define NowPrintingPleaseWaitText 0x0195u

#include "home/printer.h"
#include "home/frames.h"
#include "generated/wram.h"
#include "generated/hram.h"
#define PAD_B 0x02u
#define FALSE 0x00u
#define PRINTERPKT_INIT 0x01u
#define PRINTERPKT_NUL 0x0Fu
#define PRINTER_STATUS_BUSY 0x01u
#define PRINTER_STATUS_PRINTING 0x03u

#include "home/printer.h"
#define PrinterIsNotConnectedText 0x00d7u

#include "generated/wram.h"
#include "home/menus.h"
#include "home/printer.h"
#define PRINTER_ERROR_BATTERIES_LOST_CHARGE 0x07u
#define PRINTER_ERROR_CABLE_PRINTER_SWITCH 0x06u
#define PRINTER_ERROR_PAPER_JAMMED 0x05u
#define BatteriesHaveLostTheirChargeText 0x00d8u
#define CheckCableOrPrinterSwitchText 0x00dau
#define PrinterPacketErrorText 0x00dbu
#define PrinterPaperIsJammedText 0x00d9u
#define PrintingWasInterruptedText 0x00dcu

#define PRINTERPKT_PRINT_INSTRUCTION 0x02u
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

/* >>> factory DrawBottomCardInfoInSRAMGfxBuffer0 */
void DrawBottomCardInfoInSRAMGfxBuffer0(void)
{
	Func_1a025();
	gb_write8(wCardPageType_ADDR, CARDPAGETYPE_NOT_PLAY_AREA);
	uint16_t hl = sGfxBuffer0_ADDR;
	uint8_t c = 9u;
	while (c != 0u) {
		CopyLine(&hl, SYM_SPACE, 20u, 0x36u, 0x37u);
		c = (uint8_t)(c - 1u);
	}
	CopyLine(&hl, 0x35u, 20u, 0x32u, 0x33u);
	if (gb_read8(wLoadedCard1Type_ADDR) < TYPE_ENERGY) {
		(void)PlaceTextItems(RetreatWeakResistData);
		DisplayCardPage_PokemonOverview();
		WriteByteToBGMap0(SYM_No, 15u, 72u);
		WriteOneByteNumberInTxSymbol_PadSpace(gb_read8(wLoadedCard1PokedexNumber_ADDR), 15u, 73u, 0u, 0u, 0u);
		return;
	}
	(void)SetNoLineSeparation();
	InitTextPrintingInTextbox(19u, 1u, 66u);
	(void)ProcessTextFromPointerToID(wLoadedCard1NonPokemonDescription_ADDR);
	(void)SetOneLineSeparation();
}
/* <<< factory DrawBottomCardInfoInSRAMGfxBuffer0 */

/* >>> factory ShowPrinterTransmitting */
void ShowPrinterTransmitting(void)
{
	SetSpriteAnimationsAsVBlankFunction();
	(void)LoadScene(SCENE_GAMEBOY_PRINTER_TRANSMITTING, 0u, 0u, 0u, 0u, 0u, 0u);
	(void)DrawWideTextBox_PrintText(NowPrintingPleaseWaitText);
	EnableLCD();
}
/* <<< factory ShowPrinterTransmitting */

/* >>> factory SendPrinterPacket */
/* printer.asm:5-77. The hardware serial ISR normally advances the 12-state
 * printer sequence asynchronously. The PC runtime executes that already-ported
 * state machine synchronously; wSerialTransferData/wPrinterStatus provide the
 * injected device responses at states 11/12. */
SendPrinterPacketResult SendPrinterPacket(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t device_response = gb_read8(wSerialTransferData_ADDR);
	uint8_t status_response = gb_read8(wPrinterStatus_ADDR);
	gb_write8(wPrinterPacketPreamble_ADDR, 0x88u);
	gb_write8((uint16_t)(wPrinterPacketPreamble_ADDR + 1u), 0x33u);
	gb_write8(wPrinterPacketInstructions_ADDR, d);
	gb_write8((uint16_t)(wPrinterPacketInstructions_ADDR + 1u), e);
	gb_write8(wPrinterPacketDataSize_ADDR, c);
	gb_write8((uint16_t)(wPrinterPacketDataSize_ADDR + 1u), b);
	gb_write8(wPrinterPacketDataPtr_ADDR, (uint8_t)hl);
	gb_write8((uint16_t)(wPrinterPacketDataPtr_ADDR + 1u), (uint8_t)(hl >> 8));
	gb_write8(wPrinterPacketChecksum_ADDR, 0x45u);
	gb_write8((uint16_t)(wPrinterPacketChecksum_ADDR + 1u), 0xFFu);
	gb_write8(wSerialDataPtr_ADDR, (uint8_t)wPrinterPacket_ADDR);
	gb_write8((uint16_t)(wSerialDataPtr_ADDR + 1u), (uint8_t)(wPrinterPacket_ADDR >> 8));
	(void)Func_0e8e();
	gb_write8(wPrinterPacketSequence_ADDR, 1u);
	SendNextPrinterPacketByteResult first = SendNextPrinterPacketByte();
	uint8_t step_d = first.d;
	uint8_t step_e = first.e;
	while (gb_read8(wPrinterPacketSequence_ADDR) != 0u) {
		uint8_t sequence = gb_read8(wPrinterPacketSequence_ADDR);
		if (sequence == 11u)
			gb_write8(rSB, device_response);
		else if (sequence == 12u)
			gb_write8(rSB, status_response);
		ExecutePrinterPacketSequenceResult step = ExecutePrinterPacketSequence(sequence, step_d, step_e);
		step_d = step.d;
		step_e = step.e;
	}
	ResetSerial();
	uint8_t device = gb_read8(wSerialTransferData_ADDR);
	if (device != 0x81u) {
		gb_write8(wPrinterStatus_ADDR, 0xFFu);
		return (SendPrinterPacketResult){0xFFu, 0x10u};
	}
	uint8_t status = gb_read8(wPrinterStatus_ADDR);
	uint8_t f = (uint8_t)((status & 0xF1u) == 0u ? 0x80u : 0x10u);
	return (SendPrinterPacketResult){status, f};
}
/* <<< factory SendPrinterPacket */

/* >>> factory ShowPrinterConnectionErrorScene */
/* link/printer.asm:64-80. Displays the printer-not-connected scene, waits for
 * input, restores the VBlank callback, and returns carry. */
ShowPrinterConnectionErrorSceneResult ShowPrinterConnectionErrorScene(
	uint8_t a, uint8_t f, uint8_t d, uint8_t e, uint16_t hl)
{
	uint16_t text = hl;
	LoadTxRam3((uint16_t)a);
	SetSpriteAnimationsAsVBlankFunction();
	(void)LoadScene(0x12u, f, 0u, 0u, d, e, text);
	(void)DrawWideTextBox_WaitForInput(text);
	RestoreVBlankFunction();
	return (ShowPrinterConnectionErrorSceneResult){0x90u};
}
/* <<< factory ShowPrinterConnectionErrorScene */

/* >>> factory TryInitPrinterCommunications */
/* engine/link/printer.asm:342. B aborts with carry and a zeroed status byte;
 * otherwise NUL packets poll the printer until it answers idle (status bits
 * 1/3 clear), then an INIT packet goes out, restarted from the top up to
 * three times before the time-out exit. Neither oracle ever completes a
 * serial transfer, so only the B exit returns on the reference; the packet
 * paths below run on the PC runtime's synchronous SendPrinterPacket. */
TryInitPrinterCommunicationsResult TryInitPrinterCommunications(void)
{
	wPrinterInitAttempts = 0u;
	for (;;) {
		DoFrame();
		if ((hKeysHeld & PAD_B) != 0u) {
			wPrinterStatus = 0u;
			/* xor a leaves zero set, scf adds carry: a = 0, f = $90 */
			return (TryInitPrinterCommunicationsResult){0x00u, 0x90u};
		}
		SendPrinterPacketResult packet = SendPrinterPacket(0u, 0u, PRINTERPKT_NUL, FALSE, 0u);
		if ((packet.f & 0x10u) != 0u) {
			for (uint8_t frames = 10u; frames != 0u; frames--)
				DoFrame();
		} else if ((packet.a & (uint8_t)((1u << PRINTER_STATUS_BUSY) | (1u << PRINTER_STATUS_PRINTING))) != 0u) {
			continue;
		}
		packet = SendPrinterPacket(0u, 0u, PRINTERPKT_INIT, FALSE, 0u);
		if ((packet.f & 0x10u) == 0u)
			return (TryInitPrinterCommunicationsResult){packet.a, packet.f};
		wPrinterInitAttempts = (uint8_t)(wPrinterInitAttempts + 1u);
		if (wPrinterInitAttempts < 3u)
			continue;
		/* cp 3 sets zero at the limit, scf adds carry: a = attempts, f = $90 */
		return (TryInitPrinterCommunicationsResult){wPrinterInitAttempts, 0x90u};
	}
}
/* <<< factory TryInitPrinterCommunications */

/* >>> factory ShowPrinterIsNotConnected */
ShowPrinterIsNotConnectedResult ShowPrinterIsNotConnected(uint8_t a, uint8_t f, uint8_t d, uint8_t e, uint16_t hl)
{
	a = 0x02u;
	ShowPrinterConnectionErrorSceneResult result = ShowPrinterConnectionErrorScene(a, f, d, e, PrinterIsNotConnectedText);
	return (ShowPrinterIsNotConnectedResult){result.f};
}
/* <<< factory ShowPrinterIsNotConnected */

/* >>> factory HandlePrinterError */
HandlePrinterErrorResult HandlePrinterError(uint8_t f, uint8_t d, uint8_t e)
{
	(void)f;
	uint8_t status = wPrinterStatus;

	if (status == 0xFFu) {
		ShowPrinterConnectionErrorSceneResult scene =
			ShowPrinterConnectionErrorScene(0x02u, 0xC0u, d, e, CheckCableOrPrinterSwitchText);
		return (HandlePrinterErrorResult){scene.f};
	}
	if (status == 0u) {
		WaitResult wait = DrawWideTextBox_WaitForInput(PrintingWasInterruptedText);
		return (HandlePrinterErrorResult){(uint8_t)(wait.f | 0x10u)};
	}
	if ((status & (uint8_t)(1u << PRINTER_ERROR_BATTERIES_LOST_CHARGE)) != 0u) {
		ShowPrinterConnectionErrorSceneResult scene =
			ShowPrinterConnectionErrorScene(0x01u, 0x20u, d, e, BatteriesHaveLostTheirChargeText);
		return (HandlePrinterErrorResult){scene.f};
	}
	if ((status & (uint8_t)(1u << PRINTER_ERROR_CABLE_PRINTER_SWITCH)) != 0u) {
		ShowPrinterConnectionErrorSceneResult scene =
			ShowPrinterConnectionErrorScene(0x02u, 0x20u, d, e, CheckCableOrPrinterSwitchText);
		return (HandlePrinterErrorResult){scene.f};
	}
	if ((status & (uint8_t)(1u << PRINTER_ERROR_PAPER_JAMMED)) != 0u) {
		ShowPrinterConnectionErrorSceneResult scene =
			ShowPrinterConnectionErrorScene(0x03u, 0x20u, d, e, PrinterPaperIsJammedText);
		return (HandlePrinterErrorResult){scene.f};
	}
	ShowPrinterConnectionErrorSceneResult scene =
		ShowPrinterConnectionErrorScene(0x04u, 0xA0u, d, e, PrinterPacketErrorText);
	return (HandlePrinterErrorResult){scene.f};
}
/* <<< factory HandlePrinterError */

/* >>> factory SendPrinterInstructionPacket */
SendPrinterInstructionPacketResult SendPrinterInstructionPacket(uint16_t hl, uint16_t saved_hl)
{
	SendPrinterPacketResult packet = SendPrinterPacket(0u, 0u, PRINTERPKT_DATA, FALSE, hl);
	if ((packet.f & 0x10u) == 0u)
		packet = SendPrinterPacket(0u, 4u, PRINTERPKT_PRINT_INSTRUCTION, FALSE, saved_hl);
	return (SendPrinterInstructionPacketResult){packet.a, packet.f, saved_hl};
}
/* <<< factory SendPrinterInstructionPacket */

/* >>> factory SendPrinterInstructionPacket_1Sheet */
/* engine/link/printer.asm:450. Takes the pending line-feed nybbles out of
 * wPrinterNumberLineFeeds, clears that byte, and falls through into
 * SendPrinterInstructionPacket with h = line feeds and l = 1 sheet. The
 * contrast word pushed here is the caller-pushed word the fallthrough
 * target's second `pop hl` consumes, so it is passed as that routine's
 * saved_hl and comes back as exit hl. b/c/d/e are clobbered by the packet
 * calls (`ld bc, 0` / `lb de, ...`) and are not reported. */
SendPrinterInstructionPacket_1SheetResult SendPrinterInstructionPacket_1Sheet(void)
{
	GetPrinterContrastSerialDataResult contrast = GetPrinterContrastSerialData();
	uint8_t line_feeds = wPrinterNumberLineFeeds;
	wPrinterNumberLineFeeds = 0x00u;
	uint16_t instruction = (uint16_t)(((uint16_t)line_feeds << 8) | 0x01u);
	SendPrinterInstructionPacketResult packet =
		SendPrinterInstructionPacket(instruction, contrast.hl);
	return (SendPrinterInstructionPacket_1SheetResult){packet.a, packet.f, packet.hl};
}
/* <<< factory SendPrinterInstructionPacket_1Sheet */
