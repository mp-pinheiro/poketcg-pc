#include "home/deck_selection.h"
#include "home/duel.h"
#include "home/duel_core.h"
#include "home/empty_screen.h"
#include "home/objects.h"
#include "home/switch_rom.h"

#include "generated/text_ids.h"
#include "generated/constants.h"
#define MENU_CONFIRM 0x01u
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/random.h"

#define DECK_CARD_STRIDE 0x54u


#include "generated/wram.h"

#include "mem.h"

#include "generated/wram.h"
#include "mem.h"

#include "home/switch_sram.h"
#include "home/load_deck.h"
#include "mem.h"

#include "home/deck_selection.h"
#define SYM_0 0x20u

#define HandCardsGfx HandCardsGfx_ADDR
#define v0Tiles2_dest 0x9380u

#define TRUE 0x01u


#include "generated/wram.h"

#include "generated/wram.h"
#include "home/deck_configuration.h"


#include "generated/hram.h"
#include "generated/wram.h"
#include "home/deck_check.h"

#define PAD_START 0x08u
#define MENU_CANCEL 0xFFu

#include "generated/sram.h"
#include "generated/wram.h"
#include "home/input_name.h"
#include "home/write_number.h"
#include "mem.h"
#define INPUT_CUR_DECK_DECK1_DATA (PrintCardSetListEntries_ADDR + 0x69u)
#define INPUT_CUR_DECK_DECK2_DATA (PrintCardSetListEntries_ADDR + 0x72u)
#define INPUT_CUR_DECK_DECK3_DATA (PrintCardSetListEntries_ADDR + 0x7Bu)
#define INPUT_CUR_DECK_DECK4_DATA (PrintCardSetListEntries_ADDR + 0x84u)

#include "home/frames.h"
#include "home/menus.h"
#include "home/tiles.h"
#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "mem.h"
#define DECK_BUILDING_PARAMS_ADDR DeckBuildingParams_ADDR
#define DECK_SELECTION_MENU_PARAMS_ADDR (DeckSelectionMenu__DeckSelectionMenuParameters_ADDR)
#define DECK_SELECTION_DATA_ADDR DeckSelectionData_ADDR
/* <<< factory statics */

/* >>> factory GetPointerToDeckCards */
/* deck_selection.asm:528-545 */
uint16_t GetPointerToDeckCards(void)
{
	uint16_t hl = (uint16_t)(((uint16_t)wCurDeck << 8) | DECK_CARD_STRIDE);
	uint16_t offset = HtimesL(hl);
	return (uint16_t)(sDeck1Cards_ADDR + offset);
}
/* <<< factory GetPointerToDeckCards */

/* >>> factory ResetCheckMenuCursorPositionAndBlink */
/* deck_selection.asm:541-551 */
ResetCheckMenuCursorPositionAndBlinkResult ResetCheckMenuCursorPositionAndBlink(void)
{
	wCheckMenuCursorXPosition = 0u;
	wCheckMenuCursorYPosition = 0u;
	wCheckMenuCursorBlinkCounter = 0u;
	return (ResetCheckMenuCursorPositionAndBlinkResult){0u, 0x80u};
}
/* <<< factory ResetCheckMenuCursorPositionAndBlink */

/* >>> factory GetPointerToDeckName */
uint16_t GetPointerToDeckName(void)
{
	uint8_t deck = wCurDeck;
	uint16_t offset = HtimesL((uint16_t)(((uint16_t)deck << 8) | DECK_STRUCT_SIZE));
	return (uint16_t)(sDeck1Name_ADDR + offset);
}
/* <<< factory GetPointerToDeckName */

/* >>> factory InitDeckBuildingParams */
InitDeckBuildingParamsResult InitDeckBuildingParams(uint16_t *hl, uint8_t f)
{
	uint8_t a = 0u;
	uint8_t b = 7u;
	for (uint8_t i = 0; i < 7u; i++) {
		a = gb_read8((*hl)++);
		wMaxNumCardsAllowed_PTR[i] = a;
		b--;
	}
	return (InitDeckBuildingParamsResult){a, (uint8_t)((f & 0x10u) | 0xC0u), b, 0xCFD8u, *hl};
}
/* <<< factory InitDeckBuildingParams */

/* >>> factory CheckIfCurDeckIsValid */
CheckIfCurDeckIsValidResult CheckIfCurDeckIsValid(void)
{
	uint8_t deck = gb_read8(0xCEB1u);
	uint16_t hl = (uint16_t)(0xCEB2u + deck);
	uint8_t b = 0u;
	uint8_t c = deck;
	uint8_t value = gb_read8(hl);
	uint8_t f = value ? 0x00u : 0x90u;
	return (CheckIfCurDeckIsValidResult){value, f, b, c, hl};
}
/* <<< factory CheckIfCurDeckIsValid */

/* >>> factory CancelDeckSelectionSubMenu */
void CancelDeckSelectionSubMenu(void)
{
	return;
}
/* <<< factory CancelDeckSelectionSubMenu */

/* >>> factory LoadHandCardsIcon */
LoadHandCardsIconResult LoadHandCardsIcon(void)
{
	gb_write8(0x2000u, 0x02u);
	uint16_t hl = HandCardsGfx;
	uint16_t de = v0Tiles2_dest;
	CopyListFromHLToDE(&hl, &de);
	return (LoadHandCardsIconResult){hl, (uint8_t)(de >> 8), (uint8_t)de};
}
/* <<< factory LoadHandCardsIcon */

/* >>> factory InitPromotionalCardAndDeckCounterSaveData */
LoadHandCardsIconResult InitPromotionalCardAndDeckCounterSaveData(void)
{
	EnableSRAM();
	gb_write8(sHasPromotionalCards_ADDR, 0u);
	gb_write8((uint16_t)(sHasPromotionalCards_ADDR + 1u), 1u);
	gb_write8((uint16_t)(sHasPromotionalCards_ADDR + 2u), 1u);
	gb_write8((uint16_t)(sHasPromotionalCards_ADDR + 3u), 1u);
	gb_write8(sUnnamedDeckCounter_ADDR, 1u);
	DisableSRAM();
	return LoadHandCardsIcon();
}
/* <<< factory InitPromotionalCardAndDeckCounterSaveData */

/* >>> factory PrepareMenuGraphics */
void PrepareMenuGraphics(void)
{
	wTileMapFill = 0u;
	ZeroObjectPositions();
	EmptyScreen();
	wVBlankOAMCopyToggle = TRUE;
	LoadCursorTile();
	LoadSymbolsFont();
	LoadDuelCardSymbolTiles();
	LoadHandCardsIcon();
	SetDefaultConsolePalettes();
	SetupText(0x3cu, 0xbfu);
}
/* <<< factory PrepareMenuGraphics */

/* >>> factory EmptyScreenAndLoadFontDuelAndHandCardsIcons */
void EmptyScreenAndLoadFontDuelAndHandCardsIcons(void)
{
	wTileMapFill = 0u;
	EmptyScreen();
	ZeroObjectPositions();
	wVBlankOAMCopyToggle = TRUE;
	LoadSymbolsFont();
	LoadDuelCardSymbolTiles();
	LoadHandCardsIcon();
	SetDefaultConsolePalettes();
	SetupText(0x3cu, 0xbfu);
}
/* <<< factory EmptyScreenAndLoadFontDuelAndHandCardsIcons */

/* >>> factory PrintThereIsNoDeckHereText */
uint8_t PrintThereIsNoDeckHereText(void)
{
	DrawWideTextBox_WaitForInput(ThereIsNoDeckHereText);
	return wCurDeck;
}
/* <<< factory PrintThereIsNoDeckHereText */

/* >>> factory WriteCardListsTerminatorBytes */
WriteCardListsTerminatorBytesResult WriteCardListsTerminatorBytes(void)
{
	uint16_t filtered_terminator = (uint16_t)(wFilteredCardList_ADDR + DECK_SIZE);
	gb_write8(filtered_terminator, 0u);
	uint16_t deck_terminator = (uint16_t)(wCurDeckCards_ADDR + DECK_CONFIG_BUFFER_SIZE);
	gb_write8(deck_terminator, 0u);
	return (WriteCardListsTerminatorBytesResult){0u, 0x80u, 0u, 0x50u, 0xCF67u};
}
/* <<< factory WriteCardListsTerminatorBytes */

/* >>> factory OpenDeckConfirmationMenu */
void OpenDeckConfirmationMenu(uint16_t de, uint16_t hl)
{
	/* copy deck name */
	CopyListFromHLToDEInSRAM(hl, wCurDeckName_ADDR);

	/* copy deck cards */
	EnableSRAM();
	DecompressSRAMDeck(de, wCurDeckCards_ADDR);
	DisableSRAM();
	gb_write8((uint16_t)(wCurDeckCards_ADDR + DECK_SIZE * 2u), 0u);
	gb_write8((uint16_t)(wCurDeckCards_ADDR + DECK_SIZE * 2u + 1u), 0u);

	ClearMemory_Bank2(NUM_FILTERS, wCardFilterCounts_ADDR);
	wTotalCardCount = DECK_SIZE;
	wCardFilterCounts = DECK_SIZE;
	HandleDeckConfirmationMenu();
}
/* <<< factory OpenDeckConfirmationMenu */

/* >>> factory HandleStartButtonInDeckSelectionMenu */
HandleStartButtonInDeckSelectionMenuResult HandleStartButtonInDeckSelectionMenu(void)
{
	uint8_t a = (uint8_t)(hDPadHeld & PAD_START);
	if (a == 0u)
		return (HandleStartButtonInDeckSelectionMenuResult){a, 0xA0u};

	wCurDeck = wCurMenuItem;
	CheckIfCurDeckIsValidResult validity = CheckIfCurDeckIsValid();
	if ((validity.f & 0x10u) != 0u) {
		PlaySFXConfirmOrCancel(MENU_CANCEL);
		uint8_t deck = PrintThereIsNoDeckHereText();
		return (HandleStartButtonInDeckSelectionMenuResult){deck, 0x90u};
	}

	PlaySFXConfirmOrCancel(MENU_CONFIRM);
	uint16_t cards = GetPointerToDeckCards();
	uint16_t name = GetPointerToDeckName();
	OpenDeckConfirmationMenu(cards, name);
	DrawDecksScreen(ALL_DECKS);
	return (HandleStartButtonInDeckSelectionMenuResult){wCurDeck, 0x10u};
}
/* <<< factory HandleStartButtonInDeckSelectionMenu */

/* >>> factory InputCurDeckName */
void InputCurDeckName(void)
{
	uint8_t deck = wCurDeck;
	uint16_t question = INPUT_CUR_DECK_DECK4_DATA;
	if (deck == 0u)
		question = INPUT_CUR_DECK_DECK1_DATA;
	else if (deck == 1u)
		question = INPUT_CUR_DECK_DECK2_DATA;
	else if (deck == 2u)
		question = INPUT_CUR_DECK_DECK3_DATA;

	/* deck_selection.asm:331 `farcall InputDeckName`: bank 6 for the call and
	 * the caller's bank back after it. Writing g_rom_bank alone desynced
	 * hBankROM, so a callee's own save/restore put the caller's bank back
	 * mid-call and the naming screen read its question text from bank 2. */
	uint8_t saved_bank = hBankROM;
	BankswitchROM(6u);
	(void)InputDeckName(MAX_DECK_NAME_LENGTH, 4u, 1u,
		(uint8_t)(wCurDeckName_ADDR >> 8), (uint8_t)wCurDeckName_ADDR, question);
	BankswitchROM(saved_bank);
	if (gb_read8(wCurDeckName_ADDR) != 0u)
		return;

	EnableSRAM();
	uint8_t counter_low = sUnnamedDeckCounter;
	uint8_t counter_high = sUnnamedDeckCounter_PTR[1];
	DisableSRAM();
	uint16_t counter = (uint16_t)(((uint16_t)counter_high << 8) | counter_low);
	uint16_t text = wDefaultText_ADDR;
	TwoByteNumberToText(counter, &text);

	uint16_t name = wCurDeckName_ADDR;
	gb_write8(name++, 0x06u);
	gb_write8(name++, (uint8_t)'D');
	gb_write8(name++, (uint8_t)'e');
	gb_write8(name++, (uint8_t)'c');
	gb_write8(name++, (uint8_t)'k');
	gb_write8(name++, (uint8_t)' ');
	uint16_t digits = (uint16_t)(wDefaultText_ADDR + 2u);
	gb_write8(name++, gb_read8(digits++));
	gb_write8(name++, gb_read8(digits++));
	gb_write8(name++, gb_read8(digits));
	gb_write8(name, 0u);

	EnableSRAM();
	counter = (uint16_t)(((uint16_t)sUnnamedDeckCounter_PTR[1] << 8) | sUnnamedDeckCounter);
	if (counter == MAX_UNNAMED_DECK_NUM)
		counter = 0u;
	counter = (uint16_t)(counter + 1u);
	sUnnamedDeckCounter_PTR[1] = (uint8_t)(counter >> 8);
	sUnnamedDeckCounter = (uint8_t)counter;
	DisableSRAM();
}
/* <<< factory InputCurDeckName */

/* >>> factory DeckSelectionMenu */
void DeckSelectionMenu(void)
{
	uint16_t params = DECK_BUILDING_PARAMS_ADDR;
	(void)InitDeckBuildingParams(&params, 0u);
	DrawDecksScreen(ALL_DECKS);
	DeckSelectionMenu_InitMenuParams(0u);
}

void DeckSelectionMenu_InitMenuParams(uint8_t a)
{
	for (;;) {
		uint16_t menu_params = DECK_SELECTION_MENU_PARAMS_ADDR;
		InitializeMenuParameters(a, &menu_params);
		(void)DrawWideTextBox_PrintText(PleaseSelectDeckText);
		for (;;) {
			DoFrame();
			HandleStartButtonInDeckSelectionMenuResult start = HandleStartButtonInDeckSelectionMenu();
			if ((start.f & 0x10u) != 0u) {
				a = start.a;
				break;
			}
			HandleMenuInputResult input = HandleMenuInput();
			if ((input.f & 0x10u) == 0u)
				continue;
			if (hCurMenuItem == MENU_CANCEL)
				return;
			uint8_t selected_deck = hCurMenuItem;
			wCurDeck = selected_deck;
			DeckSelectionSubMenu();
			return;
		}
	}
}
/* <<< factory DeckSelectionMenu */

/* >>> factory DeckSelectionSubMenu */
void DeckSelectionSubMenu(void)
{
	(void)DrawWideTextBox();
	(void)PlaceTextItems(DECK_SELECTION_DATA_ADDR);
	(void)ResetCheckMenuCursorPositionAndBlink();
	for (;;) {
		DoFrame();
		HandleCheckMenuInputResult input = HandleCheckMenuInput();
		if ((input.f & 0x10u) == 0u)
			continue;
		if (input.a == MENU_CANCEL) {
			(void)EraseCheckMenuCursor();
			DeckSelectionMenu_InitMenuParams(wCurDeck);
			return;
		}
		if (wCheckMenuCursorXPosition != 0u) {
			DeckSelectionSubMenu_SelectOrCancel();
			return;
		}
		if (wCheckMenuCursorYPosition != 0u) {
			CheckIfCurDeckIsValidResult validity = CheckIfCurDeckIsValid();
			if ((validity.f & 0x10u) != 0u) {
				DeckSelectionMenu_InitMenuParams(PrintThereIsNoDeckHereText());
				return;
			}
			goto get_input_deck_name;
		}

		uint16_t deck_cards = GetPointerToDeckCards();
		EnableSRAM();
		DecompressSRAMDeck(deck_cards, wCurDeckCards_ADDR);
		DisableSRAM();
		gb_write8((uint16_t)(wCurDeckCards_ADDR + DECK_SIZE * 2u), 0u);
		gb_write8((uint16_t)(wCurDeckCards_ADDR + DECK_SIZE * 2u + 1u), 0u);
		ClearMemory_Bank2(20u, wCurDeckName_ADDR);
		uint16_t deck_name = GetPointerToDeckName();
		(void)CopyListFromHLToDEInSRAM(deck_name, wCurDeckName_ADDR);

		DeckBuildScreenResult built = HandleDeckBuildScreen();
		if ((built.f & 0x10u) == 0u) {
			DrawDecksScreen(ALL_DECKS);
			DeckSelectionMenu_InitMenuParams(wCurDeck);
			return;
		}
		EnableSRAM();
		(void)DecrementDeckCardsInCollection(wCurDeckCards_ADDR);
		uint16_t destination = AddDeckToCollection(GetPointerToDeckCards());
		uint16_t source = wCurDeckCards_ADDR;
		for (uint8_t i = 0u; i < DECK_SIZE; i++)
			gb_write8(destination++, gb_read8(source++));
		uint16_t saved_name = GetPointerToDeckName();
		uint16_t name_source = wCurDeckName_ADDR;
		CopyListFromHLToDE(&name_source, &saved_name);
		uint8_t has_name = gb_read8(GetPointerToDeckName());
		DisableSRAM();
		if (has_name != 0u) {
			DrawDecksScreen(ALL_DECKS);
			DeckSelectionMenu_InitMenuParams(wCurDeck);
			return;
		}

get_input_deck_name:
		ClearMemory_Bank2(20u, wCurDeckName_ADDR);
		uint16_t old_name = GetPointerToDeckName();
		(void)CopyListFromHLToDEInSRAM(old_name, wCurDeckName_ADDR);
		InputCurDeckName();
		uint16_t new_name = GetPointerToDeckName();
		(void)CopyListFromHLToDEInSRAM(new_name, wCurDeckName_ADDR);
		DrawDecksScreen(ALL_DECKS);
		DeckSelectionMenu_InitMenuParams(wCurDeck);
		return;
	}
}
/* <<< factory DeckSelectionSubMenu */

/* >>> factory DeckSelectionSubMenu_SelectOrCancel */
void DeckSelectionSubMenu_SelectOrCancel(void)
{
	if (wCheckMenuCursorYPosition != 0u) {
		CancelDeckSelectionSubMenu();
		return;
	}

	CheckIfCurDeckIsValidResult validity = CheckIfCurDeckIsValid();
	if ((validity.f & 0x10u) != 0u) {
		DeckSelectionMenu_InitMenuParams(PrintThereIsNoDeckHereText());
		return;
	}

	EnableSRAM();
	uint8_t previous_deck = sCurrentlySelectedDeck;
	DisableSRAM();
	uint16_t product = HtimesL((uint16_t)(0x0300u | previous_deck));
	uint16_t rectangle_de = (uint16_t)(0x0200u | (uint8_t)(product + 1u));
	FillRectangle(0u, 2u, 2u, rectangle_de, 0u);

	uint8_t selected_deck = wCurDeck;
	EnableSRAM();
	sCurrentlySelectedDeck = selected_deck;
	DisableSRAM();
	DrawHandCardsTileOnCurDeck();

	uint16_t name = GetPointerToDeckName();
	EnableSRAM();
	(void)CopyDeckName(name);
	DisableSRAM();
	gb_write8(wTxRam2_ADDR, 0u);
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), 0u);
	(void)DrawWideTextBox_WaitForInput(ChosenAsDuelingDeckText);
	DeckSelectionMenu_InitMenuParams(wCurDeck);
}
/* <<< factory DeckSelectionSubMenu_SelectOrCancel */
