/* >>> part includes */
#include "home/deck_selection.h"
#include "home/duel.h"
#include "home/duel_core.h"
#include "home/empty_screen.h"
#include "home/objects.h"
#include "home/switch_rom.h"

#include "generated/text_ids.h"
#include "generated/constants.h"
/* <<< part includes */
/* >>> part MENU_CONFIRM */
#define MENU_CONFIRM 0x01u
/* <<< part MENU_CONFIRM */
/* >>> part includes_tail */
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes_tail */
/* >>> part DECK_CARD_STRIDE */
#define DECK_CARD_STRIDE DECK_COMPRESSED_STRUCT_SIZE
/* <<< part DECK_CARD_STRIDE */
/* >>> part includes_SYM_0 */
#include "generated/wram.h"

#include "mem.h"

#include "generated/wram.h"
#include "mem.h"

#include "home/switch_sram.h"
#include "home/load_deck.h"
#include "mem.h"

#include "home/deck_selection.h"
/* <<< part includes_SYM_0 */
/* >>> part INPUT_CUR_DECK_DECK1_DATA */
#define INPUT_CUR_DECK_DECK1_DATA Deck1Data_ADDR
/* <<< part INPUT_CUR_DECK_DECK1_DATA */
/* >>> part INPUT_CUR_DECK_DECK2_DATA */
#define INPUT_CUR_DECK_DECK2_DATA Deck2Data_ADDR
/* <<< part INPUT_CUR_DECK_DECK2_DATA */
/* >>> part INPUT_CUR_DECK_DECK3_DATA */
#define INPUT_CUR_DECK_DECK3_DATA Deck3Data_ADDR
/* <<< part INPUT_CUR_DECK_DECK3_DATA */
/* >>> part INPUT_CUR_DECK_DECK4_DATA */
#define INPUT_CUR_DECK_DECK4_DATA Deck4Data_ADDR
/* <<< part INPUT_CUR_DECK_DECK4_DATA */
/* >>> factory GetPointerToDeckName */
uint16_t GetPointerToDeckName(void)
{
	uint8_t deck = wCurDeck;
	uint16_t offset = HtimesL((uint16_t)(((uint16_t)deck << 8) | DECK_CARD_STRIDE));
	return (uint16_t)(sDeck1Name_ADDR + offset);
}
/* <<< factory GetPointerToDeckName */
/* --- factory CopyDeckFromSRAM */
/* --- factory Func_9001 */
/* >>> factory WriteCardListsTerminatorBytes */
WriteCardListsTerminatorBytesResult WriteCardListsTerminatorBytes(void)
{
	uint16_t filtered_terminator =
		(uint16_t)(wFilteredCardList_ADDR + MAX_NUM_CARDS_PER_TYPE * 2u);
	gb_write8(filtered_terminator, 0u);
	gb_write8((uint16_t)(filtered_terminator + 1u), 0u);
	uint16_t deck_terminator =
		(uint16_t)(wCurDeckCards_ADDR + DECK_CONFIG_BUFFER_SIZE * 2u);
	gb_write8(deck_terminator, 0u);
	gb_write8((uint16_t)(deck_terminator + 1u), 0u);
	return (WriteCardListsTerminatorBytesResult){
		0u, 0x80u, 0u, (uint8_t)(MAX_NUM_CARDS_PER_TYPE * 2u),
		(uint16_t)(deck_terminator + 1u)};
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
		CompressDeckToSRAM(wCurDeckCards_ADDR, destination);
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
/* === factory CheckIfCurDeckIsValid */
