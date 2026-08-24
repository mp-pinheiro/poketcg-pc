#include "home/deck_machine.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/print_text.h"
#include "home/process_text.h"
#include "home/switch_sram.h"

#define DECK_NAME_SIZE 0x18u
#define NUM_DECK_MACHINE_SLOTS 0x05u

#include "home/switch_sram.h"

#define CARD_NOT_OWNED 0x80u
#define DECK_SIZE 0x3Cu

#include "home/deck_configuration.h"
#include "generated/sram.h"

#define DECK_STRUCT_SIZE            0x54u
#define NUM_DECK_SAVE_MACHINE_SLOTS 0x3cu

#include "generated/wram.h"
#include "home/bg_map.h"

#define FALSE 0x00u
#define NUM_DECK_MACHINE_VISIBLE_DECKS 0x05u
#define TRUE 0x01u
#define SYM_CURSOR_U 0x0Cu
#define SYM_BOX_RIGHT 0x1Fu
#define SYM_CURSOR_D 0x2Fu

#include "home/process_text.h"
#include "home/print_text.h"
#include "generated/wram.h"

#include "home/deck_machine.h"

#define CardToSendText 0x0281u

#define CardReceivedText 0x0280u
#define ReceivedTheseCardsFromText 0x0283u

#include "home/deck_configuration.h"
#include "home/process_text.h"
#include "generated/wram.h"
#include "mem.h"
#define TX_END 0x00u
#define TX_SYMBOL 0x05u
#define SYM_SLASH 0x2Eu
/* <<< factory statics */

/* >>> factory CheckIfSelectedDeckMachineEntryIsEmpty */
/* deck_machine.asm:772-789 */
uint8_t CheckIfSelectedDeckMachineEntryIsEmpty(void)
{
	uint16_t entry = (uint16_t)(wMachineDeckPtrs_ADDR
		+ (uint16_t)wSelectedDeckMachineEntry * 2u);
	uint16_t deck = (uint16_t)(gb_read8(entry)
		| (uint16_t)(gb_read8((uint16_t)(entry + 1u)) << 8));
	uint16_t name = (uint16_t)(deck + DECK_NAME_SIZE);

	EnableSRAM();
	uint8_t value = gb_read8(name);
	DisableSRAM();

	return value ? 0u : 0x90u;
}
/* <<< factory CheckIfSelectedDeckMachineEntryIsEmpty */

/* >>> factory SafelySwitchToSRAM1 */
/* deck_machine.asm:1261-1271. */
void SafelySwitchToSRAM1(void)
{
	if (hBankSRAM != 1u) {
		wTempBankSRAM = hBankSRAM;
		BankswitchSRAM(1u);
	}
}
/* <<< factory SafelySwitchToSRAM1 */

/* >>> factory SafelySwitchToTempSRAMBank */
/* deck_machine.asm:1273-1285. */
void SafelySwitchToTempSRAMBank(void)
{
	if (hBankSRAM != wTempBankSRAM)
		BankswitchSRAM(wTempBankSRAM);
}
/* <<< factory SafelySwitchToTempSRAMBank */

/* >>> factory CheckIfHasEnoughCardsToBuildDeck */
/* deck_machine.asm:1290-1323. */
DeckBuildCheckResult CheckIfHasEnoughCardsToBuildDeck(uint16_t *hl)
{
	EnableSRAM();
	uint16_t deck = *hl;
	uint16_t collection = wTempCardCollection_ADDR;

	for (uint8_t i = 0; i < DECK_SIZE; i++) {
		uint8_t card = gb_read8(deck);
		deck = (uint16_t)(deck + 1u);
		uint16_t slot = (uint16_t)(collection + card);
		uint8_t count = gb_read8(slot);
		if (count == 0u || count == CARD_NOT_OWNED) {
			*hl = deck;
			DisableSRAM();
			return (DeckBuildCheckResult){ .a = count, .f = 0x90u };
		}
		gb_write8(slot, (uint8_t)(count - 1u));
	}

	*hl = deck;
	DisableSRAM();
	return (DeckBuildCheckResult){ .a = DECK_SIZE, .f = 0x00u };
}
/* <<< factory CheckIfHasEnoughCardsToBuildDeck */

/* >>> factory GetSavedDeckPointers */
/* deck_machine.asm:827-860. Clears the wMachineDeckPtrs array (2 bytes per
 * slot), then fills it with little-endian pointers to each consecutive
 * DECK_STRUCT_SIZE-byte saved-deck struct in sSavedDecks. Exits with hl/de
 * advanced past the table/structs processed. */
void GetSavedDeckPointers(uint16_t *hl, uint16_t *de)
{
	ClearMemory_Bank2((uint8_t)(NUM_DECK_SAVE_MACHINE_SLOTS * 2u), wMachineDeckPtrs_ADDR);
	uint16_t d = wMachineDeckPtrs_ADDR;
	uint16_t h = sSavedDecks_ADDR;
	for (uint8_t i = 0; i < NUM_DECK_SAVE_MACHINE_SLOTS; i++) {
		gb_write8(d++, (uint8_t)h);
		gb_write8(d++, (uint8_t)(h >> 8));
		h = (uint16_t)(h + DECK_STRUCT_SIZE);
	}
	*hl = h;
	*de = d;
}
/* <<< factory GetSavedDeckPointers */

/* >>> factory GetSavedDeckCount */
/* deck_machine.asm:1070-1101. */
void GetSavedDeckCount(void)
{
	EnableSRAM();
	uint8_t count = 0;
	for (uint8_t i = 0; i < NUM_DECK_SAVE_MACHINE_SLOTS; i++) {
		uint16_t hl = (uint16_t)(sSavedDecks_ADDR + i * DECK_STRUCT_SIZE);
		if (gb_read8(hl) != 0)
			count++;
	}
	wNumSavedDecks = count;
	DisableSRAM();
}
/* <<< factory GetSavedDeckCount */

/* >>> factory GetSelectedSavedDeckPtr */
/* deck_machine.asm:1205-1224. */
uint16_t GetSelectedSavedDeckPtr(void)
{
	uint8_t index = gb_read8(wSelectedDeckMachineEntry_ADDR);
	uint16_t offset = (uint16_t)((uint8_t)(index << 1));
	uint16_t hl = (uint16_t)(wMachineDeckPtrs_ADDR + offset);
	uint8_t low = gb_read8(hl);
	uint8_t high = gb_read8((uint16_t)(hl + 1u));
	return (uint16_t)(low | ((uint16_t)high << 8));
}
/* <<< factory GetSelectedSavedDeckPtr */

/* >>> factory SafelySwitchToSRAM0 */
/* deck_machine.asm:1247-1261. */
void SafelySwitchToSRAM0(void)
{
	uint8_t bank = hBankSRAM;
	if (bank != 0u) {
		wTempBankSRAM = bank;
		BankswitchSRAM(0u);
	}
}
/* <<< factory SafelySwitchToSRAM0 */

/* >>> factory DrawListScrollArrows */
void DrawListScrollArrows(void)
{
	uint8_t tile;
	if (wCardListVisibleOffset != 0u)
		tile = SYM_CURSOR_U;
	else
		tile = SYM_BOX_RIGHT;
	WriteByteToBGMap0(tile, 19u, 1u);

	uint8_t threshold = (uint8_t)(wCardListVisibleOffset + NUM_DECK_MACHINE_VISIBLE_DECKS + 1u);
	if (wNumDeckMachineEntries < threshold) {
		wUnableToScrollDown = TRUE;
		tile = SYM_BOX_RIGHT;
	} else {
		wUnableToScrollDown = FALSE;
		tile = SYM_CURSOR_D;
	}
	WriteByteToBGMap0(tile, 19u, 11u);
}
/* <<< factory DrawListScrollArrows */

/* >>> factory SetDeckMachineTitleText */
SetDeckMachineTitleTextResult SetDeckMachineTitleText(void)
{
	InitTextPrinting(1u, 0u);
	uint16_t hl = (uint16_t)(gb_read8(wDeckMachineTitleText_ADDR) | ((uint16_t)gb_read8((uint16_t)(wDeckMachineTitleText_ADDR + 1u)) << 8));
	ProcessTextHeaderResult r = ProcessTextFromID(hl);
	return (SetDeckMachineTitleTextResult){r.hl};
}
/* <<< factory SetDeckMachineTitleText */

/* >>> factory FindFirstEmptyDeckSlot */
FindFirstEmptyDeckSlotResult FindFirstEmptyDeckSlot(void)
{
	uint16_t hl = 0xA218u;
	uint8_t a = gb_read8(hl);
	if (a == 0u)
		return (FindFirstEmptyDeckSlotResult){0u, 0x80u, hl};
	hl = 0xA26Cu;
	a = gb_read8(hl);
	if (a == 0u)
		return (FindFirstEmptyDeckSlotResult){1u, 0x80u, hl};
	hl = 0xA2C0u;
	a = gb_read8(hl);
	if (a == 0u)
		return (FindFirstEmptyDeckSlotResult){2u, 0x80u, hl};
	hl = 0xA314u;
	a = gb_read8(hl);
	if (a == 0u)
		return (FindFirstEmptyDeckSlotResult){3u, 0x80u, hl};
	return (FindFirstEmptyDeckSlotResult){a, 0x10u, hl};
}
/* <<< factory FindFirstEmptyDeckSlot */

/* >>> factory EmptyScreenAndDrawTextBox */
void EmptyScreenAndDrawTextBox(void)
{
	Set_OBJ_8x8();
	PrepareMenuGraphics();
	uint16_t hl = 0xc600u;
	DrawRegularTextBox(&hl, 0u, 20u, 13u, 0u, 0u);
}
/* <<< factory EmptyScreenAndDrawTextBox */

/* >>> factory PrintCardToSendText */
void PrintCardToSendText(void)
{
	EmptyScreenAndDrawTextBox();
	InitTextPrinting(1u, 1u);
	ProcessTextFromID(CardToSendText);
}
/* <<< factory PrintCardToSendText */

/* >>> factory PrintReceivedTheseCardsText */
void PrintReceivedTheseCardsText(void)
{
	EmptyScreenAndDrawTextBox();
	InitTextPrinting(1u, 1u);
	ProcessTextFromID(CardReceivedText);
	uint16_t hl = wNameBuffer_ADDR;
	uint16_t de = wDefaultText_ADDR;
	CopyListFromHLToDE(&hl, &de);
	gb_write8(wTxRam2_ADDR, 0u);
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), 0u);
	DrawWideTextBox_PrintText(ReceivedTheseCardsFromText);
}
/* <<< factory PrintReceivedTheseCardsText */

/* >>> factory PrintNumSavedDecks */
void PrintNumSavedDecks(void)
{
	uint8_t num = wNumSavedDecks;
	uint16_t hl = wDefaultText_ADDR;
	ConvertToNumericalDigitsResult r1 = ConvertToNumericalDigits(num, hl);
	hl = r1.hl;
	gb_write8(hl, TX_SYMBOL);
	hl = (uint16_t)(hl + 1u);
	gb_write8(hl, SYM_SLASH);
	hl = (uint16_t)(hl + 1u);
	ConvertToNumericalDigitsResult r2 = ConvertToNumericalDigits(NUM_DECK_SAVE_MACHINE_SLOTS, hl);
	hl = r2.hl;
	gb_write8(hl, TX_END);
	InitTextPrinting(14u, 1u);
	uint16_t text_hl = wDefaultText_ADDR;
	ProcessText(&text_hl);
}
/* <<< factory PrintNumSavedDecks */

/* >>> factory Func_b568 */
void Func_b568(void)
{
	uint8_t b = wCardListCursorPos;
	uint8_t a = (uint8_t)(wCardListVisibleOffset + b + 1u);
	uint16_t hl = wDefaultText_ADDR;
	ConvertToNumericalDigitsResult r1 = ConvertToNumericalDigits(a, hl);
	hl = r1.hl;
	gb_write8(hl, TX_SYMBOL);
	hl = (uint16_t)(hl + 1u);
	gb_write8(hl, SYM_SLASH);
	hl = (uint16_t)(hl + 1u);
	uint8_t num_saved = wNumSavedDecks;
	ConvertToNumericalDigitsResult r2 = ConvertToNumericalDigits(num_saved, hl);
	hl = r2.hl;
	gb_write8(hl, TX_END);
	InitTextPrinting(14u, 1u);
	uint16_t text_hl = wDefaultText_ADDR;
	ProcessText(&text_hl);
}
/* <<< factory Func_b568 */
