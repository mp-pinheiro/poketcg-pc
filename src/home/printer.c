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

#include "home/printer.h"
#include "generated/sram.h"

#include "generated/sram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/copy.h"
#include "home/printer.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "home/random.h"
#include "home/sprite_vblank.h"
#include "home/switch_sram.h"
#include "home/text_box.h"
#include "home/tiles.h"
#define DECK_STRUCT_SIZE 0x54u
#define DeckPrinterText 0x0021u

#include "home/printer.h"

#include "generated/sram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/bg_map.h"
#include "home/card_data.h"
#include "home/core.h"
#include "home/lcd.h"
#include "home/load_animation.h"
#include "home/menus.h"
#include "home/print_text.h"
#include "home/printer.h"
#include "home/sound.h"
#include "home/sprite_vblank.h"
#include "home/text_box.h"
#include "home/tiles.h"
#define TX_END 0x00u
#define SYM_Lv 0x11u
#define SYM_HP 0x0Cu
#define NowPrintingText 0x01a2u

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/card_collection.h"
#include "home/card_data.h"
#include "home/duel.h"
#include "home/empty_screen.h"
#include "home/print_text.h"
#include "home/printer.h"
#include "home/process_text.h"
#include "home/sprite_vblank.h"
#include "home/text_box.h"
#include "home/tiles.h"
#define PAD_SELECT 0x04u
#define PLAYER_TURN 0xC2u
#define GRASS_ENERGY 0x01u
#define STAR 0x02u
/* PROMOTIONAL EQU CARD_SET_PROMOTIONAL << 4, and CARD_SET_PROMOTIONAL is $04
 * (card_data_constants.asm), so the byte is $40. */
#define PROMOTIONAL 0x40u
#define CARD_COUNT_MASK 0x7Fu
#define CARD_NOT_OWNED 0x80u
#define CARD_NOT_OWNED_F 0x07u
#define TX_HALF2FULL 0x07u
#define TYPE_TRAINER 0x10u
#define AllCardsOwnedText 0x0015u
#define TotalNumberOfCardsText 0x0016u
#define TypesOfCardsText 0x0017u
#define GrassPokemonText 0x0018u
#define FirePokemonText 0x0019u
#define WaterPokemonText 0x001Au
#define LightningPokemonText 0x001Bu
#define FightingPokemonText 0x001Cu
#define PsychicPokemonText 0x001Du
#define ColorlessPokemonText 0x001Eu
#define TrainerCardText 0x001Fu
#define EnergyCardText 0x0020u

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/common.h"
#include "home/deck_configuration.h"
#include "home/deck_selection.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/print_text.h"
#include "home/process_text.h"
#define SYM_BOX_TOP 0x1Cu
#define PrintTheCardListText 0x0277u
/* Data_ad05 is `02:6d05 Data_ad05` in poketcg.sym: the nine card-selection
 * parameter bytes (x 3, y 3, y spacing 0, x spacing 4, 2 entries,
 * SYM_CURSOR_R $0F, SYM_SPACE $00, NULL handler) this menu hands
 * InitCardSelectionParams, which reads them through the $4000-$7FFF window. */
#define PRINTER_CARD_LIST_SELECTION_PARAMS_BANK 2u
#define PRINTER_CARD_LIST_SELECTION_PARAMS_ADDR 0x6D05u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/common.h"
#include "home/deck_check.h"
#include "home/deck_configuration.h"
#include "home/deck_selection.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "home/tiles.h"
#include "mem.h"
#define CONSOLE_CGB 0x02u
#define MENU_CANCEL 0xFFu
#define MENU_CONFIRM 0x01u
#define NUM_FILTERS 0x09u
#define PAD_DOWN 0x80u
#define PAD_START 0x08u
#define FILTERS_CARD_SELECTION_PARAMS_ADDR 0x5667u
#define PRINTER_POKEMON_CARDS_DATA_ADDR 0x6396u
#define PRINTER_POKEMON_CARDS_PRINT_LIST_ADDR 0x642Du
#define PRINTER_POKEMON_CARDS_SELECTION_PARAMS_ADDR 0x6D05u
#define PrintThisCardYesNoText 0x0274u
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
	uint16_t hl = sGfxBuffer5_ADDR;
	uint16_t de = (uint16_t)(sGfxBuffer5_ADDR + 0x280u);
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

	uint16_t hl_out = (uint16_t)(sGfxBuffer5_ADDR + 0x280u);
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

/* >>> factory SendTilesToPrinter */
/* engine/link/printer.asm:391-440. Stages two 20-tile rows from the tile map
 * at hl into sGfxBuffer5, resolving each map entry through sGfxBuffer1, then
 * compresses the 0x280-byte buffer and hands the packet to the synchronous
 * SendPrinterPacket transform. .Copy20Tiles reads 20 entries but advances the
 * map by `2 tiles` (32 entries), so the second row starts 32 entries in and
 * the map ends 64 entries along. The `push hl` before Compress is what makes
 * exit hl the advanced map, not Compress's data pointer. */
SendTilesToPrinterResult SendTilesToPrinter(uint16_t hl, uint8_t b, uint8_t c)
{
	(void)b;
	(void)c;
	uint16_t de = sGfxBuffer5_ADDR;
	for (uint8_t row = 0u; row < 2u; row++) {
		for (uint8_t i = 0u; i < 20u; i++) {
			uint8_t tile = gb_read8((uint16_t)(hl + i));
			uint16_t src = (uint16_t)(sGfxBuffer1_ADDR + (uint16_t)((uint16_t)tile << 4u));
			for (uint8_t j = 0u; j < 16u; j++) {
				gb_write8(de, gb_read8((uint16_t)(src + j)));
				de = (uint16_t)(de + 1u);
			}
		}
		hl = (uint16_t)(hl + 32u);
	}

	CompressDataForPrinterSerialTransferResult compressed = CompressDataForPrinterSerialTransfer();
	SendPrinterPacketResult packet =
		SendPrinterPacket((uint8_t)(compressed.bc >> 8), (uint8_t)compressed.bc,
		                  compressed.d, compressed.e, compressed.hl);
	return (SendTilesToPrinterResult){packet.a, packet.f, hl};
}
/* <<< factory SendTilesToPrinter */

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

/* >>> factory SendPrinterInstructionPacket_1Sheet_3LineFeeds */
/* engine/link/printer.asm:442-446. The _1Sheet twin with a constant
 * instruction word: `lb hl, 3, 1` builds h = $03 (line feeds) and l = $01
 * (sheet), replacing the wPrinterNumberLineFeeds read; the contrast word
 * GetPrinterContrastSerialData returns is the pushed word the instruction
 * packet sends as its data and returns as exit hl. */
SendPrinterInstructionPacket_1SheetResult SendPrinterInstructionPacket_1Sheet_3LineFeeds(void)
{
	GetPrinterContrastSerialDataResult contrast = GetPrinterContrastSerialData();
	SendPrinterInstructionPacketResult packet =
		SendPrinterInstructionPacket(0x0301u, contrast.hl);
	return (SendPrinterInstructionPacket_1SheetResult){packet.a, packet.f, packet.hl};
}
/* <<< factory SendPrinterInstructionPacket_1Sheet_3LineFeeds */

/* >>> factory LoadGfxBufferForPrinter */
/* engine/link/printer.asm:615-643. The fallthrough continuation of
 * AddToPrinterGfxBuffer. `srl a` on the horizontal offset is the packet
 * count; each SendTilesToPrinter call consumes 64 map entries, so the map
 * walks sGfxBuffer0 in 64-byte strides. The success exit is `ld a, 1` then
 * `or a`: a=1, f=0x00. */
LoadGfxBufferForPrinterResult LoadGfxBufferForPrinter(uint16_t hl)
{
	TryInitPrinterCommunicationsResult init = TryInitPrinterCommunications();
	if ((init.f & 0x10u) != 0u)
		return (LoadGfxBufferForPrinterResult){init.a, init.f, hl};

	uint8_t count = (uint8_t)(gb_read8(wPrinterHorizontalOffset_ADDR) >> 1u);
	uint16_t map = sGfxBuffer0_ADDR;
	do {
		SendTilesToPrinterResult sent = SendTilesToPrinter(map, 0u, 0u);
		if ((sent.f & 0x10u) != 0u)
			return (LoadGfxBufferForPrinterResult){sent.a, sent.f, hl};
		map = (uint16_t)(map + 64u);
		count = (uint8_t)(count - 1u);
	} while (count != 0u);

	SendPrinterInstructionPacket_1SheetResult instruction = SendPrinterInstructionPacket_1Sheet();
	if ((instruction.f & 0x10u) != 0u)
		return (LoadGfxBufferForPrinterResult){instruction.a, instruction.f, hl};

	(void)ClearPrinterGfxBuffer(instruction.a, instruction.f, 0u, 0u, 0u, 0u, instruction.hl);
	gb_write8(wPrinterHorizontalOffset_ADDR, 1u);
	return (LoadGfxBufferForPrinterResult){1u, 0x00u, hl};
}
/* <<< factory LoadGfxBufferForPrinter */

/* >>> factory AddToPrinterGfxBuffer */
/* engine/link/printer.asm:601-613. `cp 18 / ccf / ret nc`: the no-carry
 * return fires while the doubled offset stays below 18, carrying cp's N and
 * H ((offset & $0F) < 2) with C cleared by ccf; at 18 or above the routine
 * falls through into LoadGfxBufferForPrinter above. */
AddToPrinterGfxBufferResult AddToPrinterGfxBuffer(uint16_t hl)
{
	uint16_t addr = wPrinterHorizontalOffset_ADDR;
	gb_write8(addr, (uint8_t)(gb_read8(addr) + 2u));
	uint8_t offset = gb_read8(addr);
	if (offset < 18u) {
		uint8_t f = (uint8_t)(0x40u | (((offset & 0x0Fu) < 2u) ? 0x20u : 0x00u));
		return (AddToPrinterGfxBufferResult){offset, f, hl};
	}
	LoadGfxBufferForPrinterResult flushed = LoadGfxBufferForPrinter(hl);
	return (AddToPrinterGfxBufferResult){flushed.a, flushed.f, flushed.hl};
}
/* <<< factory AddToPrinterGfxBuffer */

/* >>> factory _PreparePrinterConnection */
/* engine/link/printer.asm:4-19, falls through into HandlePrinterError::21.
 * Sends an empty PRINTERPKT_DATA packet for the caller's buffer (bc = 0,
 * de = PRINTERPKT_DATA/FALSE) and returns on the spot when SendPrinterPacket
 * reports no error. On error a wPrinterStatus of zero -- a printer that
 * answered nothing at all -- is rewritten to $ff, and $ff then routes to
 * ShowPrinterIsNotConnected while every other status falls through into
 * HandlePrinterError.
 *
 * Only f is returned. The one callsite is the farcall wrapper
 * PreparePrinterConnection (menus/common.asm:26), whose own caller
 * (HandlePrinterMenu, engine/menus/printer.asm:232) tests carry alone, and
 * both error exits end inside ShowPrinterConnectionErrorScene, whose ported
 * result is f only -- exit a is residue on two of the three paths, so it is
 * omitted uniformly instead of being guessed on the one path that knows it.
 *
 * d/e reach the error callees as SendPrinterPacket's residue, which its ported
 * result does not carry, so zero is passed; both callees only forward them to
 * LoadScene. hl at the fallthrough is wPrinterStatus (`ld hl, wPrinterStatus`),
 * and ShowPrinterIsNotConnected overwrites it with its text id before use. */
PreparePrinterConnectionResult _PreparePrinterConnection(uint16_t hl)
{
	SendPrinterPacketResult packet = SendPrinterPacket(0u, 0u, PRINTERPKT_DATA, FALSE, hl);
	if ((packet.f & 0x10u) == 0u)
		return (PreparePrinterConnectionResult){packet.f};
	if (wPrinterStatus == 0u)
		wPrinterStatus = 0xFFu;
	uint8_t status = wPrinterStatus;
	if (status == 0xFFu) {
		/* cp $ff with a == $ff: Z and N set, no half-carry, no carry. */
		ShowPrinterIsNotConnectedResult shown =
			ShowPrinterIsNotConnected(status, 0xC0u, 0u, 0u, wPrinterStatus_ADDR);
		return (PreparePrinterConnectionResult){shown.f};
	}
	/* cp $ff with a < $ff: N and C always; H unless the low nibble is $f. */
	uint8_t cp_flags = (uint8_t)(0x50u | ((status & 0x0Fu) == 0x0Fu ? 0x00u : 0x20u));
	HandlePrinterErrorResult handled = HandlePrinterError(cp_flags, 0u, 0u);
	return (PreparePrinterConnectionResult){handled.f};
}
/* <<< factory _PreparePrinterConnection */

/* >>> factory SendCardListToPrinter */
SendCardListToPrinterResult SendCardListToPrinter(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t offset = wPrinterHorizontalOffset;
	if (offset != 1u) {
		LoadGfxBufferForPrinterResult loaded = LoadGfxBufferForPrinter(hl);
		if ((loaded.f & 0x10u) != 0u)
			return (SendCardListToPrinterResult){loaded.a, loaded.f, b, c, d, e, loaded.hl};
		hl = loaded.hl;
	}
	TryInitPrinterCommunicationsResult init = TryInitPrinterCommunications();
	if ((init.f & 0x10u) != 0u)
		return (SendCardListToPrinterResult){init.a, init.f, b, c, d, e, hl};
	SendPrinterInstructionPacket_1SheetResult packet = SendPrinterInstructionPacket_1Sheet_3LineFeeds();
	return (SendCardListToPrinterResult){packet.a, packet.f, b, c, d, e, packet.hl};
}
/* <<< factory SendCardListToPrinter */

/* >>> factory Func_19f87 */
Func_19f87Result Func_19f87(void)
{
	TryInitPrinterCommunicationsResult init = TryInitPrinterCommunications();
	if ((init.f & 0x10u) != 0u)
		return (Func_19f87Result){init.a, init.f};

	SendTilesToPrinterResult first = SendTilesToPrinter(sGfxBuffer0_ADDR, 0u, 0u);
	if ((first.f & 0x10u) != 0u)
		return (Func_19f87Result){first.a, first.f};

	SendTilesToPrinter(first.hl, 0u, 0u);
	SendPrinterInstructionPacket_1SheetResult packet = SendPrinterInstructionPacket_1Sheet();
	return (Func_19f87Result){packet.a, packet.f};
}
/* <<< factory Func_19f87 */

/* >>> factory Func_1a011 */
Func_1a011Result Func_1a011(void)
{
	TryInitPrinterCommunicationsResult init = TryInitPrinterCommunications();
	if ((init.f & 0x10u) != 0u)
		return (Func_1a011Result){init.a, init.f};

	uint16_t map = sGfxBuffer0_ADDR;
	for (uint8_t count = 5u; count != 0u; count--) {
		SendTilesToPrinterResult sent = SendTilesToPrinter(map, 0u, 0u);
		if ((sent.f & 0x10u) != 0u)
			return (Func_1a011Result){sent.a, sent.f};
		map = sent.hl;
	}

	SendPrinterInstructionPacket_1SheetResult packet = SendPrinterInstructionPacket_1Sheet_3LineFeeds();
	return (Func_1a011Result){packet.a, packet.f};
}
/* <<< factory Func_1a011 */

/* >>> factory Func_19f99 */
Func_19f99Result Func_19f99(void)
{
	TryInitPrinterCommunicationsResult init = TryInitPrinterCommunications();
	if ((init.f & 0x10u) != 0u)
		return (Func_19f99Result){init.a, init.f};

	uint16_t hl = (uint16_t)(sGfxBuffer0_ADDR + 128u);
	uint8_t c = 6u;
	while (c != 0u) {
		SendTilesToPrinterResult tiles = SendTilesToPrinter(hl, 0u, c);
		if ((tiles.f & 0x10u) != 0u)
			return (Func_19f99Result){tiles.a, tiles.f};
		hl = tiles.hl;
		c--;
	}

	SendPrinterInstructionPacket_1SheetResult packet = SendPrinterInstructionPacket_1Sheet();
	return (Func_19f99Result){packet.a, packet.f};
}
/* <<< factory Func_19f99 */

/* >>> factory _PrintDeckConfiguration */
void _PrintDeckConfiguration(uint8_t a)
{
	EnableSRAM();
	uint16_t hl = HtimesL((uint16_t)(((uint16_t)DECK_STRUCT_SIZE << 8) | a));
	hl = (uint16_t)(hl + sSavedDeck1_ADDR);
	uint16_t de = wDuelTempList_ADDR;
	CopyDataHLtoDE(&hl, &de, DECK_STRUCT_SIZE);
	DisableSRAM();

	ShowPrinterTransmitting();
	(void)PrepareForPrinterCommunications(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	Func_1a025();
	TileCopyResult tiles = Func_212f();
	DrawRegularTextBoxDMG(&tiles.hl, 0u, 20u, 4u, 0u, 64u);
	InitTextPrinting(4u, 66u);
	hl = wDuelTempList_ADDR;
	ProcessText(&hl);
	(void)ProcessTextFromID(DeckPrinterText);

	wPrinterHorizontalOffset = 5u;
	wPrinterTotalCardCount = 0u;
	gb_write8((uint16_t)(wPrinterTotalCardCount_ADDR + 1u), 0u);
	wPrintOnlyStarRarity = 0u;

	hl = wCurDeckCards_ADDR;
	for (;;) {
		uint8_t card = gb_read8(hl);
		if (card == 0u)
			break;
		uint8_t b = card;
		hl = (uint16_t)(hl + 1u);
		uint8_t c = 1u;
		LoadCardDataToBuffer1_FromCardID(card);
		while (gb_read8(hl) == card) {
			hl = (uint16_t)(hl + 1u);
			c = (uint8_t)(c + 1u);
		}
		wPrinterCardCount = c;
		LoadCardInfoForPrinter(b, c, &hl);
		AddToPrinterGfxBufferResult added = AddToPrinterGfxBuffer(hl);
		if ((added.f & 0x10u) != 0u) {
			(void)ResetPrinterCommunicationSettings(added.a, added.f, 0u, 0u, 0u, 0u, added.hl);
			RestoreVBlankFunction();
			(void)HandlePrinterError(added.f, 0u, 0u);
			return;
		}
	}

	SendCardListToPrinterResult sent = SendCardListToPrinter(0u, 0u, 0u, 0u, 0u, 0u, hl);
	if ((sent.f & 0x10u) != 0u) {
		(void)ResetPrinterCommunicationSettings(sent.a, sent.f, sent.b, sent.c, sent.d, sent.e, sent.hl);
		RestoreVBlankFunction();
		(void)HandlePrinterError(sent.f, sent.d, sent.e);
		return;
	}
	(void)ResetPrinterCommunicationSettings(sent.a, sent.f, sent.b, sent.c, sent.d, sent.e, sent.hl);
	RestoreVBlankFunction();
}
/* <<< factory _PrintDeckConfiguration */

/* >>> factory Func_1a080 */
/* engine/link/printer.asm:333, unreferenced. A status-probe packet: bc = 0
 * (no data bytes), lb de, PRINTERPKT_NUL, FALSE, and the caller's hl as the
 * packet's data pointer. `jp SendPrinterPacket` is a tail jump, so the
 * callee's exit registers are this routine's exit registers and the ported
 * a/f come straight back. */
Func_1a080Result Func_1a080(uint16_t hl)
{
	SendPrinterPacketResult packet = SendPrinterPacket(0u, 0u, PRINTERPKT_NUL, FALSE, hl);
	return (Func_1a080Result){packet.a, packet.f};
}
/* <<< factory Func_1a080 */

/* >>> factory _RequestToPrintCard */
/* engine/link/printer.asm:83. Entry a is the card id (`ld e, a` feeds
 * LoadCardDataToBuffer1_FromCardID); d/e/b/c/hl are all reloaded by this
 * routine or by its callees before any use, so they are not parameters.
 *
 * The two local labels .DrawTopCardInfoInSRAMGfxBuffer0 (printer.asm:139) and
 * .DrawCardPicInSRAMGfxBuffer2 (printer.asm:125) are each called exactly once
 * and are inlined at their callsites.
 *
 * Only f is reported. The success exit is `or a` over the a that
 * ResetPrinterCommunicationSettings passes through, and both error exits end
 * in HandlePrinterError, whose ported result is f alone -- exit a is residue
 * on the error paths, so it is omitted uniformly rather than guessed. */
RequestToPrintCardResult _RequestToPrintCard(uint8_t a)
{
	LoadCardDataToBuffer1_FromCardID(a);
	SetSpriteAnimationsAsVBlankFunction();
	LoadSceneResult scene =
		LoadScene(SCENE_GAMEBOY_PRINTER_TRANSMITTING, 0u, 0u, 0u, 0u, 0u, 0u);
	CopyCardNameAndLevelResult name =
		CopyCardNameAndLevel(20u, scene.b, scene.c, scene.d, scene.e);
	gb_write8(name.hl, TX_END);
	LoadTxRam2(0u);
	(void)DrawWideTextBox_PrintText(NowPrintingText);
	EnableLCD();
	(void)PrepareForPrinterCommunications(0u, 0u, 0u, 0u, 0u, 0u, 0u);

	/* .DrawTopCardInfoInSRAMGfxBuffer0: the empty text box frame, the card's
	 * type symbol and its name, plus lv/HP for a Pokemon card. */
	Func_1a025();
	(void)Func_212f();
	uint16_t hl = sGfxBuffer0_ADDR;
	CopyLine(&hl, 0x34u, 20u, 0x30u, 0x31u);
	uint8_t lines = 15u;
	while (lines != 0u) {
		CopyLine(&hl, SYM_SPACE, 20u, 0x36u, 0x37u);
		lines = (uint8_t)(lines - 1u);
	}
	FillRectangle(0x38u, 2u, 2u, 0x0141u, 0x0102u);
	(void)InitTextPrinting_ProcessTextFromPointerToID(4u, 65u, wLoadedCard1Name_ADDR);
	uint8_t type = gb_read8(wLoadedCard1Type_ADDR);
	if (type < TYPE_ENERGY) {
		WriteByteToBGMap0((uint8_t)(type + 1u), 18u, 65u);
		WriteByteToBGMap0(SYM_Lv, 11u, 66u);
		WriteTwoDigitNumberInTxSymbol_PadSpace(gb_read8(wLoadedCard1Level_ADDR),
						       12u, 66u, 0u, 0u, 0u);
		WriteByteToBGMap0(SYM_HP, 15u, 66u);
		WriteOneByteNumberInTxSymbol_PadSpace(gb_read8(wLoadedCard1HP_ADDR),
						      16u, 66u, 0u, 0u, 0u);
	}

	/* The asm ignores this result: there is no `jr c` after the call. */
	(void)Func_19f87();

	/* .DrawCardPicInSRAMGfxBuffer2: the card picture pointer is the word at
	 * wLoadedCard1Gfx. */
	uint16_t gfx = (uint16_t)(gb_read8(wLoadedCard1Gfx_ADDR) |
				  ((uint16_t)gb_read8((uint16_t)(wLoadedCard1Gfx_ADDR + 1u)) << 8));
	(void)Func_37a5(gfx, sGfxBuffer2_ADDR);
	FillRectangle(0x40u, 16u, 12u, 0x0244u, 0x0C01u);

	Func_19f99Result picture = Func_19f99();
	if ((picture.f & 0x10u) != 0u) {
		RestoreVBlankFunction();
		ResetPrinterCommunicationSettingsResult reset =
			ResetPrinterCommunicationSettings(1u, picture.f, 0u, 0u, 0u, 0u, 0u);
		HandlePrinterErrorResult handled = HandlePrinterError(reset.f, reset.d, reset.e);
		return (RequestToPrintCardResult){handled.f};
	}

	DrawBottomCardInfoInSRAMGfxBuffer0();

	Func_1a011Result bottom = Func_1a011();
	if ((bottom.f & 0x10u) != 0u) {
		RestoreVBlankFunction();
		ResetPrinterCommunicationSettingsResult reset =
			ResetPrinterCommunicationSettings(1u, bottom.f, 0u, 0u, 0u, 0u, 0u);
		HandlePrinterErrorResult handled = HandlePrinterError(reset.f, reset.d, reset.e);
		return (RequestToPrintCardResult){handled.f};
	}

	RestoreVBlankFunction();
	/* RestoreVBlankFunction's tail is ZeroObjectPositionsAndToggleOAMCopy,
	 * whose last act is `ld a, TRUE` / `ld [wVBlankOAMCopyToggle], a`, so a is
	 * 1 here and ResetPrinterCommunicationSettings passes it through. */
	ResetPrinterCommunicationSettingsResult reset =
		ResetPrinterCommunicationSettings(1u, bottom.f, 0u, 0u, 0u, 0u, 0u);
	/* `or a`: carry, N and H clear, Z from a. */
	return (RequestToPrintCardResult){(uint8_t)(reset.a == 0u ? 0x80u : 0x00u)};
}
/* <<< factory _RequestToPrintCard */

/* >>> factory _PrintCardList */
/* .printer_error / .printer_error_pop_de (printer.asm:797): the shared error
 * tail. ResetPrinterCommunicationSettings brackets its body with push af/pop af,
 * so the carry that got here survives into HandlePrinterError, whose ported
 * result is f alone. */
static uint8_t print_card_list_printer_error(uint8_t a, uint8_t f, uint8_t b, uint8_t c,
					     uint8_t d, uint8_t e, uint16_t hl)
{
	ResetPrinterCommunicationSettingsResult reset =
		ResetPrinterCommunicationSettings(a, f, b, c, d, e, hl);
	RestoreVBlankFunction();
	HandlePrinterErrorResult handled = HandlePrinterError(reset.f, reset.d, reset.e);
	return handled.f;
}

/* .PrintTextWithNumber (printer.asm:838): prints text id `hl` at column 2 of the
 * current printer row, then the decimal form of the number in bc at column 14.
 * The second InitTextPrinting keeps whatever e ProcessTextFromID left behind --
 * the asm reloads d only. Carry is AddToPrinterGfxBuffer's. */
static AddToPrinterGfxBufferResult print_card_list_text_with_number(uint16_t text_id,
								   uint16_t number)
{
	uint8_t e = (uint8_t)((uint8_t)(wPrinterHorizontalOffset - 1u) | 0x40u);
	InitTextPrinting(2u, e);
	ProcessTextHeaderResult header = ProcessTextFromID(text_id);
	InitTextPrinting(14u, header.e);
	(void)TwoByteNumberToTxSymbol_PadSpace(number);
	uint16_t hl = wStringBuffer_ADDR;
	ProcessText(&hl);
	return AddToPrinterGfxBuffer(hl);
}

/* .LoadCardTypeEntry (printer.asm:860): when wLoadedCard1's type differs from
 * wCurPrinterCardType, draw that type's icon and label and reset the per-type
 * counters. Both exits clear carry -- `cp c` on equality, and the trailing
 * `xor a` on the drawing path -- so the caller's `jr c, .printer_error_pop_de`
 * is unreachable and is not modelled. */
static void print_card_list_card_type_entry(void)
{
	/* .IconTextList (printer.asm:900): three bytes per entry, icon tile then
	 * the little-endian text id. Indices 0-6 are the TYPE_PKMN_* order, index
	 * 7 is Energy (every TYPE_ENERGY_* card) and index 8 is Trainer. */
	static const uint8_t icon_tiles[9] = {
		0xE0u, 0xE4u, 0xE8u, 0xECu, 0xF0u, 0xF4u, 0xF8u, 0xFCu, 0xDCu
	};
	static const uint16_t icon_texts[9] = {
		FirePokemonText, GrassPokemonText, LightningPokemonText,
		WaterPokemonText, FightingPokemonText, PsychicPokemonText,
		ColorlessPokemonText, EnergyCardText, TrainerCardText
	};

	uint8_t type = wLoadedCard1Type;
	uint8_t c = type;
	if (type >= TYPE_ENERGY) {
		c = 0x08u;
		if (type < TYPE_TRAINER)
			c = 0x07u;
	}
	if (wCurPrinterCardType == c)
		return;
	wCurPrinterCardType = c;

	uint8_t e = (uint8_t)((uint8_t)(wPrinterHorizontalOffset - 1u) | 0x40u);
	FillRectangle(icon_tiles[c], 2u, 2u, (uint16_t)(0x0100u | e), 0x0102u);
	e = (uint8_t)(e + 1u);
	InitTextPrinting(3u, e);
	ProcessTextHeaderResult label = ProcessTextFromID(icon_texts[c]);
	(void)AddToPrinterGfxBuffer(label.hl);

	gb_write8(wPrinterCurCardTypeCount_ADDR, 0u);
	gb_write8((uint16_t)(wPrinterCurCardTypeCount_ADDR + 1u), 0u);
	wce98 = 0u;
}

PrintCardListResult _PrintCardList(void)
{
	uint8_t star_only = FALSE;
	if ((hKeysHeld & PAD_SELECT) != 0u)
		star_only = TRUE;
	wPrintOnlyStarRarity = star_only;

	ShowPrinterTransmitting();
	CreateTempCardCollection();
	(void)CopyPlayerName(wDefaultText_ADDR);
	(void)PrepareForPrinterCommunications(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	Func_1a025();
	TileCopyResult tiles = Func_212f();
	DrawRegularTextBoxDMG(&tiles.hl, 0u, 20u, 4u, 0u, 64u);
	hWhoseTurn = PLAYER_TURN;
	InitTextPrinting(2u, 66u);
	uint16_t text = wDefaultText_ADDR;
	ProcessText(&text);
	ProcessTextHeaderResult owned = ProcessTextFromID(AllCardsOwnedText);
	if (wPrintOnlyStarRarity != 0u) {
		(void)ProcessSpecialTextCharacter(TX_HALF2FULL, owned.hl);
		/* ldfw de, fullwidth star: charmaps.asm:360 maps it to the two bytes
		 * TX_FULLWIDTH3 ($03) and $54, loaded high-byte-first into de. */
		Func_22ca(0x03u, 0x54u);
	}

	wCurPrinterCardType = 0xFFu;
	gb_write8(wPrinterTotalCardCount_ADDR, 0u);
	gb_write8((uint16_t)(wPrinterTotalCardCount_ADDR + 1u), 0u);
	wPrinterNumCardTypes = 0u;
	wPrinterHorizontalOffset = 5u;

	uint8_t card_id = GRASS_ENERGY;
	for (;;) {
		/* `jr c, .done_card_loop` tests the carry that GetCardPointer raises
		 * for an out-of-range id. The ported LoadCardDataToBuffer1_FromCardID
		 * is void and copies unconditionally, so the bound is evaluated here
		 * first and wLoadedCard1 is left alone exactly as the ROM leaves it. */
		CardPtrResult ptr = GetCardPointer(card_id);
		if (ptr.carry)
			break;
		LoadCardDataToBuffer1_FromCardID(card_id);
		/* `ld d, HIGH(wTempCardCollection)` / `ld a, [de]`: the collection
		 * count lives at the card id's slot in the $C0 page. */
		wPrinterCardCount = gb_read8((uint16_t)((wTempCardCollection_ADDR & 0xFF00u)
							| card_id));
		print_card_list_card_type_entry();

		uint8_t counted;
		if (wPrintOnlyStarRarity != 0u) {
			counted = (uint8_t)((wLoadedCard1Set & 0xF0u) != PROMOTIONAL &&
					    wLoadedCard1Rarity == STAR);
			if (counted != 0u)
				wPrinterCardCount &= (uint8_t)~(uint8_t)(1u << CARD_NOT_OWNED_F);
		} else {
			uint8_t count = wPrinterCardCount;
			counted = (uint8_t)(count != 0u && count != CARD_NOT_OWNED);
		}

		if (counted != 0u) {
			uint8_t c = (uint8_t)(wPrinterCardCount & CARD_COUNT_MASK);

			uint16_t total = wPrinterTotalCardCount_ADDR;
			uint16_t total_sum = (uint16_t)(c + gb_read8(total));
			gb_write8(total, (uint8_t)total_sum);
			gb_write8((uint16_t)(total + 1u),
				  (uint8_t)(gb_read8((uint16_t)(total + 1u))
					    + (uint8_t)(total_sum >> 8)));

			uint16_t cur = wPrinterCurCardTypeCount_ADDR;
			uint16_t cur_sum = (uint16_t)(c + gb_read8(cur));
			gb_write8(cur, (uint8_t)cur_sum);
			gb_write8((uint16_t)(cur + 1u),
				  (uint8_t)(gb_read8((uint16_t)(cur + 1u))
					    + (uint8_t)(cur_sum >> 8)));

			wPrinterNumCardTypes = (uint8_t)(wPrinterNumCardTypes + 1u);
			wce98 = (uint8_t)(wce98 + 1u);

			/* hl is still wce98 here; LoadCardInfoForPrinter pushes and pops
			 * it, so AddToPrinterGfxBuffer sees the same word. b is caller
			 * residue that LoadCardInfoForPrinter only hands to
			 * CopyCardNameAndLevel, which passes it straight back. */
			uint16_t hl = wce98_ADDR;
			LoadCardInfoForPrinter(0u, c, &hl);
			AddToPrinterGfxBufferResult added = AddToPrinterGfxBuffer(hl);
			if ((added.f & 0x10u) != 0u)
				return (PrintCardListResult){print_card_list_printer_error(
					added.a, added.f, 0u, 0u, 0u, 0u, added.hl)};
		}
		card_id = (uint8_t)(card_id + 1u);
	}

	/* .done_card_loop: the separator line under the last card row. */
	uint8_t row = (uint8_t)((uint8_t)(wPrinterHorizontalOffset - 1u) | 0x40u);
	uint16_t line = BCCoordToBGMap0Address(0u, row);
	CopyLine(&line, 0x35u, 20u, 0x35u, 0x35u);
	AddToPrinterGfxBufferResult separator = AddToPrinterGfxBuffer(line);
	if ((separator.f & 0x10u) != 0u)
		return (PrintCardListResult){print_card_list_printer_error(
			separator.a, separator.f, 0u, 0u, 0u, 0u, separator.hl)};

	uint16_t total_ptr = wPrinterTotalCardCount_ADDR;
	uint16_t total = (uint16_t)(gb_read8(total_ptr)
				    | ((uint16_t)gb_read8((uint16_t)(total_ptr + 1u)) << 8));
	AddToPrinterGfxBufferResult printed =
		print_card_list_text_with_number(TotalNumberOfCardsText, total);
	if ((printed.f & 0x10u) != 0u)
		return (PrintCardListResult){print_card_list_printer_error(
			printed.a, printed.f, 0u, 0u, 0u, 0u, printed.hl)};

	if (wPrintOnlyStarRarity == 0u) {
		printed = print_card_list_text_with_number(TypesOfCardsText,
							  wPrinterNumCardTypes);
		if ((printed.f & 0x10u) != 0u)
			return (PrintCardListResult){print_card_list_printer_error(
				printed.a, printed.f, 0u, 0u, 0u, 0u, printed.hl)};
	}

	SendCardListToPrinterResult sent =
		SendCardListToPrinter(printed.a, printed.f, 0u, 0u, 0u, 0u, printed.hl);
	if ((sent.f & 0x10u) != 0u)
		return (PrintCardListResult){print_card_list_printer_error(
			sent.a, sent.f, sent.b, sent.c, sent.d, sent.e, sent.hl)};

	(void)ResetPrinterCommunicationSettings(sent.a, sent.f, sent.b, sent.c,
						sent.d, sent.e, sent.hl);
	RestoreVBlankFunction();
	/* `or a` over RestoreVBlankFunction's exit a, whose
	 * ZeroObjectPositionsAndToggleOAMCopy tail ends in `ld a, TRUE` /
	 * `ld [wVBlankOAMCopyToggle], a`: a is 1, so Z stays clear and carry, N
	 * and H are cleared. */
	return (PrintCardListResult){0x00u};
}
/* <<< factory _PrintCardList */

/* >>> factory PrinterMenu_CardList */
/* engine/menus/printer.asm:200. The card-list entry of the printer menu:
 * draws the collection screen, seeds the two-entry cursor parameters from
 * Data_ad05 (02:6d05), then loops on DoFrame until HandleCardSelectionInput
 * reports a selection. hffb3 then holds the cursor position the input handler
 * stored, or MENU_CANCEL on B, and only position 0 falls through to the
 * bank1call.
 *
 * Entry registers are all dead -- b/c/d/e/hl are loaded by the routine and a
 * is `xor a`ed before anything reads it. The two exits disagree on a/f: the
 * `ret nz` leaves a = [hffb3] with `or a`'s flags (Z clear, so f = $00), while
 * the bank1call exit leaves PrintCardList's own a/f and the ported
 * PrintCardList surfaces carry alone. Nothing is returned, exactly as the
 * landed HandleDeckConfirmationMenu records for the same two-exit shape; the
 * single caller (HandlePrinterMenu's JumpToFunctionInTable dispatch) reloads a
 * from wSelectedPrinterMenuItem and discards both. */
void PrinterMenu_CardList(void)
{
	(void)WriteCardListsTerminatorBytes();
	Set_OBJ_8x8();
	PrepareMenuGraphics();
	FillBGMapLineWithA(SYM_BOX_TOP, 0u, 4u);

	wCardListVisibleOffset = 0u;
	wCurCardTypeFilter = 0u;
	/* `xor a` leaves a = 0 and f = $80; FillBGMapLineWithA returns with
	 * b = c = 0 and de = hl = BCCoordToBGMap0Address(0, 4) = $9880. Only a
	 * reaches the filter lookup -- the callee reloads bc and passes d/e/hl
	 * on to CreateFilteredCardList, which never reads them. */
	PrintFilteredCardSelectionList(0u, 0x80u, 0u, 0u, 0x98u, 0x80u, 0x9880u);
	EnableLCD();
	InitTextPrinting(1u, 1u);
	(void)ProcessTextFromID(PrintTheCardListText);

	/* `ld hl, Data_ad05` is a bank-local read with no bankswitch: the
	 * routine executes from bank 2 and every callee above restores the
	 * caller's bank before returning, so the reference still has bank 2
	 * latched here. The port states that latch the way the landed music
	 * routines state theirs, because the ported callees reach their own
	 * data through g_rom_bank and do not put it back. */
	g_rom_bank = PRINTER_CARD_LIST_SELECTION_PARAMS_BANK;
	uint16_t params = PRINTER_CARD_LIST_SELECTION_PARAMS_ADDR;
	(void)InitCardSelectionParams(0x01u, &params);

	for (;;) { /* .loop_frame */
		DoFrame();
		if (HandleCardSelectionInput().carry != 0u)
			break;
	}

	if (hffb3 != 0u)
		return;
	(void)PrintCardList();
}
/* <<< factory PrinterMenu_CardList */

/* >>> factory PrinterMenu_PokemonCards */
void PrinterMenu_PokemonCards(void)
{
	(void)WriteCardListsTerminatorBytes();
	PrintPlayersCardsHeaderInfo();

	wCardListVisibleOffset = 0u;
	wCurCardTypeFilter = 0u;
	PrintFilteredCardSelectionList(0u, 0x80u, 0u, 0u, 0u, 0u, wCardListCoords_ADDR);
	EnableLCD();

	uint16_t filter_params = FILTERS_CARD_SELECTION_PARAMS_ADDR;
	g_rom_bank = 2u;
	(void)InitCardSelectionParams(0u, &filter_params);

	for (;;) {
		DoFrame();
		uint8_t current_filter = wCurCardTypeFilter;
		uint8_t temp_filter = wTempCardTypeFilter;
		if (temp_filter != current_filter) {
			wCurCardTypeFilter = temp_filter;
			wCardListVisibleOffset = 0u;
			PrintFilteredCardSelectionList(temp_filter, 0u, 0u, 0u, 0u, 0u, wCardListVisibleOffset_ADDR);
			hffb0 = 1u;
			PrintPlayersCardsText();
			hffb0 = 0u;
			wCardListNumCursorPositions = NUM_FILTERS;
		}

		if ((hDPadHeld & PAD_DOWN) != 0u) {
			(void)ConfirmSelectionAndReturnCarry();
		} else {
			HandleCardSelectionInputResult input = HandleCardSelectionInput();
			if (input.carry == 0u)
				continue;
			if (hffb3 == MENU_CANCEL)
				return;
		}

		if (wNumEntriesInCurFilter == 0u)
			continue;

		uint16_t list_params = PRINTER_POKEMON_CARDS_DATA_ADDR;
		g_rom_bank = 2u;
		(void)InitCardSelectionParams(0u, &list_params);
		uint8_t entries = wNumEntriesInCurFilter;
		wNumCardListEntries = entries;
		if (entries < wNumVisibleCardListEntries)
			wCardListNumCursorPositions = entries;
		gb_write8(wCardListUpdateFunction_ADDR, (uint8_t)PRINTER_POKEMON_CARDS_PRINT_LIST_ADDR);
		gb_write8((uint16_t)(wCardListUpdateFunction_ADDR + 1u),
			(uint8_t)(PRINTER_POKEMON_CARDS_PRINT_LIST_ADDR >> 8));
		wced2 = 0u;

		for (;;) {
			DoFrame();
			HandleSelectUpAndDownInListResult move = HandleSelectUpAndDownInList();
			if ((move.f & 0x10u) != 0u)
				continue;

			HandleDeckCardSelectionListResult selection = HandleDeckCardSelectionList();
			if ((selection.f & 0x10u) != 0u) {
				(void)DrawListCursor_Invisible();
				wTempCardListNumCursorPositions = wCardListNumCursorPositions;
				wTempCardListCursorPos = wCardListCursorPos;
				if (hffb3 == MENU_CANCEL) {
					uint16_t params = FILTERS_CARD_SELECTION_PARAMS_ADDR;
					g_rom_bank = 2u;
					(void)InitCardSelectionParams(hffb3, &params);
					wTempCardTypeFilter = wCurCardTypeFilter;
					hffb0 = 1u;
					PrintPlayersCardsText();
					hffb0 = 0u;
					break;
				}
			} else if ((hDPadHeld & PAD_START) == 0u) {
				continue;
			}

			PlaySFXConfirmOrCancel(MENU_CONFIRM);
			wTempCardListNumCursorPositions = wCardListNumCursorPositions;
			wTempCardListCursorPos = wCardListCursorPos;
			gb_write8(wCurCardListPtr_ADDR, (uint8_t)wFilteredCardList_ADDR);
			gb_write8((uint16_t)(wCurCardListPtr_ADDR + 1u),
				(uint8_t)(wFilteredCardList_ADDR >> 8));
			OpenCardPageFromCardList();
			PrintPlayersCardsHeaderInfo();

			uint16_t params = FILTERS_CARD_SELECTION_PARAMS_ADDR;
			g_rom_bank = 2u;
			(void)InitCardSelectionParams(0u, &params);
			wTempCardTypeFilter = wCurCardTypeFilter;
			(void)DrawHorizontalListCursor_Visible();
			PrintCardSelectionList();
			EnableLCD();
			uint16_t data_params = PRINTER_POKEMON_CARDS_DATA_ADDR;
			g_rom_bank = 2u;
			(void)InitCardSelectionParams(0u, &data_params);
			wCardListNumCursorPositions = wTempCardListNumCursorPositions;
			wCardListCursorPos = wTempCardListCursorPos;
		}

		if (hffb3 == MENU_CANCEL)
			continue;

		(void)DrawListCursor_Visible();
		FillRectangle(0u, 20u, 4u, 0u, 0u);
		if (wConsole == CONSOLE_CGB) {
			hBankVRAM = 1u;
			gb_write8(0xFF4Fu, 1u);
			FillRectangle(0u, 20u, 4u, 0u, 0u);
			hBankVRAM = 0u;
			gb_write8(0xFF4Fu, 0u);
		}
		InitTextPrinting(1u, 1u);
		(void)ProcessTextFromID(PrintThisCardYesNoText);
		uint16_t yes_no_params = PRINTER_POKEMON_CARDS_SELECTION_PARAMS_ADDR;
		g_rom_bank = 2u;
		(void)InitCardSelectionParams(1u, &yes_no_params);

		for (;;) {
			DoFrame();
			HandleCardSelectionInputResult input = HandleCardSelectionInput();
			if (input.carry == 0u)
				continue;
			if (hffb3 == 0u) {
				uint16_t card_list = wFilteredCardList_ADDR;
				card_list = (uint16_t)(card_list + wTempCardListCursorPos);
				card_list = (uint16_t)(card_list + wCardListVisibleOffset);
				(void)RequestToPrintCard(gb_read8(card_list));
				PrintPlayersCardsHeaderInfo();
				break;
			}
			FillRectangle(0u, 20u, 4u, 0u, 0u);
			if (wConsole == CONSOLE_CGB) {
				hBankVRAM = 1u;
				gb_write8(0xFF4Fu, 1u);
				FillRectangle(0u, 20u, 4u, 0u, 0u);
				hBankVRAM = 0u;
				gb_write8(0xFF4Fu, 0u);
			}
			FillBGMapLineWithA(SYM_BOX_TOP, 0u, 4u);
			PrintTotalNumberOfCardsInCollection();
			PrintPlayersCardsText();
			DrawCardTypeIcons();
			break;
		}

		uint16_t filter_params_after = FILTERS_CARD_SELECTION_PARAMS_ADDR;
		g_rom_bank = 2u;
		(void)InitCardSelectionParams(0u, &filter_params_after);
		wTempCardTypeFilter = wCurCardTypeFilter;
		(void)DrawHorizontalListCursor_Visible();
		PrintCardSelectionList();
		EnableLCD();
		uint16_t data_params_after = PRINTER_POKEMON_CARDS_DATA_ADDR;
		g_rom_bank = 2u;
		(void)InitCardSelectionParams(0u, &data_params_after);
		wCardListNumCursorPositions = wTempCardListNumCursorPositions;
		wCardListCursorPos = wTempCardListCursorPos;
	}
}
/* <<< factory PrinterMenu_PokemonCards */
