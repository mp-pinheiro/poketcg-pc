/* === part includes */
/* >>> part MENU_CONFIRM */
#define MENU_CONFIRM 0x01u
/* <<< part MENU_CONFIRM */
/* --- part includes_tail */
/* >>> part includes_tail */
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes_tail */
/* --- part includes_DATA_B04A_ADDR */
/* --- part DATA_B04A_ADDR */
/* --- part SHOW_RECEIVED_CARDS_LIST_ADDR */
/* >>> part includes_tail_2 */
#include "home/common.h"
#include "home/save.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"

#include "home/common.h"
#include "home/save.h"

#include "home/deck_configuration.h"
#include "home/switch_sram.h"
#include "home/menus.h"
#include "home/credits_sequence_commands.h"
#include "home/lcd.h"
#include "home/process_text.h"
#include "home/tiles.h"
#include "home/duel_core.h"
#include "home/objects.h"
#include "home/print_text.h"
#include "home/save.h"
#include "home/common.h"
#include "generated/wram.h"

#include "generated/wram.h"

#include "generated/wram.h"
#include "home/deck_machine.h"
/* <<< part includes_tail_2 */
/* >>> factory CheckIfHasEnoughCardsToBuildDeck */
/* deck_machine.asm:1290-1323. */
DeckBuildCheckResult CheckIfHasEnoughCardsToBuildDeck(uint16_t *hl)
{
	uint16_t source = *hl;
	uint16_t collection = wTempCardCollection_ADDR;
	for (uint8_t count = 0u; count < DECK_SIZE; count++) {
		uint8_t low = gb_read8(source++);
		uint8_t high = gb_read8(source);
		uint16_t slot = (uint16_t)(collection + low +
			((uint16_t)high << 8));
		uint8_t owned = gb_read8(slot);
		if (owned == 0u || owned == CARD_NOT_OWNED) {
			*hl = source;
			return (DeckBuildCheckResult){
				owned, 0x90u};
		}
		gb_write8(slot, (uint8_t)(owned - 1u));
		source = (uint16_t)(source + 1u);
	}
	*hl = source;
	return (DeckBuildCheckResult){DECK_SIZE, 0x00u};
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
		h = (uint16_t)(h + DECK_COMPRESSED_STRUCT_SIZE);
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
		uint16_t hl = (uint16_t)(sSavedDecks_ADDR + i * DECK_COMPRESSED_STRUCT_SIZE);
		if (gb_read8(hl) != 0u)
			count++;
	}
	wNumSavedDecks = count;
	DisableSRAM();
}
/* <<< factory GetSavedDeckCount */
/* >>> factory FindFirstEmptyDeckSlot */
FindFirstEmptyDeckSlotResult FindFirstEmptyDeckSlot(void)
{
	const uint16_t slots[] = {
		sDeck1Cards_ADDR, sDeck2Cards_ADDR, sDeck3Cards_ADDR, sDeck4Cards_ADDR
	};
	uint8_t last = 0u;
	uint16_t hl = slots[0];
	for (uint8_t i = 0u; i < 4u; i++) {
		hl = slots[i];
		uint8_t low = gb_read8(hl++);
		uint8_t high = gb_read8(hl);
		last = (uint8_t)(low | high);
		if (last == 0u)
			return (FindFirstEmptyDeckSlotResult){i, 0x80u, hl};
	}
	return (FindFirstEmptyDeckSlotResult){last, 0x10u, hl};
}
/* <<< factory FindFirstEmptyDeckSlot */
/* --- factory EmptyScreenAndDrawTextBox */
/* --- factory PrintCardToSendText */
/* --- factory PrintReceivedTheseCardsText */
/* --- factory Func_b568 */
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
	EnableSRAM();
	DecompressSRAMDeck(ptr, wCurDeckCards_ADDR);
	DisableSRAM();
	uint16_t cards = wCurDeckCards_ADDR;
	DeckBuildCheckResult r = CheckIfHasEnoughCardsToBuildDeck(&cards);
	return r;
}
/* <<< factory CheckIfCanBuildSavedDeck */
/* >>> factory PrintDeckMachineEntry */
/* deck_machine.asm:1107-1230. The build symbols are fullwidth "○" $03,$5F,
 * "※" $03,$60 and "×" $00,$6C; .text is six TX_SYMBOL spaces. */
#define DECK_MACHINE_CAN_BUILD_HI 0x03u
#define DECK_MACHINE_CAN_BUILD_LO 0x5Fu
#define DECK_MACHINE_DISMANTLE_HI 0x03u
#define DECK_MACHINE_DISMANTLE_LO 0x60u
#define DECK_MACHINE_CANNOT_BUILD_HI 0x00u
#define DECK_MACHINE_CANNOT_BUILD_LO 0x6Cu

static uint8_t deck_machine_num_cards_missing(uint8_t b)
{
	SafelySwitchToSRAM0();
	CreateCardCollectionListWithDeckCards(0u);
	SafelySwitchToTempSRAMBank();
	uint16_t table = (uint16_t)(wMachineDeckPtrs_ADDR + (uint16_t)((uint8_t)(b << 1)));
	uint16_t compressed = (uint16_t)(gb_read8(table) |
		(uint16_t)gb_read8((uint16_t)(table + 1u)) << 8);
	compressed = (uint16_t)(compressed + DECK_NAME_SIZE);
	EnableSRAM();
	DecompressSRAMDeck(compressed, wCurDeckCards_ADDR);
	uint16_t cards = wCurDeckCards_ADDR;
	uint8_t missing = 0u;
	for (uint8_t index = 0u; index < DECK_SIZE; index++) {
		CardId card = card_id_read(&cards);
		uint16_t slot = (uint16_t)(wTempCardCollection_ADDR + card);
		uint8_t count = (uint8_t)(gb_read8(slot) & CARD_COUNT_MASK);
		if (count == 0u)
			missing++;
		else
			gb_write8(slot, (uint8_t)(count - 1u));
	}
	DisableSRAM();
	return missing;
}

PrintDeckMachineEntryResult PrintDeckMachineEntry(uint8_t a, uint8_t d, uint8_t e)
{
	uint8_t deck_index = a;
	uint16_t hl = wDefaultText_ADDR;
	ConvertToNumericalDigitsResult cd = ConvertToNumericalDigits((uint8_t)(a + 1u), hl);
	hl = cd.hl;
	gb_write8(hl, 0x77u);
	gb_write8((uint16_t)(hl + 1u), TX_END);
	InitTextPrinting(d, e);
	hl = wDefaultText_ADDR;
	ProcessText(&hl);

	uint16_t table_addr = (uint16_t)(wMachineDeckPtrs_ADDR + (uint16_t)((uint8_t)(deck_index << 1)));
	uint16_t ptr = (uint16_t)(gb_read8(table_addr) | (uint16_t)gb_read8((uint16_t)(table_addr + 1u)) << 8);
	uint8_t x = (uint8_t)(d + 3u);
	if ((AppendDeckName(ptr, x, e) & 0x10u) != 0u) {
		InitTextPrinting(x, e);
		(void)ProcessTextFromID(EmptyDeckNameText);
		InitTextPrinting(13u, (uint8_t)(e + 1u));
		uint16_t text_hl = PRINT_DECK_MACHINE_ENTRY_TEXT_ADDR;
		ProcessText(&text_hl);
		return (PrintDeckMachineEntryResult){0u, 0x90u};
	}

	InitTextPrinting(18u, e);
	uint8_t symbol_hi;
	uint8_t symbol_lo;
	if ((CheckIfCanBuildSavedDeck(0u, deck_index).f & 0x10u) == 0u) {
		symbol_hi = DECK_MACHINE_CAN_BUILD_HI;
		symbol_lo = DECK_MACHINE_CAN_BUILD_LO;
	} else if ((CheckIfCanBuildSavedDeck(ALL_DECKS, deck_index).f & 0x10u) == 0u) {
		symbol_hi = DECK_MACHINE_DISMANTLE_HI;
		symbol_lo = DECK_MACHINE_DISMANTLE_LO;
	} else {
		Func_22ca(DECK_MACHINE_CANNOT_BUILD_HI, DECK_MACHINE_CANNOT_BUILD_LO);
		InitTextPrinting(17u, (uint8_t)(e + 1u));
		CalculateOnesAndTensDigits(deck_machine_num_cards_missing(deck_index));
		uint8_t ones = gb_read8(wDecimalDigitsSymbols_ADDR);
		uint8_t tens = gb_read8((uint16_t)(wDecimalDigitsSymbols_ADDR + 1u));
		hl = wDefaultText_ADDR;
		gb_write8(hl++, TX_SYMBOL);
		gb_write8(hl++, tens);
		gb_write8(hl++, TX_SYMBOL);
		gb_write8(hl++, ones);
		gb_write8(hl, TX_END);
		hl = wDefaultText_ADDR;
		ProcessTextResult printed = ProcessText(&hl);
		return (PrintDeckMachineEntryResult){printed.a, (uint8_t)(printed.f & 0x80u)};
	}
	Func_22ca(symbol_hi, symbol_lo);
	InitTextPrinting(13u, (uint8_t)(e + 1u));
	uint16_t text_hl = PRINT_DECK_MACHINE_ENTRY_TEXT_ADDR;
	ProcessTextResult printed = ProcessText(&text_hl);
	return (PrintDeckMachineEntryResult){printed.a, (uint8_t)(printed.f & 0x80u)};
}
/* <<< factory PrintDeckMachineEntry */
/* --- factory ShowReceivedCardsList */
/* --- factory Func_b088 */
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
	ClearMemory_Bank2(DECK_COMPRESSED_STRUCT_SIZE, deck);
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
 * .CardListUpdateFunction is armed into wCardListUpdateFunction each .loop
 * iteration and fired by the card-list input handlers after a scroll
 * (deck_configuration.asm:1823-1824, 2483-2484); the port routes that dispatch
 * through DispatchCardListUpdateFunction in deck_configuration.c, which
 * resolves 02:6e9a to HandleDeckMissingCardsList_CardListUpdateFunction
 * below. The two bytes written are the real bank-2 address, so the WRAM
 * still matches the reference. */
/* .PrintDeckIndexAndName, deck_machine.asm:131-159: prints text in the form
 * "X.<DECK NAME> deck"; returns early when no deck name is selected. */
static void PrintDeckIndexAndName(void)
{
	if (wCurDeckName == 0u)
		return;
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

HandleDeckMissingCardsListResult HandleDeckMissingCardsList(uint16_t hl, uint16_t de)
{
	(void)de;
	(void)CopyListFromHLToDEInSRAM(hl, wCurDeckName_ADDR);

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
		PrintDeckIndexAndName();
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
		uint16_t menu_parameters = DeckMachineMenuParameters_ADDR;
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
			ClearMemory_Bank2(DECK_COMPRESSED_STRUCT_SIZE, deck_name);
			DisableSRAM();

			DrawDecksScreen(ALL_DECKS);
			cursor = wCurDeck;
			menu_parameters = DeckMachineMenuParameters_ADDR;
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
/* >>> factory SaveDeckInDeckSaveMachine */
SaveDeckInDeckSaveMachineResult SaveDeckInDeckSaveMachine(void)
{
	uint8_t a = 0u;
	DrawDecksScreen(ALL_DECKS);
	for (;;) {
		uint16_t menu_parameters = DeckMachineMenuParameters_ADDR;
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
			CopyNBytesFromHLToDE(&source, &destination, DECK_COMPRESSED_STRUCT_SIZE);
			DisableSRAM();
			ClearScreenAndDrawDeckMachineScreen();
			DrawListScrollArrows();
			PrintNumSavedDecks();
			uint8_t list_cursor = wTempDeckMachineCursorPos;
			uint16_t selection_parameters = DeckMachineSelectionParams_ADDR;
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
	uint16_t hl = HtimesL((uint16_t)(((uint16_t)DECK_COMPRESSED_STRUCT_SIZE << 8) | deck));
	hl = (uint16_t)(hl + sBuiltDecks_ADDR);
	(void)AddDeckToCollection((uint16_t)(hl + DECK_NAME_SIZE));
	ClearMemory_Bank2(DECK_COMPRESSED_STRUCT_SIZE, hl);
}

/* .CheckIfCardIsMissing: `missing` is the asm's carry, `a` the difference it
 * reports when the collection is short. */
static TbdmdMissing tbdmd_check_if_card_is_missing(CardId card, uint16_t hl)
{
	uint8_t deck_count = 0u;
	for (;;) {
		CardId id = card_id_read(&hl);
		if (id == 0u)
			break;
		if (id == card)
			deck_count = (uint8_t)(deck_count + 1u);
	}

	uint8_t owned = (uint8_t)(gb_read8((uint16_t)(wTempCardCollection_ADDR + card))
		& CARD_COUNT_MASK);
	if (owned < deck_count)
		return (TbdmdMissing){(uint8_t)(deck_count - owned), 1u};
	return (TbdmdMissing){owned, 0u};
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
			uint16_t source = (uint16_t)(saved + DECK_NAME_SIZE);
			EnableSRAM();
			DecompressSRAMDeck(source, wCurDeckCards_ADDR);
			DisableSRAM();
			gb_write8((uint16_t)(wCurDeckCards_ADDR + DECK_SIZE * 2u), 0u);
			gb_write8((uint16_t)(wCurDeckCards_ADDR + DECK_SIZE * 2u + 1u), 0u);

			(void)SortCurDeckCardsByID();
			(void)CreateCurDeckUniqueCardList();

			SafelySwitchToSRAM0();
			CreateCardCollectionListWithDeckCards(ALL_DECKS);
			SafelySwitchToTempSRAMBank();

			uint16_t list = wUniqueDeckCardList_ADDR;
			uint16_t out = wFilteredCardList_ADDR;
			for (;;) {
				CardId card = card_id_read(&list);
				if (card == 0u)
					break;
				TbdmdMissing missing =
					tbdmd_check_if_card_is_missing(card, wCurDeckCards_ADDR);
				if (!missing.missing)
					continue;
				for (uint8_t count = missing.a; count != 0u; count--)
					card_id_write(&out, card);
			}
			card_id_write(&out, 0u);

			gb_write8(wCardConfirmationText_ADDR,
				(uint8_t)TheseCardsAreNeededToBuildThisDeckText);
			gb_write8((uint16_t)(wCardConfirmationText_ADDR + 1u),
				(uint8_t)(TheseCardsAreNeededToBuildThisDeckText >> 8));

			uint16_t missing_list = wFilteredCardList_ADDR;
			uint16_t deck_cards = wCurDeckCards_ADDR;
			for (uint8_t count = 0u; count < DECK_SIZE; count++) {
				card_id_write(&deck_cards, card_id_read(&missing_list));
			}
			card_id_write(&deck_cards, 0u);

			uint16_t name = GetSelectedSavedDeckPtr();
			HandleDeckMissingCardsListResult shown =
				HandleDeckMissingCardsList(name, deck_cards);
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

	uint16_t src_name = deck;
	uint16_t dst_name = wDeckToBuild_ADDR;

	EnableSRAM();
	CopyNBytesFromHLToDE(&src_name, &dst_name, DECK_NAME_SIZE);
	uint16_t compressed = (uint16_t)(deck + DECK_NAME_SIZE);
	uint16_t uncompressed = (uint16_t)(wDeckToBuild_ADDR + DECK_NAME_SIZE);
	DecompressSRAMDeck(compressed, uncompressed);

	SafelySwitchToSRAM0();
	(void)DecrementDeckCardsInCollection(uncompressed);

	uint16_t built = HtimesL((uint16_t)(((uint16_t)DECK_COMPRESSED_STRUCT_SIZE << 8)
		| wDeckSlotForNewDeck));
	built = (uint16_t)(built + sBuiltDecks_ADDR);
	uint16_t copy_src = wDeckToBuild_ADDR;
	uint16_t copy_dst = built;
	CopyNBytesFromHLToDE(&copy_src, &copy_dst, DECK_NAME_SIZE);
	uint16_t compressed_dst = (uint16_t)(built + DECK_NAME_SIZE);
	CompressDeckToSRAM(uncompressed, compressed_dst);
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
		hl = (uint16_t)(hl + DECK_COMPRESSED_STRUCT_SIZE);
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
/* --- factory PrinterMenu_DeckConfiguration */
/* --- factory GiftCenter_ReceiveCard */
/* --- factory GiftCenter_ReceiveDeck */
/* --- factory GiftCenter_SendCard */
/* --- factory GiftCenter_SendDeck */
/* --- factory HandleGiftCenter */
/* === factory HandleDeckMachineSelection */
/* === factory SafelySwitchToTempSRAMBank */
/* >>> factory CheckIfSelectedDeckMachineEntryIsEmpty */
uint8_t CheckIfSelectedDeckMachineEntryIsEmpty(void)
{
	uint16_t entry = (uint16_t)(wMachineDeckPtrs_ADDR
		+ (uint16_t)wSelectedDeckMachineEntry * 2u);
	uint16_t deck = (uint16_t)(gb_read8(entry)
		| (uint16_t)(gb_read8((uint16_t)(entry + 1u)) << 8));
	uint16_t cards = (uint16_t)(deck + DECK_NAME_SIZE);

	EnableSRAM();
	uint8_t value = (uint8_t)(gb_read8(cards) | gb_read8((uint16_t)(cards + 1u)));
	DisableSRAM();

	return value ? 0u : 0x90u;
}
/* <<< factory CheckIfSelectedDeckMachineEntryIsEmpty */
