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

#include "home/deck_machine.h"
#include "home/deck_configuration.h"
#define WMACHINEDECKPTRS_ADDR 0xD00Du

#include "home/deck_machine.h"
#include "home/deck_configuration.h"
#include "home/process_text.h"
#include "home/print_text.h"
#define EmptyDeckNameText 0x025bu
#define PRINT_DECK_MACHINE_ENTRY_TEXT_ADDR 0x74D4u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/deck_configuration.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "mem.h"

#include "home/deck_machine.h"
#include "home/deck_configuration.h"
#include "home/card_data.h"
#include "generated/wram.h"
#define CARD_COLLECTION_SIZE 0x100u
#define FILTER_ENERGY 0x20u
#define TYPE_ENERGY 0x08u
#define FUNC_B088_CARD_LIMIT 0xe4u

#include "home/deck_configuration.h"
#include "home/menus.h"
#include "home/switch_sram.h"
#include "generated/wram.h"
#define DeletedTheConfigurationForText 0x0267u
#define DoYouReallyWishToDeleteText 0x0266u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/deck_check.h"
#include "home/deck_configuration.h"
#include "home/deck_selection.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/menus.h"
#include "home/process_text.h"
#include "mem.h"

#define NUM_FILTERS 0x09u
#define MENU_CANCEL 0xFFu
#define MENU_CONFIRM 0x01u
#define PAD_START 0x08u
#define CARRY_FLAG 0x10u
#define NUM_CONFIRMATION_CURSOR_POSITIONS 0x05u
/* charmaps.asm:319 gives the fullwidth middle dot the value $77 and
 * macros/text.asm:81-89 shows `ldfw` is a plain `ld`, so deck_machine.asm:143
 * assembles to `ld [hl], $77`. */
#define FW_MIDDLE_DOT 0x77u
/* Bank-2 addresses this routine reads as data (poketcg.sym):
 * 02:52a7 DeckNameSuffix,
 * 02:6e91 HandleDeckMissingCardsList.DeckConfirmationCardSelectionParams,
 * 02:6e9a HandleDeckMissingCardsList.CardListUpdateFunction. */
#define DeckNameSuffix_ADDR 0x52A7u
#define DECK_CONFIRMATION_CARD_SELECTION_PARAMS_ADDR 0x6E91u
#define CARD_LIST_UPDATE_FUNCTION_ADDR 0x6E9Au

#define ALL_DECKS 0xffu
#define ChooseADeckToDismantleText 0x0269u
#define DismantleThisDeckText 0x023du
#define DismantledDeckText 0x026au
#define YouMayOnlyCarry4DecksText 0x0268u

#include "home/deck_machine.h"
#include "generated/wram.h"

#include "home/text_box.h"
#include "home/credits_sequence_commands.h"
#include "home/lcd.h"
#include "home/tiles.h"
#include "home/duel_core.h"
#include "home/process_text.h"
#include "home/objects.h"

#include "home/deck_machine.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "home/deck_machine.h"
#include "home/deck_configuration.h"
#include "home/deck_selection.h"
#include "home/deck_check.h"
#include "home/frames.h"
#include "home/sound.h"
#include "home/switch_sram.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#define SFX_CURSOR 0x01u
#define PAD_RIGHT 0x10u
#define PAD_LEFT 0x20u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/deck_configuration.h"
#include "home/deck_machine.h"
#include "home/deck_selection.h"
#include "home/frames.h"
#include "home/menus.h"
#include "home/switch_sram.h"
#include "mem.h"
#define ChooseADeckToSaveText 0x0260u
#define SavedTheConfigurationForText 0x0263u

#include "home/deck_machine.h"
#include "home/auto_deck_machines.h"
#include "home/deck_configuration.h"
#include "home/deck_selection.h"
#include "home/menus.h"
#include "home/random.h"
#include "home/switch_sram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "mem.h"

#define CARD_COUNT_MASK 0x7fu
#define DECK_1_F 0x00u
#define DECK_2_F 0x01u
#define DECK_3_F 0x02u
#define DECK_4_F 0x03u
#define BuiltDeckText 0x026eu
#define DismantleTheseDecksText 0x0270u
#define DismantledTheDeckText 0x0271u
#define TheseCardsAreNeededToBuildThisDeckText 0x026fu
#define ThisDeckCanOnlyBeBuiltIfYouDismantleText 0x026cu
#define YouDoNotOwnAllCardsNeededToBuildThisDeckText 0x026du
/* poketcg.sym: 02:7609 DeckMachineMenuParameters. */
#define DECK_MACHINE_MENU_PARAMETERS_ADDR 0x7609u

#include "home/auto_deck_machines.h"
#include "home/credits_sequence_commands.h"
#include "home/deck_check.h"
#include "home/deck_configuration.h"
#include "home/deck_machine.h"
#include "home/deck_selection.h"
#include "home/duel.h"
#include "home/duel_core.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/menus.h"
#include "home/objects.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "home/text_box.h"
#include "home/tiles.h"
#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "mem.h"

#define PleaseSelectDeckText 0x0224u
/* poketcg.sym, every one of these in bank 2:
 *   02:7b6e HandleAutoDeckMenu.MenuParameters
 *   02:7b76 HandleAutoDeckMenu.DeckMachineMenuData
 *   02:7b83 HandleAutoDeckMenu.DeckMachineTitleTextList
 *   02:73fe UpdateDeckMachineScrollArrowsAndEntries
 * The first two are handed to InitializeMenuParameters/PlaceTextItems, which
 * read them off the bus, so the case has to map bank 2; the title list is read
 * with an explicit rom_ptr() because it is this routine's own data. */
#define HANDLE_AUTO_DECK_MENU_BANK 0x02u
#define HANDLE_AUTO_DECK_MENU_MENU_PARAMETERS_ADDR 0x7B6Eu
#define HANDLE_AUTO_DECK_MENU_MENU_DATA_ADDR 0x7B76u
#define HANDLE_AUTO_DECK_MENU_TITLE_TEXT_LIST_ADDR 0x7B83u
#define UPDATE_DECK_MACHINE_SCROLL_ARROWS_ADDR 0x73FEu

#include "generated/wram.h"
#include "mem.h"
#define DRAW_DECK_MACHINE_SCREEN_ADDR 0x7403u
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

/* >>> factory CheckIfCanBuildSavedDeck */
DeckBuildCheckResult CheckIfCanBuildSavedDeck(uint8_t a, uint8_t b)
{
	SafelySwitchToSRAM0();
	CreateCardCollectionListWithDeckCards(a);
	SafelySwitchToTempSRAMBank();
	uint8_t c = (uint8_t)(b << 1);
	uint16_t hl = (uint16_t)(WMACHINEDECKPTRS_ADDR + c);
	uint16_t ptr = (uint16_t)(gb_read8(hl) | (uint16_t)gb_read8((uint16_t)(hl + 1u)) << 8);
	ptr = (uint16_t)(ptr + DECK_NAME_SIZE);
	DeckBuildCheckResult r = CheckIfHasEnoughCardsToBuildDeck(&ptr);
	return r;
}
/* <<< factory CheckIfCanBuildSavedDeck */

/* >>> factory PrintDeckMachineEntry */
PrintDeckMachineEntryResult PrintDeckMachineEntry(uint8_t a, uint8_t d, uint8_t e)
{
	uint8_t deck_index = a;
	uint16_t hl = wDefaultText_ADDR;
	uint8_t num = (uint8_t)(a + 1u);
	ConvertToNumericalDigitsResult cd = ConvertToNumericalDigits(num, hl);
	hl = cd.hl;
	gb_write8(hl, 0x77u);
	hl = (uint16_t)(hl + 1u);
	gb_write8(hl, TX_END);
	InitTextPrinting(d, e);
	hl = wDefaultText_ADDR;
	ProcessText(&hl);

	uint16_t table_addr = (uint16_t)(wMachineDeckPtrs_ADDR + (uint16_t)((uint8_t)(deck_index << 1)));
	uint16_t ptr = (uint16_t)(gb_read8(table_addr) | (uint16_t)gb_read8((uint16_t)(table_addr + 1u)) << 8);

	uint8_t d2 = (uint8_t)(d + 3u);
	uint8_t af_result = AppendDeckName(ptr, d2, e);
	if (af_result & 0x10u) {
		InitTextPrinting(d2, e);
		(void)ProcessTextFromID(EmptyDeckNameText);
		uint8_t e2 = (uint8_t)(e + 1u);
		InitTextPrinting(13u, e2);
		uint16_t text_hl = PRINT_DECK_MACHINE_ENTRY_TEXT_ADDR;
		ProcessText(&text_hl);
		return (PrintDeckMachineEntryResult){0u, 0x90u};
	}

	return (PrintDeckMachineEntryResult){0u, 0u};
}
/* <<< factory PrintDeckMachineEntry */

/* >>> factory ShowReceivedCardsList */
void ShowReceivedCardsList(void)
{
	gb_write8(hffb0_ADDR, 0x01u);
	InitTextPrinting(1u, 1u);
	(void)ProcessTextFromID(CardReceivedText);
	uint16_t hl = wNameBuffer_ADDR;
	uint16_t de = wDefaultText_ADDR;
	CopyListFromHLToDE(&hl, &de);
	gb_write8(wTxRam2_ADDR, 0x00u);
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), 0x00u);
	InitTextPrinting(1u, 14u);
	(void)PrintTextNoDelay(ReceivedTheseCardsFromText, 1u, 14u);
	gb_write8(hffb0_ADDR, 0x00u);
	PrintCardSelectionList();
}
/* <<< factory ShowReceivedCardsList */

/* >>> factory Func_b088 */
Func_b088Result Func_b088(void)
{
	ClearMemory_Bank2((uint8_t)(CARD_COLLECTION_SIZE - 1u), wTempCardCollection_ADDR);

	uint16_t de = wDuelTempList_ADDR;
	for (;;) {
		uint8_t card = gb_read8(de);
		de = (uint16_t)(de + 1u);
		if (card == 0u)
			break;
		uint16_t slot = (uint16_t)(wTempCardCollection_ADDR + card);
		gb_write8(slot, (uint8_t)(gb_read8(slot) + 1u));
	}

	ClearMemory_Bank2(DECK_SIZE, wOwnedCardsCountList_ADDR);
	ClearMemory_Bank2(DECK_SIZE, wFilteredCardList_ADDR);
	uint8_t out = 0u;
	for (uint16_t id = 1u; id <= FUNC_B088_CARD_LIMIT; id++) {
		uint8_t card_id = (uint8_t)id;
		uint8_t card_type = GetCardType(card_id);
		gb_write8((uint16_t)(wFilteredCardList_ADDR + out), card_id);
		uint8_t owned = (uint8_t)(gb_read8((uint16_t)(wTempCardCollection_ADDR + card_id)) & 0x7fu);
		if (owned != 0u) {
			gb_write8((uint16_t)(wOwnedCardsCountList_ADDR + out), owned);
			out = (uint8_t)(out + 1u);
		}
		(void)card_type;
	}
	wNumEntriesInCurFilter = out;
	gb_write8((uint16_t)(wFilteredCardList_ADDR + out), 0u);
	gb_write8((uint16_t)(wOwnedCardsCountList_ADDR + out), 0xffu);
	wNumVisibleCardListEntries = 5u;
	wCardListCoords = 3u;
	gb_write8((uint16_t)(wCardListCoords_ADDR + 1u), 2u);
	wCursorAlternateTile = SYM_BOX_RIGHT;
	PrintCardSelectionList();
	uint8_t a = SYM_BOX_RIGHT;
	uint8_t f = 0x40u;
	return (Func_b088Result){a, f};
}
/* <<< factory Func_b088 */

/* >>> factory TryDeleteSavedDeck */
TryDeleteSavedDeckResult TryDeleteSavedDeck(void)
{
	HandleYesOrNoMenuResult choice = YesOrNoMenuWithText(DoYouReallyWishToDeleteText);
	if (choice.f & 0x10u) {
		uint8_t cursor = wCardListCursorPos;
		return (TryDeleteSavedDeckResult){cursor, (uint8_t)((choice.f & 0x80u) | 0x10u)};
	}
	uint16_t deck = GetSelectedSavedDeckPtr();
	EnableSRAM();
	(void)CopyDeckName(deck);
	ClearMemory_Bank2(DECK_STRUCT_SIZE, deck);
	DisableSRAM();
	gb_write8(wTxRam2_ADDR, 0u);
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), 0u);
	WaitResult waited = DrawWideTextBox_WaitForInput(DeletedTheConfigurationForText);
	return (TryDeleteSavedDeckResult){0u, waited.f};
}
/* <<< factory TryDeleteSavedDeck */

/* >>> factory HandleDeckMissingCardsList */
/* deck_machine.asm:6-165. hl = the deck's name in SRAM, de = its 60 card ids.
 * The `call .HandleList / ret` tail is inlined: .HandleList has a single exit,
 * the `ret z` in .selection_made, so every return leaves a = [hffb3] =
 * MENU_CANCEL and f = $C0 (`cp` against an equal value sets Z and N and clears
 * H and C).
 *
 * .CardListUpdateFunction is stored, never called here: the asm only parks its
 * address in wCardListUpdateFunction for CallIndirect, and this tree does not
 * dispatch that pointer (see the note on HandleLeftRightInCardList in
 * src/home/deck_configuration.c). The two bytes written are the real bank-2
 * address, so the WRAM still matches the reference. */
HandleDeckMissingCardsListResult HandleDeckMissingCardsList(uint16_t hl, uint16_t de)
{
	(void)CopyListFromHLToDEInSRAM(hl, wCurDeckName_ADDR);
	(void)CopyDeckFromSRAM(de, wCurDeckCards_ADDR);

	ClearMemory_Bank2(NUM_FILTERS, wCardFilterCounts_ADDR);
	wTotalCardCount = DECK_SIZE;
	wCardFilterCounts = DECK_SIZE;

	/* .HandleList */
	(void)SortCurDeckCardsByID();
	(void)CreateCurDeckUniqueCardList();
	wCardListVisibleOffset = 0u;

	/* The `xor a` above is the cursor .loop hands InitCardSelectionParams on
	 * first entry; the `jr .loop` from .open_card_pge re-enters with the a
	 * OpenCardPageFromCardList's .exit leaves, [wCardListCursorPos]
	 * (deck_configuration.asm:2085-2089). */
	uint8_t cursor = 0u;

	for (;;) { /* .loop */
		uint16_t params = DECK_CONFIRMATION_CARD_SELECTION_PARAMS_ADDR;

		(void)InitCardSelectionParams(cursor, &params);

		uint8_t entries = wNumUniqueCards;

		wNumCardListEntries = entries;
		if (entries >= NUM_CONFIRMATION_CURSOR_POSITIONS)
			entries = NUM_CONFIRMATION_CURSOR_POSITIONS;
		wCardListNumCursorPositions = entries;
		wNumVisibleCardListEntries = entries;

		/* .PrintTitleAndList -> .ClearScreenAndPrintDeckTitle */
		EmptyScreenAndLoadFontDuelAndHandCardsIcons();
		if (wCurDeckName != 0u) { /* .PrintDeckIndexAndName */
			InitTextPrinting(0u, 1u);

			ConvertToNumericalDigitsResult digits =
				ConvertToNumericalDigits((uint8_t)(wCurDeck + 1u),
							 wDefaultText_ADDR);

			gb_write8(digits.hl, FW_MIDDLE_DOT);
			gb_write8((uint16_t)(digits.hl + 1u), TX_END);

			uint16_t text = wDefaultText_ADDR;

			ProcessText(&text);

			uint16_t name = wCurDeckName_ADDR;
			uint16_t name_dst = wDefaultText_ADDR;

			CopyListFromHLToDE(&name, &name_dst);

			/* `ld b, $0 / add hl, bc` appends the suffix at the tile
			 * length GetTextLengthInTiles returns in c. */
			TextLength length = GetTextLengthInTiles(wDefaultText_ADDR);
			uint16_t suffix = DeckNameSuffix_ADDR;
			uint16_t suffix_dst = (uint16_t)(wDefaultText_ADDR + length.c);

			CopyListFromHLToDE(&suffix, &suffix_dst);
			InitTextPrinting(3u, 1u);
			text = wDefaultText_ADDR;
			ProcessText(&text);
		}
		EnableLCD();

		wCardListCoords = 3u;
		gb_write8((uint16_t)(wCardListCoords_ADDR + 1u), 3u);
		/* PrintConfirmationCardList takes its coordinates from
		 * wCardListCoords and ignores a, de and hl, so the asm's
		 * `lb de, 3, 3` and wCardListCoords pointer carry no state. */
		PrintConfirmationCardList(0u, 3u, 3u, (uint16_t *)0);

		uint16_t confirmation = (uint16_t)(wCardConfirmationText
			| ((uint16_t)gb_read8((uint16_t)(wCardConfirmationText_ADDR + 1u)) << 8));

		(void)DrawWideTextBox_PrintText(confirmation);

		gb_write8(wCardListUpdateFunction_ADDR, (uint8_t)CARD_LIST_UPDATE_FUNCTION_ADDR);
		gb_write8((uint16_t)(wCardListUpdateFunction_ADDR + 1u),
			  (uint8_t)(CARD_LIST_UPDATE_FUNCTION_ADDR >> 8));
		wced2 = 0u;

		for (;;) { /* .loop_input */
			DoFrame();
			if (HandleDeckCardSelectionList().f & CARRY_FLAG) {
				uint8_t selected = hffb3; /* .selection_made */

				if (selected == MENU_CANCEL)
					return (HandleDeckMissingCardsListResult){selected, 0xC0u};
				break;
			}
			if (HandleLeftRightInCardList().f & CARRY_FLAG)
				continue;
			if (hDPadHeld & PAD_START)
				break;
		}

		/* .open_card_pge */
		PlaySFXConfirmOrCancel(MENU_CONFIRM);
		wced7 = wCardListCursorPos;
		gb_write8(wCurCardListPtr_ADDR, (uint8_t)wUniqueDeckCardList_ADDR);
		gb_write8((uint16_t)(wCurCardListPtr_ADDR + 1u),
			  (uint8_t)(wUniqueDeckCardList_ADDR >> 8));
		OpenCardPageFromCardList();
		cursor = wCardListCursorPos;
	}
}
/* <<< factory HandleDeckMissingCardsList */

/* >>> factory HandleDismantleDeckToMakeSpace */
HandleDismantleDeckToMakeSpaceResult HandleDismantleDeckToMakeSpace(void)
{
	WaitResult initial_wait = DrawWideTextBox_WaitForInput(YouMayOnlyCarry4DecksText);
	(void)initial_wait;

	SafelySwitchToSRAM0();
	DrawDecksScreen(ALL_DECKS);

	uint8_t cursor = 0u;
	for (;;) {
		uint16_t menu_parameters = 0x7609u;
		InitializeMenuParameters(cursor, &menu_parameters);
		(void)DrawWideTextBox_PrintText(ChooseADeckToDismantleText);

		for (;;) {
			DoFrame();
			HandleStartButtonInDeckSelectionMenuResult start =
				HandleStartButtonInDeckSelectionMenu();
			if ((start.f & 0x10u) != 0u) {
				cursor = start.a;
				break;
			}

			HandleMenuInputResult input = HandleMenuInput();
			if ((input.f & 0x10u) == 0u)
				continue;
			if (hCurMenuItem == MENU_CANCEL) {
				SafelySwitchToTempSRAMBank();
				return (HandleDismantleDeckToMakeSpaceResult){hCurMenuItem, 0x90u};
			}

			wCurDeck = hCurMenuItem;
			HandleYesOrNoMenuResult choice =
				YesOrNoMenuWithText(DismantleThisDeckText);
			if ((choice.f & 0x10u) != 0u) {
				cursor = wCurDeck;
				break;
			}

			uint16_t deck_name = GetPointerToDeckName();
			uint16_t source = deck_name;
			uint16_t destination = wDismantledDeckName_ADDR;
			EnableSRAM();
			CopyListFromHLToDE(&source, &destination);
			(void)AddDeckToCollection((uint16_t)(deck_name + DECK_NAME_SIZE));
			ClearMemory_Bank2(DECK_STRUCT_SIZE, deck_name);
			DisableSRAM();

			DrawDecksScreen(ALL_DECKS);
			cursor = wCurDeck;
			menu_parameters = 0x7609u;
			InitializeMenuParameters(cursor, &menu_parameters);
			DrawCursor2();
			SafelySwitchToTempSRAMBank();
			(void)CopyDeckName(wDismantledDeckName_ADDR);
			wTxRam2 = 0u;
			gb_write8((uint16_t)(wTxRam2_ADDR + 1u), 0u);
			WaitResult final_wait =
				DrawWideTextBox_WaitForInput(DismantledDeckText);
			return (HandleDismantleDeckToMakeSpaceResult){wCurDeck, final_wait.f};
		}
	}
}
/* <<< factory HandleDismantleDeckToMakeSpace */

/* >>> factory PrintVisibleDeckMachineEntries */
PrintVisibleDeckMachineEntriesResult PrintVisibleDeckMachineEntries(uint8_t f)
{
	uint8_t a = wCardListVisibleOffset;
	uint8_t b = NUM_DECK_MACHINE_VISIBLE_DECKS;
	uint8_t e = 2u;
	for (;;) {
		(void)PrintDeckMachineEntry(a, 2u, e);
		if (f & 0x10u)
			return (PrintVisibleDeckMachineEntriesResult){a, f};
		b--;
		if (b == 0u)
			return (PrintVisibleDeckMachineEntriesResult){a, (uint8_t)((f & 0x10u) | 0xE0u)};
		a++;
		e = (uint8_t)(e + 2u);
	}
}
/* <<< factory PrintVisibleDeckMachineEntries */

/* >>> factory ClearScreenAndDrawDeckMachineScreen */
void ClearScreenAndDrawDeckMachineScreen(void)
{
	Set_OBJ_8x8();
	wTileMapFill = 0u;
	ZeroObjectPositions();
	EmptyScreen();
	wVBlankOAMCopyToggle = TRUE;
	(void)LoadSymbolsFont();
	(void)LoadDuelCardSymbolTiles();
	SetDefaultConsolePalettes();
	(void)SetupText(0x3Cu, 0xFFu);
	uint16_t hl = 0u;
	DrawRegularTextBox(&hl, 0u, 20u, 13u, 0u, 0u);
	(void)SetDeckMachineTitleText();
	uint16_t de = 0u;
	GetSavedDeckPointers(&hl, &de);
	(void)PrintVisibleDeckMachineEntries(0u);
	GetSavedDeckCount();
	EnableLCD();
}
/* <<< factory ClearScreenAndDrawDeckMachineScreen */

/* >>> factory DrawDeckMachineScreen */
DrawDeckMachineScreenResult DrawDeckMachineScreen(void)
{
	DrawListScrollArrows();
	hffb0 = 0x01u;
	(void)SetDeckMachineTitleText();
	InitTextPrinting(1u, 14u);
	uint16_t text = (uint16_t)(gb_read8(wDeckMachineText_ADDR)
		| ((uint16_t)gb_read8((uint16_t)(wDeckMachineText_ADDR + 1u)) << 8));
	ProcessTextHeaderResult text_result = ProcessTextFromID(text);
	hffb0 = 0x00u;
	PrintVisibleDeckMachineEntriesResult entries =
		PrintVisibleDeckMachineEntries(text_result.f);
	if (!(text_result.f & 0x10u) && entries.f == 0xE0u)
		entries.f = 0xC0u;
	return (DrawDeckMachineScreenResult){entries.a, entries.f};
}
/* <<< factory DrawDeckMachineScreen */

/* >>> factory HandleDeckMachineSelection */
HandleDeckMachineSelectionResult HandleDeckMachineSelection(void)
{
	for (;;) {
		DoFrame();
		HandleDeckCardSelectionListResult r = HandleDeckCardSelectionList();
		if (r.f & CARRY_FLAG) {
			DrawListCursor_Visible();
			wTempCardListVisibleOffset = wCardListVisibleOffset;
			wTempDeckMachineCursorPos = wCardListCursorPos;
			uint8_t v = hffb3;
			return (HandleDeckMachineSelectionResult){v, v ? 0u : 0x80u};
		}
		uint8_t held = hDPadHeld;
		uint8_t old = wCardListVisibleOffset;
		if (held == PAD_RIGHT || held == PAD_LEFT) {
			uint8_t next = old;
			if (held == PAD_RIGHT) { next = (uint8_t)(old + NUM_DECK_MACHINE_SLOTS); if ((uint8_t)(next + NUM_DECK_MACHINE_SLOTS) >= wNumDeckMachineEntries) next = (uint8_t)(wNumDeckMachineEntries - NUM_DECK_MACHINE_SLOTS); }
			else if (old >= NUM_DECK_MACHINE_SLOTS) next = (uint8_t)(old - NUM_DECK_MACHINE_SLOTS);
			wCardListVisibleOffset = next;
			if (next != old) { PlaySFX(SFX_CURSOR); DrawDeckMachineScreen(); PrintNumSavedDecks(); }
			continue;
		}
		if (!(held & PAD_START)) continue;
		wTempCardListVisibleOffset = wCardListVisibleOffset;
		wTempDeckMachineCursorPos = wCardListCursorPos;
		uint8_t i = (uint8_t)(wCardListVisibleOffset + wCardListCursorPos);
		wCurDeck = (uint8_t)((i + 1u) | 0x80u);
		uint16_t p = (uint16_t)(wMachineDeckPtrs_ADDR + (uint16_t)i * 2u);
		uint16_t deck = (uint16_t)(gb_read8(p) | ((uint16_t)gb_read8((uint16_t)(p + 1u)) << 8));
		EnableSRAM(); uint8_t n = gb_read8((uint16_t)(deck + DECK_NAME_SIZE)); DisableSRAM();
		if (!n) continue;
		PlaySFXConfirmOrCancel(MENU_CONFIRM); OpenDeckConfirmationMenu((uint16_t)(deck + DECK_NAME_SIZE), deck);
		wCardListVisibleOffset = wTempCardListVisibleOffset;
		ClearScreenAndDrawDeckMachineScreen(); DrawListScrollArrows(); PrintNumSavedDecks();
		wCardListCursorPos = wTempDeckMachineCursorPos;
		return (HandleDeckMachineSelectionResult){0u, CARRY_FLAG};
	}
}
/* <<< factory HandleDeckMachineSelection */

/* >>> factory UpdateDeckMachineScrollArrowsAndEntries */
PrintVisibleDeckMachineEntriesResult UpdateDeckMachineScrollArrowsAndEntries(uint8_t f)
{
	(void)f;
	DrawListScrollArrows();
	uint8_t visible_offset = wCardListVisibleOffset;
	uint8_t threshold = (uint8_t)(visible_offset + NUM_DECK_MACHINE_VISIBLE_DECKS + 1u);
	uint8_t entries = wNumDeckMachineEntries;
	uint8_t draw_f;
	if (entries < threshold) {
		draw_f = 0x50u;
		if ((uint8_t)(entries & 0x0Fu) < (uint8_t)(threshold & 0x0Fu))
			draw_f |= 0x20u;
	} else {
		draw_f = 0x80u;
	}
	return PrintVisibleDeckMachineEntries(draw_f);
}
/* <<< factory UpdateDeckMachineScrollArrowsAndEntries */

/* >>> factory SaveDeckInDeckSaveMachine */
SaveDeckInDeckSaveMachineResult SaveDeckInDeckSaveMachine(void)
{
	uint8_t a = 0u;
	DrawDecksScreen(ALL_DECKS);
	for (;;) {
		uint16_t menu_parameters = 0x7609u;
		InitializeMenuParameters(a, &menu_parameters);
		(void)DrawWideTextBox_PrintText(ChooseADeckToSaveText);
		for (;;) {
			DoFrame();
			HandleStartButtonInDeckSelectionMenuResult start =
				HandleStartButtonInDeckSelectionMenu();
			if ((start.f & 0x10u) != 0u) {
				a = start.a;
				break;
			}
			HandleMenuInputResult input = HandleMenuInput();
			if ((input.f & 0x10u) == 0u)
				continue;
			a = hCurMenuItem;
			if (a == MENU_CANCEL)
				return (SaveDeckInDeckSaveMachineResult){a, 0xc0u};
			wCurDeck = a;
			CheckIfCurDeckIsValidResult valid = CheckIfCurDeckIsValid();
			if ((valid.f & 0x10u) != 0u) {
				(void)PrintThereIsNoDeckHereText();
				a = wCurDeck;
				break;
			}
			uint16_t source = GetPointerToDeckName();
			uint16_t destination = GetSelectedSavedDeckPtr();
			EnableSRAM();
			CopyNBytesFromHLToDE(&source, &destination, DECK_STRUCT_SIZE);
			DisableSRAM();
			ClearScreenAndDrawDeckMachineScreen();
			DrawListScrollArrows();
			PrintNumSavedDecks();
			uint8_t list_cursor = wTempDeckMachineCursorPos;
			uint16_t selection_parameters = 0x76fbu;
			(void)InitCardSelectionParams(list_cursor, &selection_parameters);
			(void)DrawListCursor_Visible();
			source = GetPointerToDeckName();
			EnableSRAM();
			(void)CopyDeckName(source);
			DisableSRAM();
			a = 0u;
			wTxRam2 = 0u;
			gb_write8((uint16_t)(wTxRam2_ADDR + 1u), 0u);
			WaitResult waited = DrawWideTextBox_WaitForInput(SavedTheConfigurationForText);
			uint8_t f = (uint8_t)((waited.f & 0x80u) | 0x10u);
			return (SaveDeckInDeckSaveMachineResult){a, f};
		}
	}
}
/* <<< factory SaveDeckInDeckSaveMachine */

/* >>> factory TryBuildDeckMachineDeck */
/* deck_machine.asm:1509-1720. The local labels are inlined; .DismantleDeck
 * and .CheckIfCardIsMissing become static helpers.
 *
 * .CheckIfCardIsMissing's `scf / ret z` never returns: the branch is only
 * reached when the collection count is below the deck count, so `sub e` is
 * never zero and control falls through into .GetCardCountFromDeck. That tail
 * pushes af, walks wTempCardCollection + card id to the first zero byte and
 * pops af back, writing nothing and restoring both a and the carry, so it is
 * invisible to every caller and is not reproduced here. */
typedef struct { uint8_t a; uint8_t missing; } TbdmdMissing;

/* .DismantleDeck: a = DECK_*_F. */
static void tbdmd_dismantle_deck(uint8_t deck)
{
	uint16_t hl = HtimesL((uint16_t)(((uint16_t)DECK_STRUCT_SIZE << 8) | deck));
	hl = (uint16_t)(hl + sBuiltDecks_ADDR);
	(void)AddDeckToCollection((uint16_t)(hl + DECK_NAME_SIZE));
	ClearMemory_Bank2(DECK_STRUCT_SIZE, hl);
}

/* .CheckIfCardIsMissing: `missing` is the asm's carry, `a` the difference it
 * reports when the collection is short. */
static TbdmdMissing tbdmd_check_if_card_is_missing(uint8_t card, uint16_t hl)
{
	uint8_t d = 0u;

	for (;;) { /* .loop_deck_cards */
		uint8_t id = gb_read8(hl);

		hl = (uint16_t)(hl + 1u);
		if (id == 0u)
			break;
		if (id == card)
			d = (uint8_t)(d + 1u);
	}

	uint8_t e = (uint8_t)(gb_read8((uint16_t)(wTempCardCollection_ADDR + card))
		& CARD_COUNT_MASK);

	if (e < d)
		return (TbdmdMissing){(uint8_t)(d - e), 1u};
	return (TbdmdMissing){e, 0u};
}

/* .DismantleDecksNeededToBuild: returns the flag byte left by its `scf` (the
 * player declined) or by its closing `or a` (the decks were dismantled). */
static uint8_t tbdmd_dismantle_decks_needed_to_build(void)
{
	CheckWhichDecksToDismantleToBuildSavedDeckResult chk =
		CheckWhichDecksToDismantleToBuildSavedDeck();

	/* SafelySwitchToSRAM0 preserves af, so DrawDecksScreen still receives the
	 * a the farcall returned. */
	SafelySwitchToSRAM0();
	DrawDecksScreen(chk.a);

	HandleYesOrNoMenuResult choice = YesOrNoMenuWithText(DismantleTheseDecksText);

	if (choice.f & CARRY_FLAG) {
		SafelySwitchToTempSRAMBank();
		return (uint8_t)((choice.f & 0x80u) | CARRY_FLAG);
	}

	EnableSRAM();
	if (wDecksToBeDismantled & (uint8_t)(1u << DECK_1_F))
		tbdmd_dismantle_deck(DECK_1_F);
	if (wDecksToBeDismantled & (uint8_t)(1u << DECK_2_F))
		tbdmd_dismantle_deck(DECK_2_F);
	if (wDecksToBeDismantled & (uint8_t)(1u << DECK_3_F))
		tbdmd_dismantle_deck(DECK_3_F);
	if (wDecksToBeDismantled & (uint8_t)(1u << DECK_4_F))
		tbdmd_dismantle_deck(DECK_4_F);
	DisableSRAM();

	DrawDecksScreen(wDecksToBeDismantled);
	SafelySwitchToTempSRAMBank();

	WaitResult waited = DrawWideTextBox_WaitForInput(DismantledTheDeckText);

	/* `or a` clears carry, N and H and takes Z from the byte the wait left in
	 * a, which is the zero TryDeleteSavedDeck models for the same tail. */
	return (uint8_t)(waited.f & 0x80u);
}

TryBuildDeckMachineDeckResult TryBuildDeckMachineDeck(void)
{
	uint8_t entry = wSelectedDeckMachineEntry;
	DeckBuildCheckResult check = CheckIfCanBuildSavedDeck(0x00u, entry);

	if (check.f & CARRY_FLAG) {
		check = CheckIfCanBuildSavedDeck(ALL_DECKS, entry);
		if (check.f & CARRY_FLAG) {
			/* .do_not_own_all_cards_needed */
			(void)DrawWideTextBox_WaitForInput(
				YouDoNotOwnAllCardsNeededToBuildThisDeckText);

			/* .ShowMissingCardList */
			wCurDeck = wSelectedDeckMachineEntry;

			uint16_t saved = GetSelectedSavedDeckPtr();
			uint16_t src = (uint16_t)(saved + DECK_NAME_SIZE);
			uint16_t dst = wCurDeckCards_ADDR;

			EnableSRAM();
			CopyNBytesFromHLToDE(&src, &dst, DECK_SIZE);
			DisableSRAM();
			gb_write8((uint16_t)(wCurDeckCards_ADDR + DECK_SIZE), 0u);

			(void)SortCurDeckCardsByID();
			(void)CreateCurDeckUniqueCardList();

			SafelySwitchToSRAM0();
			CreateCardCollectionListWithDeckCards(ALL_DECKS);
			SafelySwitchToTempSRAMBank();

			uint16_t list = wUniqueDeckCardList_ADDR;
			uint16_t out = wFilteredCardList_ADDR;

			for (;;) { /* .loop_deck_configuration */
				uint8_t card = gb_read8(list);

				list = (uint16_t)(list + 1u);
				if (card == 0u)
					break;

				TbdmdMissing missing =
					tbdmd_check_if_card_is_missing(card, wCurDeckCards_ADDR);

				if (!missing.missing)
					continue;

				uint8_t needed = missing.a;

				do { /* .loop_number_missing */
					gb_write8(out, card);
					out = (uint16_t)(out + 1u);
					needed = (uint8_t)(needed - 1u);
				} while (needed != 0u);
			}

			/* .finish_missing_card_list */
			gb_write8(out, 0u);

			gb_write8(wCardConfirmationText_ADDR, (uint8_t)TheseCardsAreNeededToBuildThisDeckText);
			gb_write8((uint16_t)(wCardConfirmationText_ADDR + 1u),
				  (uint8_t)(TheseCardsAreNeededToBuildThisDeckText >> 8));

			uint16_t name = GetSelectedSavedDeckPtr();
			HandleDeckMissingCardsListResult shown =
				HandleDeckMissingCardsList(name, wFilteredCardList_ADDR);

			/* .set_carry_and_return */
			return (TryBuildDeckMachineDeckResult){wCardListCursorPos,
				(uint8_t)((shown.f & 0x80u) | CARRY_FLAG)};
		}

		(void)DrawWideTextBox_WaitForInput(ThisDeckCanOnlyBeBuiltIfYouDismantleText);

		uint8_t dismantled = tbdmd_dismantle_decks_needed_to_build();

		if (dismantled & CARRY_FLAG) {
			/* .set_carry_and_return */
			return (TryBuildDeckMachineDeckResult){wCardListCursorPos,
				(uint8_t)((dismantled & 0x80u) | CARRY_FLAG)};
		}
	}

	/* .build_deck */
	EnableSRAM();
	SafelySwitchToSRAM0();

	FindFirstEmptyDeckSlotResult slot = FindFirstEmptyDeckSlot();

	SafelySwitchToTempSRAMBank();
	DisableSRAM();

	uint8_t deck_slot = slot.a;

	if (slot.f & CARRY_FLAG) {
		HandleDismantleDeckToMakeSpaceResult space = HandleDismantleDeckToMakeSpace();

		if (space.f & CARRY_FLAG)
			return (TryBuildDeckMachineDeckResult){space.a,
				(uint8_t)((space.f & 0x80u) | CARRY_FLAG)};
		deck_slot = space.a;
	}

	/* .got_deck_slot */
	wDeckSlotForNewDeck = deck_slot;

	uint16_t table = (uint16_t)(wMachineDeckPtrs_ADDR
		+ (uint8_t)(wSelectedDeckMachineEntry << 1));
	uint16_t deck = (uint16_t)(gb_read8(table)
		| ((uint16_t)gb_read8((uint16_t)(table + 1u)) << 8));

	uint16_t src = deck;
	uint16_t dst = wDeckToBuild_ADDR;

	EnableSRAM();
	CopyNBytesFromHLToDE(&src, &dst, DECK_STRUCT_SIZE);

	SafelySwitchToSRAM0();
	(void)DecrementDeckCardsInCollection((uint16_t)(wDeckToBuild_ADDR + DECK_NAME_SIZE));

	uint16_t built = HtimesL((uint16_t)(((uint16_t)DECK_STRUCT_SIZE << 8)
		| wDeckSlotForNewDeck));

	built = (uint16_t)(built + sBuiltDecks_ADDR);

	uint16_t copy_src = wDeckToBuild_ADDR;
	uint16_t copy_dst = built;

	CopyNBytesFromHLToDE(&copy_src, &copy_dst, DECK_STRUCT_SIZE);
	DisableSRAM();

	DrawDecksScreen(ALL_DECKS);
	wCurDeck = wDeckSlotForNewDeck;

	uint16_t menu_parameters = DECK_MACHINE_MENU_PARAMETERS_ADDR;

	InitializeMenuParameters(wDeckSlotForNewDeck, &menu_parameters);
	DrawCursor2();

	uint16_t deck_name = GetPointerToDeckName();

	EnableSRAM();
	(void)CopyDeckName(deck_name);
	DisableSRAM();
	SafelySwitchToTempSRAMBank();

	wTxRam2 = 0u;
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), 0u);

	WaitResult waited = DrawWideTextBox_WaitForInput(BuiltDeckText);

	/* `xor a` before the wait is what TryDeleteSavedDeck's identical tail
	 * models, so a is 0 and the closing `scf` only sets carry. */
	return (TryBuildDeckMachineDeckResult){0u, (uint8_t)((waited.f & 0x80u) | CARRY_FLAG)};
}
/* <<< factory TryBuildDeckMachineDeck */

/* >>> factory HandleAutoDeckMenu */
/* deck_machine.asm:1872-2010. The local labels are inlined: .please_select_deck
 * is the outer loop and .wait_input the inner one, while .InitAutoDeckMenu,
 * .CreateAutoDeckPointerList and the .please_select_deck prologue become static
 * helpers so that .read_the_instructions' `jp .wait_input` can re-enter the
 * inner loop without re-running that prologue.
 *
 * .exit is the routine's only `ret`: `xor a` / `ld [wTempBankSRAM], a` leaves
 * a = 0 with Z set and every other flag clear, so both `jp z, .exit` and the
 * fallthrough from .asm_bb09 return {0, $80}. */

/* .CreateAutoDeckPointerList: writes the little-endian pointers to the five
 * consecutive DECK_STRUCT_SIZE auto decks in sAutoDecks into wMachineDeckPtrs. */
static void hadm_create_auto_deck_pointer_list(void)
{
	ClearMemory_Bank2((uint8_t)(2u * NUM_DECK_MACHINE_SLOTS), wMachineDeckPtrs_ADDR);

	uint16_t de = wMachineDeckPtrs_ADDR;
	uint16_t hl = sAutoDecks_ADDR;

	for (uint8_t i = NUM_DECK_MACHINE_SLOTS; i != 0u; i--) {
		gb_write8(de++, (uint8_t)hl);
		gb_write8(de++, (uint8_t)(hl >> 8));
		hl = (uint16_t)(hl + DECK_STRUCT_SIZE);
	}
}

/* .InitAutoDeckMenu */
static void hadm_init_auto_deck_menu(void)
{
	Set_OBJ_8x8();
	wTileMapFill = 0u;
	ZeroObjectPositions();
	EmptyScreen();
	wVBlankOAMCopyToggle = TRUE;
	(void)LoadSymbolsFont();
	(void)LoadDuelCardSymbolTiles();
	SetDefaultConsolePalettes();
	(void)SetupText(0x3Cu, 0xFFu);

	uint16_t hl = 0u;

	DrawRegularTextBox(&hl, 0u, 20u, 13u, 0u, 0u);
	InitTextPrinting(1u, 0u);

	uint16_t title = (uint16_t)(gb_read8(wDeckMachineTitleText_ADDR)
		| ((uint16_t)gb_read8((uint16_t)(wDeckMachineTitleText_ADDR + 1u)) << 8));

	(void)ProcessTextFromID(title);
	SafelySwitchToSRAM1();
	ReadAutoDeckConfiguration();
	hadm_create_auto_deck_pointer_list();
	/* .CreateAutoDeckPointerList's closing `dec a` preserves carry and
	 * ClearMemory_Bank2 preserves af, so PrintVisibleDeckMachineEntries is
	 * entered on the path that prints all five entries -- the same call the
	 * landed ClearScreenAndDrawDeckMachineScreen models with a clear carry. */
	(void)PrintVisibleDeckMachineEntries(0u);
	SafelySwitchToSRAM0();
	EnableLCD();
}

/* .please_select_deck's prologue, everything above .wait_input. */
static void hadm_open_deck_menu(uint8_t cursor)
{
	uint16_t params = HANDLE_AUTO_DECK_MENU_MENU_PARAMETERS_ADDR;

	InitializeMenuParameters(cursor, &params);
	(void)DrawWideTextBox_PrintText(PleaseSelectDeckText);
	wCardListNumCursorPositions = NUM_DECK_MACHINE_SLOTS;
	gb_write8(wCardListUpdateFunction_ADDR, (uint8_t)UPDATE_DECK_MACHINE_SCROLL_ARROWS_ADDR);
	gb_write8((uint16_t)(wCardListUpdateFunction_ADDR + 1u),
		  (uint8_t)(UPDATE_DECK_MACHINE_SCROLL_ARROWS_ADDR >> 8));
}

HandleAutoDeckMenuResult HandleAutoDeckMenu(void)
{
	const uint8_t *title = rom_ptr(HANDLE_AUTO_DECK_MENU_BANK,
		(uint16_t)(HANDLE_AUTO_DECK_MENU_TITLE_TEXT_LIST_ADDR
			+ (uint8_t)(wCurAutoDeckMachine << 1)));

	gb_write8(wDeckMachineTitleText_ADDR, title[0]);
	gb_write8((uint16_t)(wDeckMachineTitleText_ADDR + 1u), title[1]);
	wCardListVisibleOffset = 0u;
	hadm_init_auto_deck_menu();
	wNumDeckMachineEntries = NUM_DECK_MACHINE_SLOTS;

	uint8_t cursor = 0u;
	uint8_t resume_wait_input = 0u;

	for (;;) { /* .please_select_deck */
		if (!resume_wait_input)
			hadm_open_deck_menu(cursor);
		resume_wait_input = 0u;

		uint8_t selection_made = 0u;

		for (;;) { /* .wait_input */
			DoFrame();
			if (HandleMenuInput().f & CARRY_FLAG) {
				selection_made = 1u;
				break;
			}
			/* The PAD_UP | PAD_DOWN test above .asm_ba4e falls through
			 * to the very next instruction either way, so it is a no-op. */
			if (!(hDPadHeld & PAD_START))
				continue;

			wTempCardListVisibleOffset = wCardListVisibleOffset;

			uint8_t offset = wCardListVisibleOffset;

			wTempDeckMachineCursorPos = wCurMenuItem;

			uint8_t index = (uint8_t)(wCurMenuItem + offset);

			wCurDeck = (uint8_t)((uint8_t)(index + 1u) | 0x80u);

			uint16_t entry = (uint16_t)(wMachineDeckPtrs_ADDR
				+ (uint8_t)(index << 1));

			SafelySwitchToSRAM1();

			uint16_t deck = (uint16_t)(gb_read8(entry)
				| ((uint16_t)gb_read8((uint16_t)(entry + 1u)) << 8));
			uint16_t name = (uint16_t)(deck + DECK_NAME_SIZE);
			uint8_t first = gb_read8(name);

			SafelySwitchToSRAM0();
			if (first == 0u)
				continue; /* invalid deck */

			PlaySFXConfirmOrCancel(MENU_CONFIRM);
			SafelySwitchToSRAM1();
			OpenDeckConfirmationMenu(name, deck);
			SafelySwitchToSRAM0();
			wCardListVisibleOffset = wTempCardListVisibleOffset;
			hadm_init_auto_deck_menu();
			cursor = wTempDeckMachineCursorPos;
			break;
		}
		if (!selection_made)
			continue;

		/* .deck_selection_made */
		DrawCursor2();
		wTempCardListVisibleOffset = wCardListVisibleOffset;
		wTempDeckMachineCursorPos = wCurMenuItem;

		uint8_t item = hCurMenuItem;

		if (item == MENU_CANCEL) {
			/* .exit */
			wTempBankSRAM = 0u;
			return (HandleAutoDeckMenuResult){0u, 0x80u};
		}

		wSelectedDeckMachineEntry = item;
		(void)ResetCheckMenuCursorPositionAndBlink();
		wce5e = 0u;
		(void)DrawWideTextBox();
		(void)PlaceTextItems(HANDLE_AUTO_DECK_MENU_MENU_DATA_ADDR);

		uint8_t choice;

		for (;;) { /* .wait_submenu_input */
			DoFrame();

			TempListResult input = HandleCheckMenuInput_YourOrOppPlayArea();

			if (input.f & CARRY_FLAG) {
				choice = input.a;
				break;
			}
		}
		if (choice == MENU_CANCEL) {
			cursor = wTempDeckMachineCursorPos;
			continue;
		}

		/* .submenu_option_selected */
		uint8_t option = (uint8_t)((uint8_t)(wCheckMenuCursorYPosition << 1)
			+ wCheckMenuCursorXPosition);

		if (option == 0u) { /* Build a Deck */
			SafelySwitchToSRAM1();

			TryBuildDeckMachineDeckResult built = TryBuildDeckMachineDeck();

			/* SafelySwitchToSRAM0 and the `ld a, [wTempDeckMachineCursorPos]`
			 * between them both preserve the carry `jp nc` tests. */
			SafelySwitchToSRAM0();
			cursor = wTempDeckMachineCursorPos;
			if (!(built.f & CARRY_FLAG))
				continue;

			wCardListVisibleOffset = wTempCardListVisibleOffset;
			hadm_init_auto_deck_menu();
			cursor = wTempDeckMachineCursorPos;
			continue;
		}
		if (option == 1u) { /* .asm_bb09 falls into .exit */
			wTempBankSRAM = 0u;
			return (HandleAutoDeckMenuResult){0u, 0x80u};
		}

		/* .read_the_instructions */
		wTempCardListVisibleOffset = wCardListVisibleOffset;

		uint8_t list_offset = wCardListVisibleOffset;

		wTempDeckMachineCursorPos = wCurMenuItem;

		uint8_t list_index = (uint8_t)(wCurMenuItem + list_offset);

		wCurDeck = list_index;

		uint16_t list_entry = (uint16_t)(wMachineDeckPtrs_ADDR
			+ (uint8_t)(list_index << 1));
		uint16_t description = (uint16_t)(wAutoDeckMachineTextDescriptions_ADDR
			+ (uint8_t)(list_index << 1));

		gb_write8(wCardConfirmationText_ADDR, gb_read8(description));
		gb_write8((uint16_t)(wCardConfirmationText_ADDR + 1u),
			  gb_read8((uint16_t)(description + 1u)));

		SafelySwitchToSRAM1();

		uint16_t list_deck = (uint16_t)(gb_read8(list_entry)
			| ((uint16_t)gb_read8((uint16_t)(list_entry + 1u)) << 8));
		uint16_t list_name = (uint16_t)(list_deck + DECK_NAME_SIZE);
		uint8_t list_first = gb_read8(list_name);

		SafelySwitchToSRAM0();
		if (list_first == 0u) {
			/* `jp z, .wait_input`: back into the inner loop without
			 * re-running the .please_select_deck prologue. */
			resume_wait_input = 1u;
			continue;
		}

		PlaySFXConfirmOrCancel(MENU_CONFIRM);
		SafelySwitchToSRAM1();
		(void)HandleDeckMissingCardsList(list_deck, list_name);
		SafelySwitchToSRAM0();
		wCardListVisibleOffset = wTempCardListVisibleOffset;
		hadm_init_auto_deck_menu();
		cursor = wTempDeckMachineCursorPos;
	}
}
/* <<< factory HandleAutoDeckMenu */

/* >>> factory InitDeckMachineDrawingParams */
InitDeckMachineDrawingParamsResult InitDeckMachineDrawingParams(uint8_t d, uint8_t e)
{
	wCardListNumCursorPositions = NUM_DECK_MACHINE_SLOTS;
	wDeckMachineText = e;
	gb_write8((uint16_t)(wDeckMachineText_ADDR + 1u), d);
	wCardListUpdateFunction = (uint8_t)DRAW_DECK_MACHINE_SCREEN_ADDR;
	gb_write8((uint16_t)(wCardListUpdateFunction_ADDR + 1u), (uint8_t)(DRAW_DECK_MACHINE_SCREEN_ADDR >> 8));
	wced2 = 0u;
	return (InitDeckMachineDrawingParamsResult){0u, 0x80u, (uint8_t)(DRAW_DECK_MACHINE_SCREEN_ADDR >> 8), e, (uint16_t)(wCardListUpdateFunction_ADDR + 1u)};
}
/* <<< factory InitDeckMachineDrawingParams */
