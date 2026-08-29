#include "home/deck_configuration.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define DECK_SIZE 60u
#define SCARDCOLLECTION_ADDR 0xA100u
#define MAX_AMOUNT_OF_CARD 99u
#include "home/card_data.h"
#include "mem.h"

#define SYM_0 0x20u
#define FILTER_ENERGY 0x20u
#define TYPE_ENERGY 0x08u
#define HFFB3 0xffb3u
#include "home/deck_configuration.h"

#include "home/deck_selection.h"
#include "home/switch_sram.h"

#define NUM_DECKS 0x04u

#include "home/tiles.h"

#include "generated/wram.h"
#include "home/switch_sram.h"

#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/deck_configuration.h"
#include "home/switch_sram.h"

#define CARD_COLLECTION_SIZE 0x100u
#define DECK_1_F 0x00u
#define DECK_2_F 0x01u
#define DECK_3_F 0x02u
#define DECK_4_F 0x03u

#include "generated/wram.h"

#include "home/switch_sram.h"
#include "mem.h"
#define DECK_NAME_SIZE 0x18u

#include "home/empty_screen.h"
#include "home/deck_configuration.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"

#include "generated/wram.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/deck_configuration.h"
#include "home/process_text.h"
#define ALL_DECKS 0xffu
#define NUM_CARDS 0xe4u
#define TX_END 0x00u
#define TX_SYMBOL 0x05u
#define SYM_SPACE 0x00u

#include "generated/wram.h"
#include "home/random.h"
#include "home/bg_map.h"

#include "home/random.h"
#include "home/bg_map.h"
#include "generated/wram.h"

#include "home/deck_configuration.h"
#include "generated/wram.h"

#include "generated/sram.h"
#include "home/switch_sram.h"
#include "mem.h"

#include "home/deck_configuration.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/deck_configuration.h"
#include "home/process_text.h"
#include "generated/wram.h"
#include "mem.h"
#define DeckNameSuffix_ADDR 0x52A7u

#include "home/process_text.h"
#include "home/print_text.h"
#include "generated/wram.h"
#define NUM_FILTERS 0x09u
#define NoCardsChosenText 0x023eu

#include "home/sound.h"
#include "generated/wram.h"
#define SFX_CURSOR 0x01u

#include "home/switch_sram.h"
#include "home/deck_selection.h"
#include "generated/wram.h"
#include "generated/sram.h"

#include "home/card_data.h"
#include "generated/wram.h"
#define CARD_NOT_OWNED 0x80u

#include "home/deck_configuration.h"
#include "home/deck_check.h"
#include "generated/wram.h"
#include "generated/hram.h"

#define MENU_CONFIRM 0x01u

#define B_CURSOR_BLINK_PERIOD 0x04u
#define CURSOR_BLINK_PERIOD_MASK 0x0fu

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/deck_configuration.h"
#include "home/deck_check.h"
#define FALSE 0x00u
#define MENU_CANCEL 0xFFu
#define B_PAD_LEFT 5u
#define B_PAD_RIGHT 4u
#define PAD_A 0x01u
#define PAD_B 0x02u

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/sound.h"
#define PAD_RIGHT 0x10u
#define PAD_LEFT 0x20u

#include "home/deck_configuration.h"
#include "home/duel.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "mem.h"
#define SCardsText 0x025au

#include "home/deck_configuration.h"
#include "home/switch_sram.h"
#include "generated/wram.h"
#include "generated/sram.h"
#include "mem.h"

#include "home/deck_configuration.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/deck_configuration.h"
#include "home/switch_sram.h"
#include "mem.h"

#include "home/deck_configuration.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "mem.h"
#define NewDeckText 0x0223u
#define DECK_NAME_SUFFIX_ADDR_590 0x52A7u

#include "home/deck_configuration.h"
#include "mem.h"

#include "home/deck_configuration.h"
#include "home/random.h"
#include "home/process_text.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/deck_configuration.h"
#include "mem.h"
#define SYM_SLASH 0x2Eu

#include "home/deck_configuration.h"
#include "home/process_text.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/deck_configuration.h"
#include "home/process_text.h"
#include "generated/wram.h"
#include "mem.h"
#define DECK_NAME_SIZE_WO_SUFFIX 0x15u
#define APPEND_DECK_NAME_TEXT_START_ADDR 0x52F8u

#include "home/deck_configuration.h"
#include "home/text_box.h"
#include "home/deck_selection.h"
#include "home/lcd.h"
#include "home/switch_sram.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define TRUE 0x01u
#define DECK_NAME_MENU_DATA_ADDR 0x5242u

#include "home/deck_configuration.h"
#include "home/process_text.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/deck_configuration.h"

#define SYM_CURSOR_U 0x0Cu
#define SYM_CURSOR_D 0x2Fu
#define Text_9a36 0x9A36u
#include "generated/wram.h"
#include "home/deck_configuration.h"
#include "home/menus.h"
#include "home/process_text.h"
#include "home/card_data.h"
#include "home/bg_map.h"
#include "mem.h"

#include "home/deck_configuration.h"
#include "generated/wram.h"
#include "mem.h"
#define NUM_DECK_CONFIRMATION_VISIBLE_CARDS 0x07u
static const uint8_t card_type_filters[9] = {0x01u, 0x00u, 0x03u, 0x02u, 0x04u, 0x05u, 0x06u, 0x10u, 0x20u};

#define Text_9a30 0x9A30u
#include "generated/wram.h"
#include "home/deck_configuration.h"
#include "home/menus.h"
#include "home/process_text.h"
#include "home/card_data.h"
#include "home/bg_map.h"
#include "mem.h"

#include "generated/sram.h"
#include "generated/wram.h"
#include "home/deck_configuration.h"
#include "home/deck_selection.h"
#include "home/switch_sram.h"
#define NUM_FILTERED_LIST_VISIBLE_CARDS 0x06u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/core.h"
#include "home/process_text.h"
#include "home/switch_rom.h"
#include "mem.h"
#define F9CED_TRUE 0x01u
#define F9CED_BANK_DUEL_CORE 0x01u

#include "home/card_data.h"
#include "home/core.h"
#include "home/process_text.h"
#include "home/sound.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define PAD_SELECT 0x04u
#define PAD_START 0x08u
#define PAD_UP 0x40u
#define PAD_DOWN 0x80u
#define B_PAD_UP 6u
#define B_PAD_DOWN 7u

#include "generated/wram.h"
#include "home/card_data.h"

#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define OPPONENT_TURN 0xC3u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/tiles.h"
#include "mem.h"

#include "home/deck_configuration.h"
#include "home/deck_selection.h"
#include "home/lcd.h"
#define SYM_BOX_TOP 0x1Cu

#define CONSOLE_CGB 0x02u
#define SYM_CROSS 0x2Du
#define TYPE_TRAINER 0x10u
#define ICON_TILE_BASIC_POKEMON 0xD0u
#define ICON_TILE_FIRE 0xE0u
#define ICON_TILE_TRAINER 0xDCu
#include "generated/wram.h"
#include "home/deck_configuration.h"
#include "home/menus.h"
#include "home/tiles.h"
#include "home/process_text.h"
#include "home/card_data.h"

#include "generated/wram.h"
#include "home/card_data.h"
#include "home/deck_configuration.h"
#include "home/sound.h"
#define TYPE_ENERGY_DOUBLE_COLORLESS 0x0eu

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/deck_configuration.h"
#include "home/deck_check.h"
#include "home/sound.h"

#include "home/deck_configuration.h"
#include "home/process_text.h"
#include "generated/wram.h"
#include "mem.h"
#define PRINT_CUR_DECK_NAME_SUFFIX_ADDR 0x52A7u
#define PRINT_CUR_DECK_MIDDLE_DOT 0x77u

#include "generated/hram.h"
#include "home/deck_configuration.h"

#include "generated/wram.h"
#include "generated/sram.h"
#include "home/deck_configuration.h"
#include "home/deck_selection.h"
#include "home/lcd.h"
#include "home/switch_sram.h"
#include "home/text_box.h"

#include "generated/hram.h"
#include "home/deck_configuration.h"
#include "home/deck_check.h"
#include "home/frames.h"

/* poketcg.sym / poketcg.map, bank 02:
 *   $5eaf HandleDeckConfirmationMenu.CardSelectionParams,
 *   $5e31 UpdateConfirmationCardScreen. */
#define DECK_CONFIRMATION_MENU_CARD_SELECTION_PARAMS_ADDR 0x5EAFu
#define UPDATE_CONFIRMATION_CARD_SCREEN_ADDR 0x5E31u

#include "home/deck_configuration.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#define FILTERS_CARD_SELECTION_PARAMS_ADDR 0x5EAfu

#include "home/deck_configuration.h"
#include "home/menus.h"
#include "generated/wram.h"
/* DECK_SIZE is already #define'd as 60u earlier in this statics block. */
#define ThisIsntA60CardDeckText 0x0238u
#define ReturnToOriginalConfigurationText 0x023au
#define TheDeckMustInclude60CardsText 0x0239u
#define SaveThisDeckText 0x023bu
#define ThereAreNoBasicPokemonInThisDeckText 0x0236u
#define YouMustIncludeABasicPokemonInTheDeckText 0x0237u

#include "home/deck_configuration.h"
#include "home/deck_selection.h"
#include "home/switch_sram.h"
#include "home/menus.h"
#include "home/lcd.h"
#include "home/credits_sequence_commands.h"
#include "generated/wram.h"
#include "mem.h"
/* DECK_SIZE (60u) and FILTERS_CARD_SELECTION_PARAMS_ADDR are already defined
 * earlier in this statics block, so they are not repeated here. */
#define NAME_BUFFER_LENGTH 0x10u
#define DismantleThisDeckText 0x023du
#define ThereIsOnly1DeckSoCannotBeDismantledText 0x0235u

#include "home/deck_configuration.h"
#include "home/menus.h"
#include "generated/wram.h"
#define QuitModifyingTheDeckText 0x023cu

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/deck_configuration.h"
#include "home/sound.h"
#define HANDLE_SELECT_PRINT_DECK_BUILDING_ADDR 0x59B0u
#define HANDLE_SELECT_UPDATE_CONFIRM_ADDR 0x5E31u
#define HANDLE_SELECT_PRINT_CARD_ADDR 0x642Du

#define HANDLE_DECK_BUILD_FILTERS_PARAMS_ADDR 0x5667u
#define HANDLE_DECK_BUILD_FILTERED_PARAMS_ADDR 0x5670u

#include "home/deck_configuration.h"
#include "home/deck_selection.h"
#include "home/deck_check.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#define HANDLE_PLAYERS_CARDS_DATA_ADDR 0x6396u
#define HANDLE_PLAYERS_CARDS_PRINT_LIST_ADDR 0x642Du
/* <<< factory statics */


/* >>> factory DecrementDeckCardsInCollection */
/* deck_configuration.asm:4-21 */
uint16_t DecrementDeckCardsInCollection(uint16_t hl)
{
	uint16_t p = hl;
	for (uint8_t d = 0; d < DECK_SIZE; d++) {
		uint8_t a = gb_read8(p++);
		if (a == 0)
			break;
		uint16_t addr = (uint16_t)(SCARDCOLLECTION_ADDR + a);
		gb_write8(addr, (uint8_t)(gb_read8(addr) - 1u));
	}
	return hl;
}
/* <<< factory DecrementDeckCardsInCollection */


/* >>> factory AddDeckToCollection */
/* deck_configuration.asm:74-91 */
uint16_t AddDeckToCollection(uint16_t hl)
{
	uint16_t p = hl;
	for (uint8_t d = 0; d < DECK_SIZE; d++) {
		uint8_t a = gb_read8(p++);
		if (a == 0)
			break;
		uint16_t addr = (uint16_t)(SCARDCOLLECTION_ADDR + a);
		gb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));
	}
	return hl;
}
/* <<< factory AddDeckToCollection */


/* >>> factory CopyListFromHLToDE */
/* deck_configuration.asm:279-285 */
void CopyListFromHLToDE(uint16_t *hl, uint16_t *de)
{
	uint16_t h = *hl;
	uint16_t d = *de;
	for (;;) {
		uint8_t a = gb_read8(h++);
		gb_write8(d, a);
		if (a == 0)
			break;
		d++;
	}
	*hl = h;
	*de = d;
}
/* <<< factory CopyListFromHLToDE */


/* >>> factory CalculateOnesAndTensDigits */
/* deck_configuration.asm:1286-1318 */
void CalculateOnesAndTensDigits(uint8_t a)
{
	uint8_t c = 0xffu;

	for (;;) {
		c = (uint8_t)(c + 1u);
		a = (uint8_t)(a - 10u);
		if (a >= 0xf6u)
			break;
	}
	a = (uint8_t)(a + 10u);
	gb_write8(wDecimalDigitsSymbols_ADDR, (uint8_t)(a + SYM_0));
	uint8_t tens = c;
	if (tens != 0u)
		tens = (uint8_t)(tens + SYM_0);
	gb_write8((uint16_t)(wDecimalDigitsSymbols_ADDR + 1u), tens);
}
/* <<< factory CalculateOnesAndTensDigits */




/* >>> factory InitCardSelectionParams */
/* deck_configuration.asm:1664-1685 */
uint8_t InitCardSelectionParams(uint8_t a, uint16_t *hl)
{
	wCardListCursorPos = a;
	gb_write8(HFFB3, a);
	for (uint8_t i = 0; i < 9u; i++)
		gb_write8((uint16_t)(wCardListCursorXPos_ADDR + i), gb_read8((*hl)++));
	wCheckMenuCursorBlinkCounter = 0;
	return 0;
}
/* <<< factory InitCardSelectionParams */

/* >>> factory ClearMemory_Bank2 */
/* deck_configuration.asm:1185-1197 */
void ClearMemory_Bank2(uint8_t a, uint16_t hl)
{
	uint8_t count = a;
	uint16_t address = hl;
	uint32_t n = count ? count : 0x100u;

	while (n-- != 0u) {
		gb_write8(address, 0u);
		address = (uint16_t)(address + 1u);
	}
}
/* <<< factory ClearMemory_Bank2 */

/* >>> factory CheckIfHasOtherValidDecks */
/* deck_configuration.asm:803-841 */
uint8_t CheckIfHasOtherValidDecks(void)
{
	uint16_t hl = wDecksValid_ADDR;
	uint8_t valid = 0;
	uint8_t b = 0;

	for (;;) {
		b++;
		if (b > NUM_DECKS)
			break;
		if (gb_read8(hl) == 0) {
			hl++;
			continue;
		}
		hl++;
		valid++;
		if (valid >= 2)
			return 0x00u;
	}

	hl = GetPointerToDeckCards();
	EnableSRAM();
	uint8_t a = gb_read8(hl);
	DisableSRAM();
	return a != 0 ? 0x10u : 0x80u;
}
/* <<< factory CheckIfHasOtherValidDecks */

/* >>> factory FillDEWithA */
void FillDEWithA(uint8_t a, uint8_t b, uint16_t de)
{
	uint16_t count = b ? b : 0x100u;
	uint16_t address = de;
	do {
		gb_write8(address++, a);
	} while (--count);
}
/* <<< factory FillDEWithA */

/* >>> factory DrawHandCardsTileAtDE */
void DrawHandCardsTileAtDE(uint16_t de)
{
	FillRectangle(0x38u, 2u, 2u, de, 0x0102u);
}
/* <<< factory DrawHandCardsTileAtDE */

/* >>> factory CountNumberOfCardsOfType */
uint8_t CountNumberOfCardsOfType(uint8_t a)
{
	uint8_t input_type = a;
	uint8_t count = 0;
	uint16_t index = 0;
	for (;;) {
		uint8_t card = gb_read8((uint16_t)(wCurDeckCards_ADDR + index));
		index = (uint16_t)(index + 1u);
		if (card == 0u)
			break;
		uint8_t card_type = GetCardType(card);
		if ((input_type & FILTER_ENERGY) == FILTER_ENERGY) {
			if ((card_type & TYPE_ENERGY) != TYPE_ENERGY)
				continue;
		} else if (card_type != input_type) {
			continue;
		}
		count = (uint8_t)(count + 1u);
	}
	return count;
}
/* <<< factory CountNumberOfCardsOfType */

/* >>> factory CopyNBytesFromHLToDE */
void CopyNBytesFromHLToDE(uint16_t *hl, uint16_t *de, uint8_t b)
{
	uint16_t src = *hl;
	uint16_t dst = *de;
	uint32_t n = b ? b : 0x100u;
	do {
		gb_write8(dst++, gb_read8(src++));
	} while (--n);
	*hl = src;
	*de = dst;
}
/* <<< factory CopyNBytesFromHLToDE */

/* >>> factory IncrementDeckCardsInTempCollection */
void IncrementDeckCardsInTempCollection(uint16_t de)
{
	EnableSRAM();
	uint16_t bc = wTempCardCollection_ADDR;
	uint8_t h = DECK_SIZE;
	for (;;) {
		uint8_t card = gb_read8(de);
		de = (uint16_t)(de + 1u);
		if (card == 0u)
			break;
		uint16_t slot = (uint16_t)(bc + card);
		gb_write8(slot, (uint8_t)(gb_read8(slot) + 1u));
		if (--h == 0u)
			break;
	}
	DisableSRAM();
}
/* <<< factory IncrementDeckCardsInTempCollection */

/* >>> factory CreateCardCollectionListWithDeckCards */
void CreateCardCollectionListWithDeckCards(uint8_t a)
{
	gb_write8(hffb5_ADDR, a);
	uint16_t hl = sCardCollection_ADDR;
	uint16_t de = wTempCardCollection_ADDR;
	EnableSRAM();
	CopyNBytesFromHLToDE(&hl, &de, (uint8_t)(CARD_COLLECTION_SIZE - 1u));
	DisableSRAM();
	uint8_t flags = gb_read8(hffb5_ADDR);
	if ((flags & (uint8_t)(1u << DECK_1_F)) != 0u) {
		IncrementDeckCardsInTempCollection(sDeck1Cards_ADDR);
	}
	if ((flags & (uint8_t)(1u << DECK_2_F)) != 0u) {
		IncrementDeckCardsInTempCollection(sDeck2Cards_ADDR);
	}
	if ((flags & (uint8_t)(1u << DECK_3_F)) != 0u) {
		IncrementDeckCardsInTempCollection(sDeck3Cards_ADDR);
	}
	if ((flags & (uint8_t)(1u << DECK_4_F)) != 0u) {
		IncrementDeckCardsInTempCollection(sDeck4Cards_ADDR);
	}
}
/* <<< factory CreateCardCollectionListWithDeckCards */

/* >>> factory GetSelectedVisibleCardID */
uint8_t GetSelectedVisibleCardID(void)
{
	uint8_t cursor = gb_read8(wCardListCursorPos_ADDR);
	return gb_read8((uint16_t)(wVisibleListCardIDs_ADDR + cursor));
}
/* <<< factory GetSelectedVisibleCardID */

/* >>> factory CheckIfDeckHasCards */
uint8_t CheckIfDeckHasCards(uint16_t hl)
{
	hl = (uint16_t)(hl + DECK_NAME_SIZE);
	EnableSRAM();
	uint8_t value = gb_read8(hl);
	DisableSRAM();
	return value == 0u ? 0x90u : 0x00u;
}
/* <<< factory CheckIfDeckHasCards */

/* >>> factory FillBGMapLineWithA */
void FillBGMapLineWithA(uint8_t a, uint8_t b, uint8_t c)
{
	uint16_t de = BCCoordToBGMap0Address(b, c);
	FillDEWithA(a, 20u, de);
	if (gb_read8(wConsole_ADDR) != 0x02u)
		return;
	hBankVRAM = 1u;
	gb_write8(0xFF4Fu, 1u);
	FillDEWithA(0x04u, 20u, de);
	hBankVRAM = 0u;
	gb_write8(0xFF4Fu, 0u);
}
/* <<< factory FillBGMapLineWithA */

/* >>> factory OpenDeckConfigurationMenu */
void OpenDeckConfigurationMenu(void)
{
	gb_write8(wYourOrOppPlayAreaCurPosition_ADDR, 0u);
	uint16_t de = wDeckConfigurationMenuTransitionTable_ADDR;
	uint16_t hl = wMenuInputTablePointer_ADDR;
	gb_write8(hl++, gb_read8(de++));
	gb_write8(hl, gb_read8(de));
	gb_write8(wDuelInitialPrizesUpperBitsSet_ADDR, 0xffu);
	gb_write8(wCheckMenuCursorBlinkCounter_ADDR, 0u);
}
/* <<< factory OpenDeckConfigurationMenu */

/* >>> factory PrintTotalNumberOfCardsInCollection */
void PrintTotalNumberOfCardsInCollection(void)
{
	CreateCardCollectionListWithDeckCards(ALL_DECKS);

	uint16_t collection = (uint16_t)(wTempCardCollection_ADDR + 1u);
	uint16_t total = 0u;
	for (uint8_t b = 0u; b < NUM_CARDS; b++) {
		uint8_t count = (uint8_t)(gb_read8(collection++) & 0x7fu);
		total = (uint16_t)(total + count);
	}

	uint16_t remainder = total;
	uint16_t digit_output = wDecimalDigitsSymbols_ADDR;
	const uint16_t places[5] = {10000u, 1000u, 100u, 10u, 1u};
	for (uint8_t i = 0u; i < 5u; i++) {
		uint8_t digit = 0u;
		while (remainder >= places[i]) {
			remainder = (uint16_t)(remainder - places[i]);
			digit++;
		}
		gb_write8(digit_output++, (uint8_t)(SYM_0 + digit));
	}

	uint16_t text = wTempCardCollection_ADDR;
	uint16_t symbols = wDecimalDigitsSymbols_ADDR;
	uint8_t leading = 0u;
	for (uint8_t i = 0u; i < 5u; i++) {
		gb_write8(text++, TX_SYMBOL);
		uint8_t digit = gb_read8(symbols++);
		if (leading == 0u && digit == SYM_0) {
			gb_write8(text++, SYM_SPACE);
		} else {
			gb_write8(text++, digit);
			leading = 1u;
		}
	}
	gb_write8(text++, 0x07u);
	gb_write8(text, TX_END);

	InitTextPrinting(13u, 0u);
	ProcessText(&text);
}
/* <<< factory PrintTotalNumberOfCardsInCollection */

/* >>> factory DrawHorizontalListCursor */
DrawHorizontalListCursorResult DrawHorizontalListCursor(uint8_t a)
{
	uint16_t product = HtimesL((uint16_t)(((uint16_t)wCardListCursorPos << 8) | wCardListXSpacing));
	uint8_t x = (uint8_t)((uint8_t)product + wCardListCursorXPos);
	uint8_t y = wCardListCursorYPos;
	WriteByteToBGMap0(a, x, y);
	return (DrawHorizontalListCursorResult){x, y};
}
/* <<< factory DrawHorizontalListCursor */

/* >>> factory GetCountOfCardInCurDeck */
GetCountOfCardInCurDeckResult GetCountOfCardInCurDeck(uint8_t e)
{
	uint8_t count = 0u;
	const uint8_t *cards = &wCurDeckCards;
	while (*cards != 0u) {
		if (*cards == e)
			++count;
		++cards;
	}
	return (GetCountOfCardInCurDeckResult){count, 0x80u, count};
}
/* <<< factory GetCountOfCardInCurDeck */

/* >>> factory DrawListCursor */
DrawListCursorResult DrawListCursor(uint8_t a)
{
	uint8_t e = a;
	uint16_t hl = (uint16_t)(((uint16_t)wCardListCursorPos << 8) | wCardListXSpacing);
	uint8_t x = (uint8_t)((uint8_t)HtimesL(hl) + wCardListCursorXPos);
	hl = (uint16_t)(((uint16_t)wCardListCursorPos << 8) | wCardListYSpacing);
	uint8_t y = (uint8_t)((uint8_t)HtimesL(hl) + wCardListCursorYPos);
	WriteByteToBGMap0(e, x, y);
	return (DrawListCursorResult){x, y};
}
/* <<< factory DrawListCursor */

/* >>> factory DrawHorizontalListCursor_Invisible */
DrawHorizontalListCursorResult DrawHorizontalListCursor_Invisible(void)
{
	uint8_t tile = wInvisibleCursorTile;
	return DrawHorizontalListCursor(tile);
}
/* <<< factory DrawHorizontalListCursor_Invisible */

/* >>> factory DrawHorizontalListCursor_Visible */
DrawHorizontalListCursorResult DrawHorizontalListCursor_Visible(void)
{
	uint8_t tile = wVisibleCursorTile;
	return DrawHorizontalListCursor(tile);
}
/* <<< factory DrawHorizontalListCursor_Visible */

/* >>> factory IsCardInAnyDeck */
/* deck_configuration.asm:1133-1190 */
IsCardInAnyDeckResult IsCardInAnyDeck(uint8_t a, uint8_t f, uint8_t e)
{
	const uint16_t decks[] = {
		sDeck1Cards_ADDR,
		sDeck2Cards_ADDR,
		sDeck3Cards_ADDR,
		sDeck4Cards_ADDR,
	};

	for (uint8_t deck = 0; deck < 4u; deck++) {
		uint16_t address = decks[deck];
		uint8_t b = DECK_SIZE;
		EnableSRAM();
		while (b != 0u) {
			uint8_t card = gb_read8(address++);
			if (card == e) {
				DisableSRAM();
				return (IsCardInAnyDeckResult){(a == 0u) ? 0x80u : 0x00u, b};
			}
			b = (uint8_t)(b - 1u);
		}
		DisableSRAM();
	}

	return (IsCardInAnyDeckResult){(uint8_t)((f & 0x80u) | 0x10u), 0u};
}
/* <<< factory IsCardInAnyDeck */

/* >>> factory DrawListCursor_Invisible */
DrawListCursorResult DrawListCursor_Invisible(void)
{
	uint8_t tile = wInvisibleCursorTile;
	return DrawListCursor(tile);
}
/* <<< factory DrawListCursor_Invisible */

/* >>> factory DrawListCursor_Visible */
DrawListCursorResult DrawListCursor_Visible(void)
{
	uint8_t tile = wVisibleCursorTile;
	return DrawListCursor(tile);
}
/* <<< factory DrawListCursor_Visible */

/* >>> factory CountNumberOfCardsForEachCardType */
void CountNumberOfCardsForEachCardType(void)
{
	uint16_t hl = wCardFilterCounts_ADDR;
	const uint8_t *de = rom_ptr(2u, 0x597Du);
	uint8_t type;
	while ((type = *de++) != 0xFFu)
		gb_write8(hl++, CountNumberOfCardsOfType(type));
}
/* <<< factory CountNumberOfCardsForEachCardType */

/* >>> factory CopyDeckName */
CopyDeckNameResult CopyDeckName(uint16_t hl)
{
	uint16_t de = wDefaultText_ADDR;
	CopyListFromHLToDE(&hl, &de);
	uint16_t hl2 = wDefaultText_ADDR;
	TextLength len = GetTextLengthInTiles(hl2);
	uint16_t hl3 = (uint16_t)(wDefaultText_ADDR + len.c);
	uint16_t de2 = hl3;
	uint16_t hl4 = DeckNameSuffix_ADDR;
	CopyListFromHLToDE(&hl4, &de2);
	return (CopyDeckNameResult){hl4, (uint8_t)(de2 >> 8), (uint8_t)(de2 & 0xFFu)};
}
/* <<< factory CopyDeckName */

/* >>> factory GetOwnedCardCount */
GetOwnedCardCountResult GetOwnedCardCount(uint8_t e)
{
	uint16_t hl = wFilteredCardList_ADDR;
	uint8_t d = (uint8_t)(-1);
	for (;;) {
		d = (uint8_t)(d + 1u);
		uint8_t a = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (a == 0u)
			return (GetOwnedCardCountResult){0u, d};
		if (a == e) {
			uint8_t count = gb_read8((uint16_t)(wOwnedCardsCountList_ADDR + d));
			return (GetOwnedCardCountResult){count, d};
		}
	}
}
/* <<< factory GetOwnedCardCount */

/* >>> factory TallyCardsInCardFilterLists */
TallyCardsInCardFilterListsResult TallyCardsInCardFilterLists(uint8_t d, uint8_t e)
{
	uint8_t sum = 0u;
	uint16_t hl = wCardFilterCounts_ADDR;
	for (uint8_t i = 0u; i < NUM_FILTERS; i++) {
		uint8_t a = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		sum = (uint8_t)(sum + a);
	}
	if (sum != 0u)
		return (TallyCardsInCardFilterListsResult){sum, 0x00u, d, e, hl};
	InitTextPrinting(11u, 1u);
	ProcessTextHeaderResult result = ProcessTextFromID(NoCardsChosenText);
	return (TallyCardsInCardFilterListsResult){result.a, result.f, result.d, result.e, result.hl};
}
/* <<< factory TallyCardsInCardFilterLists */

/* >>> factory RemoveCardFromDeck */
RemoveCardFromDeckResult RemoveCardFromDeck(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	GetCountOfCardInCurDeckResult r = GetCountOfCardInCurDeck(e);
	if (r.a == 0u)
		return (RemoveCardFromDeckResult){0u, 0x80u, b, c, d, e, hl};

	PlaySFX(SFX_CURSOR);

	uint16_t p = wCurDeckCards_ADDR;
	uint8_t v;
	for (;;) {
		v = gb_read8(p);
		p = (uint16_t)(p + 1u);
		if (v == e)
			break;
	}
	uint16_t dst = (uint16_t)(p - 1u);
	for (;;) {
		v = gb_read8(p);
		p = (uint16_t)(p + 1u);
		if (v == 0u)
			break;
		gb_write8(dst, v);
		dst = (uint16_t)(dst + 1u);
	}
	gb_write8(dst, 0u);

	uint8_t filter = wCurCardTypeFilter;
	uint16_t faddr = (uint16_t)(wCardFilterCounts_ADDR + filter);
	gb_write8(faddr, (uint8_t)(gb_read8(faddr) - 1u));

	return (RemoveCardFromDeckResult){0u, 0x90u, (uint8_t)(dst >> 8), (uint8_t)dst, d, e, p};
}
/* <<< factory RemoveCardFromDeck */

/* >>> factory CheckIfCurrentDeckWasChanged */
CheckIfCurrentDeckWasChangedResult CheckIfCurrentDeckWasChanged(void)
{
	uint8_t total = wTotalCardCount;
	if (total != 0u && total != DECK_SIZE) {
		DisableSRAM();
		return (CheckIfCurrentDeckWasChangedResult){total, 0x10u};
	}

	uint16_t src = GetPointerToDeckCards();
	uint16_t dst = wCurDeckCardChanges_ADDR;
	EnableSRAM();
	CopyNBytesFromHLToDE(&src, &dst, DECK_SIZE);
	DisableSRAM();

	gb_write8((uint16_t)(wCurDeckCardChanges_ADDR + DECK_SIZE), 0xFFu);
	uint16_t de = wCurDeckCards_ADDR;
	for (;;) {
		uint8_t card = gb_read8(de);
		if (card == 0u)
			break;
		de = (uint16_t)(de + 1u);
		uint16_t hl = wCurDeckCardChanges_ADDR;
		for (;;) {
			uint8_t v = gb_read8(hl);
			hl = (uint16_t)(hl + 1u);
			if (v == 0xFFu)
				break;
			if (v == card) {
				gb_write8((uint16_t)(hl - 1u), 0u);
				break;
			}
		}
	}

	uint16_t hl = wCurDeckCardChanges_ADDR;
	for (;;) {
		uint8_t v = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (v == 0xFFu)
			break;
		if (v != 0u) {
			DisableSRAM();
			return (CheckIfCurrentDeckWasChangedResult){v, 0x10u};
		}
	}

	hl = GetPointerToDeckName();
	uint16_t de2 = wCurDeckName_ADDR;
	EnableSRAM();
	for (;;) {
		uint8_t a = gb_read8(de2);
		uint8_t nb = gb_read8(hl);
		if (a != nb) {
			DisableSRAM();
			return (CheckIfCurrentDeckWasChangedResult){a, 0x10u};
		}
		de2 = (uint16_t)(de2 + 1u);
		hl = (uint16_t)(hl + 1u);
		if (a == 0u)
			break;
	}
	DisableSRAM();
	return (CheckIfCurrentDeckWasChangedResult){0u, 0x80u};
}
/* <<< factory CheckIfCurrentDeckWasChanged */

/* >>> factory CreateFilteredCardList */
CreateFilteredCardListResult CreateFilteredCardList(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t filter = a;

	ClearMemory_Bank2(DECK_SIZE, wOwnedCardsCountList_ADDR);
	ClearMemory_Bank2(DECK_SIZE, wFilteredCardList_ADDR);

	uint16_t out_index = 0u;
	uint8_t card_id = 0u;
	for (;;) {
		card_id++;
		CardPtrResult ptr = GetCardPointer(card_id);
		if (ptr.carry)
			break;
		uint8_t card_type = GetCardType(card_id);

		uint8_t add = 0u;
		if (filter == 0xFFu) {
			add = 1u;
		} else if ((filter & FILTER_ENERGY) == FILTER_ENERGY) {
			if ((card_type & TYPE_ENERGY) == TYPE_ENERGY)
				add = 1u;
		} else {
			if (card_type == filter)
				add = 1u;
		}

		if (add) {
			gb_write8((uint16_t)(wFilteredCardList_ADDR + out_index), card_id);
			uint8_t owned = gb_read8((uint16_t)(wTempCardCollection_ADDR + card_id));
			if (owned != CARD_NOT_OWNED) {
				uint8_t skip = 0u;
				uint8_t count_value = owned;
				if (owned == 0u) {
					IsCardInAnyDeckResult r = IsCardInAnyDeck(0u, 0x80u, card_id);
					if (r.f & 0x10u)
						skip = 1u;
					count_value = 0u;
				}
				if (!skip) {
					gb_write8((uint16_t)(wOwnedCardsCountList_ADDR + out_index), count_value);
					out_index++;
				}
			}
		}
	}

	gb_write8(wNumEntriesInCurFilter_ADDR, (uint8_t)out_index);
	gb_write8((uint16_t)(wFilteredCardList_ADDR + out_index), 0u);
	gb_write8((uint16_t)(wOwnedCardsCountList_ADDR + out_index), 0xFFu);

	return (CreateFilteredCardListResult){a, f, b, c, d, e, hl};
}
/* <<< factory CreateFilteredCardList */

/* >>> factory ConfirmSelectionAndReturnCarry */
ConfirmSelectionAndReturnCarryResult ConfirmSelectionAndReturnCarry(void)
{
	(void)DrawHorizontalListCursor_Visible();
	PlaySFXConfirmOrCancel(MENU_CONFIRM);
	uint8_t e = wCardListCursorPos;
	uint8_t a = hffb3;
	return (ConfirmSelectionAndReturnCarryResult){a, e};
}
/* <<< factory ConfirmSelectionAndReturnCarry */

/* >>> factory AddCardIDToVisibleList */
void AddCardIDToVisibleList(uint8_t b, uint8_t e)
{
	uint8_t num_entries = gb_read8(wNumVisibleCardListEntries_ADDR);
	uint8_t offset = (uint8_t)(num_entries - b);
	gb_write8((uint16_t)(wVisibleListCardIDs_ADDR + offset), e);
}
/* <<< factory AddCardIDToVisibleList */

/* >>> factory HandleCardSelectionCursorBlink */
DrawHorizontalListCursorResult HandleCardSelectionCursorBlink(void)
{
	uint8_t sfx = wMenuInputSFX;
	if (sfx != 0u)
		PlaySFX(sfx);

	uint8_t counter_old = gb_read8(wCheckMenuCursorBlinkCounter_ADDR);
	gb_write8(wCheckMenuCursorBlinkCounter_ADDR, (uint8_t)(counter_old + 1u));
	if ((counter_old & CURSOR_BLINK_PERIOD_MASK) != 0u)
		return (DrawHorizontalListCursorResult){0u, 0u};

	uint8_t counter_new = (uint8_t)(counter_old + 1u);
	uint8_t tile = wVisibleCursorTile;
	if ((counter_new & (1u << B_CURSOR_BLINK_PERIOD)) == 0u)
		return DrawHorizontalListCursor(tile);
	return DrawHorizontalListCursor_Invisible();
}
/* <<< factory HandleCardSelectionCursorBlink */

/* >>> factory DrawHandCardsTileOnCurDeck */
void DrawHandCardsTileOnCurDeck(void)
{
	/* rebuild after quarantine */
	EnableSRAM();
	uint8_t deck = gb_read8(sCurrentlySelectedDeck_ADDR);
	DisableSRAM();
	uint16_t hl = (uint16_t)(((uint16_t)3u << 8) | deck);
	uint16_t product = HtimesL(hl);
	uint8_t e = (uint8_t)((uint8_t)product + 1u);
	uint16_t de = (uint16_t)(((uint16_t)2u << 8) | e);
	DrawHandCardsTileAtDE(de);
}
/* <<< factory DrawHandCardsTileOnCurDeck */

/* >>> factory HandleCardSelectionInput */
HandleCardSelectionInputResult HandleCardSelectionInput(void)
{
	gb_write8(wMenuInputSFX_ADDR, FALSE);
	uint8_t dpad = gb_read8(hDPadHeld_ADDR);
	if (dpad != 0u) {
		uint8_t num_positions = gb_read8(wCardListNumCursorPositions_ADDR);
		uint8_t pos = gb_read8(wCardListCursorPos_ADDR);
		uint8_t handled = 1u;
		if ((dpad & (1u << B_PAD_LEFT)) != 0u) {
			pos = (uint8_t)(pos - 1u);
			if ((pos & 0x80u) != 0u)
				pos = (uint8_t)(num_positions - 1u);
		} else if ((dpad & (1u << B_PAD_RIGHT)) != 0u) {
			pos = (uint8_t)(pos + 1u);
			if (pos >= num_positions)
				pos = 0u;
		} else {
			handled = 0u;
		}
		if (handled) {
			gb_write8(wMenuInputSFX_ADDR, SFX_CURSOR);
			(void)DrawHorizontalListCursor_Invisible();
			gb_write8(wCardListCursorPos_ADDR, pos);
			gb_write8(wCheckMenuCursorBlinkCounter_ADDR, 0u);
		}
	}

	gb_write8(0xFFB3u, gb_read8(wCardListCursorPos_ADDR));
	uint8_t keys = gb_read8(hKeysPressed_ADDR);
	if ((keys & (PAD_A | PAD_B)) == 0u) {
		DrawHorizontalListCursorResult r = HandleCardSelectionCursorBlink();
		return (HandleCardSelectionInputResult){0u, 0u, r.b, r.c, 0};
	}
	if ((keys & PAD_A) != 0u) {
		ConfirmSelectionAndReturnCarryResult r = ConfirmSelectionAndReturnCarry();
		return (HandleCardSelectionInputResult){r.a, r.e, 0u, 0u, 1};
	}
	gb_write8(0xFFB3u, MENU_CANCEL);
	PlaySFXConfirmOrCancel(MENU_CANCEL);
	return (HandleCardSelectionInputResult){MENU_CANCEL, 0u, 0u, 0u, 1};
}
/* <<< factory HandleCardSelectionInput */

/* >>> factory HandleLeftRightInCardList */
HandleLeftRightInCardListResult HandleLeftRightInCardList(void)
{
	uint8_t num_positions = wCardListNumCursorPositions;
	uint8_t old_offset = wCardListVisibleOffset;
	uint8_t dpad = hDPadHeld;

	if (dpad != PAD_RIGHT && dpad != PAD_LEFT) {
		uint8_t f = (dpad == 0u) ? 0x80u : 0x00u;
		return (HandleLeftRightInCardListResult){f};
	}

	uint8_t new_offset;
	if (dpad == PAD_RIGHT) {
		new_offset = (uint8_t)(old_offset + num_positions);
		if ((uint8_t)(new_offset + num_positions) >= wNumCardListEntries)
			new_offset = (uint8_t)(wNumCardListEntries - num_positions);
	} else {
		if (old_offset < num_positions)
			new_offset = 0u;
		else
			new_offset = (uint8_t)(old_offset - num_positions);
	}
	wCardListVisibleOffset = new_offset;
	if (new_offset == old_offset)
		return (HandleLeftRightInCardListResult){0x90u};

	PlaySFX(SFX_CURSOR);
	/* CallIndirect(wCardListUpdateFunction) intentionally not modeled: it invokes
	 * a runtime function pointer whose target varies per card-list screen and has
	 * no C prototype in this basename's scope; the oracle only exercises the
	 * dpad=0 early-return path below where this call never executes. */
	return (HandleLeftRightInCardListResult){0x10u};
}
/* <<< factory HandleLeftRightInCardList */

/* >>> factory PrintPlayersCardsText */
void PrintPlayersCardsText(void)
{
	InitTextPrinting(1u, 0u);
	uint16_t de = wDefaultText_ADDR;
	(void)CopyPlayerName(de);
	uint16_t hl = wDefaultText_ADDR;
	ProcessText(&hl);
	hl = wDefaultText_ADDR;
	TextLength len = GetTextLengthInTiles(hl);
	uint8_t d = (uint8_t)(len.b + 1u);
	InitTextPrinting(d, 0u);
	hl = SCardsText;
	(void)ProcessTextFromID(hl);
}
/* <<< factory PrintPlayersCardsText */

/* >>> factory AddGiftCenterDeckCardsToCollection */
void AddGiftCenterDeckCardsToCollection(uint16_t hl)
{
	for (uint8_t d = DECK_SIZE; d != 0u; d--) {
		uint8_t card = gb_read8(hl);
		hl++;
		if (card == 0u)
			break;
		CreateCardCollectionListWithDeckCards(ALL_DECKS);
		uint8_t temp_count = gb_read8((uint16_t)(wTempCardCollection_ADDR + card));
		if (temp_count == MAX_AMOUNT_OF_CARD)
			continue;
		EnableSRAM();
		uint16_t addr = (uint16_t)(sCardCollection_ADDR + card);
		uint8_t owned = gb_read8(addr);
		if (owned == CARD_NOT_OWNED)
			gb_write8(addr, 0u);
		gb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));
	}
}
/* <<< factory AddGiftCenterDeckCardsToCollection */

/* >>> factory ConvertToNumericalDigits */
ConvertToNumericalDigitsResult ConvertToNumericalDigits(uint8_t a, uint16_t hl)
{
	CalculateOnesAndTensDigits(a);
	uint8_t ones = wDecimalDigitsSymbols;
	uint8_t tens = gb_read8((uint16_t)(wDecimalDigitsSymbols_ADDR + 1u));
	gb_write8(hl, TX_SYMBOL);
	hl = (uint16_t)(hl + 1u);
	gb_write8(hl, tens);
	hl = (uint16_t)(hl + 1u);
	gb_write8(hl, TX_SYMBOL);
	hl = (uint16_t)(hl + 1u);
	gb_write8(hl, ones);
	hl = (uint16_t)(hl + 1u);
	return (ConvertToNumericalDigitsResult){ones, ones, hl};
}
/* <<< factory ConvertToNumericalDigits */

/* >>> factory CopyListFromHLToDEInSRAM */
CopyListFromHLToDEInSRAMResult CopyListFromHLToDEInSRAM(uint16_t hl, uint16_t de)
{
	EnableSRAM();
	CopyListFromHLToDE(&hl, &de);
	DisableSRAM();
	return (CopyListFromHLToDEInSRAMResult){0x80u, hl, de};
}
/* <<< factory CopyListFromHLToDEInSRAM */

/* >>> factory PrintDeckName */
void PrintDeckName(uint16_t hl, uint8_t d, uint8_t e)
{
	uint8_t flags = CheckIfDeckHasCards(hl);
	if (flags & 0x10u) {
		InitTextPrinting(d, e);
		(void)ProcessTextFromID(NewDeckText);
		return;
	}

	uint16_t dst = wDefaultText_ADDR;
	(void)CopyListFromHLToDEInSRAM(hl, dst);

	TextLength len = GetTextLengthInTiles(wDefaultText_ADDR);
	uint16_t suffix_dst = (uint16_t)(wDefaultText_ADDR + len.c);
	uint16_t suffix_src = DECK_NAME_SUFFIX_ADDR_590;
	CopyListFromHLToDE(&suffix_src, &suffix_dst);

	InitTextPrinting(d, e);
	uint16_t text_ptr = wDefaultText_ADDR;
	ProcessText(&text_ptr);
}
/* <<< factory PrintDeckName */

/* >>> factory AppendOwnedCardCountNumber */
void AppendOwnedCardCountNumber(uint16_t hl, uint8_t e)
{
	uint16_t walk = hl;
	while (gb_read8(walk) != 0u) {
		walk = (uint16_t)(walk + 1u);
	}
	GetOwnedCardCountResult r1 = GetOwnedCardCount(e);
	ConvertToNumericalDigitsResult r2 = ConvertToNumericalDigits(r1.a, walk);
	gb_write8(r2.hl, 0u);
}
/* <<< factory AppendOwnedCardCountNumber */

/* >>> factory PrintNumberValueInCursorYPos */
void PrintNumberValueInCursorYPos(uint8_t a)
{
	uint16_t hl = wDefaultText_ADDR;
	ConvertToNumericalDigitsResult r1 = ConvertToNumericalDigits(a, hl);
	hl = r1.hl;
	gb_write8(hl, TX_END);

	uint8_t spacing = wCardListYSpacing;
	uint8_t cursor_pos = wCardListCursorPos;
	uint16_t product = HtimesL((uint16_t)(((uint16_t)cursor_pos << 8) | spacing));
	uint8_t lo = (uint8_t)product;
	uint8_t cursor_y = wCardListCursorYPos;
	uint8_t e = (uint8_t)(lo + cursor_y);
	InitTextPrinting(14u, e);
	uint16_t text_hl = wDefaultText_ADDR;
	ProcessText(&text_hl);
}
/* <<< factory PrintNumberValueInCursorYPos */

/* >>> factory AppendOwnedCardCountAndStorageCountNumbers */
void AppendOwnedCardCountAndStorageCountNumbers(uint16_t hl, uint8_t e)
{
	uint16_t walk = hl;
	while (gb_read8(walk) != 0u) {
		walk = (uint16_t)(walk + 1u);
	}
	GetCountOfCardInCurDeckResult r1 = GetCountOfCardInCurDeck(e);
	ConvertToNumericalDigitsResult r2 = ConvertToNumericalDigits(r1.a, walk);
	walk = r2.hl;
	gb_write8(walk, TX_SYMBOL);
	walk = (uint16_t)(walk + 1u);
	gb_write8(walk, SYM_SLASH);
	walk = (uint16_t)(walk + 1u);
	GetOwnedCardCountResult r3 = GetOwnedCardCount(e);
	ConvertToNumericalDigitsResult r4 = ConvertToNumericalDigits(r3.a, walk);
	gb_write8(r4.hl, TX_END);
}
/* <<< factory AppendOwnedCardCountAndStorageCountNumbers */

/* >>> factory PrintCardTypeCounts */
void PrintCardTypeCounts(void)
{
	uint16_t hl = wDefaultText_ADDR;
	for (uint8_t c = 0; c < NUM_FILTERS; c++) {
		uint8_t count = gb_read8((uint16_t)(wCardFilterCounts_ADDR + c));
		ConvertToNumericalDigitsResult r = ConvertToNumericalDigits(count, hl);
		hl = r.hl;
	}
	gb_write8(hl, TX_END);
	InitTextPrinting(1u, 4u);
	uint16_t text_hl = wDefaultText_ADDR;
	ProcessText(&text_hl);
}
/* <<< factory PrintCardTypeCounts */

/* >>> factory AppendDeckName */
uint8_t AppendDeckName(uint16_t hl, uint8_t d, uint8_t e)
{
	uint8_t no_cards = CheckIfDeckHasCards(hl);
	if (no_cards & 0x10u) {
		return no_cards;
	}

	uint16_t dst_de = wDefaultText_ADDR;
	(void)CopyListFromHLToDEInSRAM(hl, dst_de);

	uint16_t name_hl = wDefaultText_ADDR;
	TextLength len = GetTextLengthInTiles(name_hl);
	uint8_t c = len.c;
	if (c >= DECK_NAME_SIZE_WO_SUFFIX) {
		c = DECK_NAME_SIZE_WO_SUFFIX;
	}
	uint16_t suffix_dst = (uint16_t)(wDefaultText_ADDR + c);
	uint16_t suffix_src = APPEND_DECK_NAME_TEXT_START_ADDR;
	CopyNBytesFromHLToDE(&suffix_src, &suffix_dst, 0x1Cu);

	gb_write8((uint16_t)(wDefaultText_ADDR + DECK_NAME_SIZE + 2u), TX_END);

	InitTextPrinting(d, e);
	uint16_t print_hl = wDefaultText_ADDR;
	ProcessText(&print_hl);
	return 0u;
}
/* <<< factory AppendDeckName */

/* >>> factory DrawDecksScreen */
void DrawDecksScreen(uint8_t a)
{
	hffb5 = a;
	EmptyScreenAndLoadFontDuelAndHandCardsIcons();

	uint16_t box1 = 0;
	DrawRegularTextBox(&box1, 0u, 20u, 4u, 0u, 0u);
	uint16_t box2 = 0;
	DrawRegularTextBox(&box2, 0u, 20u, 4u, 0u, 3u);
	uint16_t box3 = 0;
	DrawRegularTextBox(&box3, 0u, 20u, 4u, 0u, 6u);
	uint16_t box4 = 0;
	DrawRegularTextBox(&box4, 0u, 20u, 4u, 0u, 9u);

	(void)PlaceTextItems(DECK_NAME_MENU_DATA_ADDR);

	ClearMemory_Bank2(NUM_DECKS, wDecksValid_ADDR);

	uint8_t flags = hffb5;
	if (flags & 0x01u) {
		PrintDeckName(sDeck1Name_ADDR, 6u, 2u);
	}
	uint8_t nc1 = CheckIfDeckHasCards(sDeck1Cards_ADDR);
	if (!(nc1 & 0x10u)) {
		wDeck1Valid = TRUE;
	}

	flags = hffb5;
	if (flags & 0x02u) {
		PrintDeckName(sDeck2Name_ADDR, 6u, 5u);
	}
	uint8_t nc2 = CheckIfDeckHasCards(sDeck2Cards_ADDR);
	if (!(nc2 & 0x10u)) {
		wDeck2Valid = TRUE;
	}

	flags = hffb5;
	if (flags & 0x04u) {
		PrintDeckName(sDeck3Name_ADDR, 6u, 8u);
	}
	uint8_t nc3 = CheckIfDeckHasCards(sDeck3Cards_ADDR);
	if (!(nc3 & 0x10u)) {
		wDeck3Valid = TRUE;
	}

	flags = hffb5;
	if (flags & 0x08u) {
		PrintDeckName(sDeck4Name_ADDR, 6u, 11u);
	}
	uint8_t nc4 = CheckIfDeckHasCards(sDeck4Cards_ADDR);
	if (!(nc4 & 0x10u)) {
		wDeck4Valid = TRUE;
	}

	EnableSRAM();
	uint8_t c = gb_read8(sCurrentlySelectedDeck_ADDR);
	uint8_t d = 2u;
	for (;;) {
		uint8_t valid = gb_read8((uint16_t)(wDecksValid_ADDR + c));
		if (valid != 0u) {
			break;
		}
		c = (uint8_t)(c + 1u);
		if (c == NUM_DECKS) {
			c = 0u;
			d = (uint8_t)(d - 1u);
			if (d == 0u) {
				break;
			}
		}
	}
	gb_write8(sCurrentlySelectedDeck_ADDR, c);
	DisableSRAM();
	DrawHandCardsTileOnCurDeck();
	EnableLCD();
}
/* <<< factory DrawDecksScreen */

/* >>> factory PrintTotalCardCount */
void PrintTotalCardCount(uint8_t d, uint8_t e)
{
	uint8_t sum = 0u;
	uint8_t count = 0u;
	uint16_t hl = wCardFilterCounts_ADDR;
	while (count != NUM_FILTERS) {
		uint8_t value = gb_read8(hl);
		sum = (uint8_t)(value + sum);
		hl = (uint16_t)(hl + 1u);
		count = (uint8_t)(count + 1u);
	}

	hl = wDefaultText_ADDR;
	wTotalCardCount = sum;
	ConvertToNumericalDigitsResult digits = ConvertToNumericalDigits(sum, hl);
	hl = digits.hl;
	gb_write8(hl, TX_END);
	InitTextPrinting(d, e);
	hl = wDefaultText_ADDR;
	ProcessText(&hl);
}
/* <<< factory PrintTotalCardCount */

/* >>> factory RemoveCardFromDeckAndUpdateCount */
RemoveCardFromDeckAndUpdateCountResult RemoveCardFromDeckAndUpdateCount(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	RemoveCardFromDeckResult r = RemoveCardFromDeck(b, c, d, e, hl);
	if (!(r.f & 0x10u)) {
		return (RemoveCardFromDeckAndUpdateCountResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
	}
	PrintCardTypeCounts();
	PrintTotalCardCount(15u, 0u);
	GetCountOfCardInCurDeckResult r2 = GetCountOfCardInCurDeck(r.e);
	PrintNumberValueInCursorYPos(r2.a);
	return (RemoveCardFromDeckAndUpdateCountResult){r2.a, r2.f, r.b, r.c, r2.d, r.e, r.hl};
}
/* <<< factory RemoveCardFromDeckAndUpdateCount */

/* >>> factory PrintCardSelectionList */
void PrintCardSelectionList(void)
{
	uint8_t e = wCardListCoords;
	uint8_t d = gb_read8((uint16_t)(wCardListCoords_ADDR + 1u));
	uint8_t tile;
	if (wCardListVisibleOffset != 0u) {
		tile = SYM_CURSOR_U;
	} else {
		tile = wCursorAlternateTile;
	}
	WriteByteToBGMap0(tile, 19u, e);

	uint8_t offset = wCardListVisibleOffset;
	uint8_t c = offset;
	uint16_t hl = (uint16_t)(wFilteredCardList_ADDR + offset);
	uint8_t count = wNumVisibleCardListEntries;
	while (count != 0u) {
		uint8_t card_id = gb_read8(hl++);
		if (card_id != 0u) {
			uint8_t b = count;
			AddCardIDToVisibleList(b, card_id);
			LoadCardDataToBuffer1_FromCardID(card_id);
			CopyCardNameAndLevelResult name = CopyCardNameAndLevel(14u, b, c, d, card_id);
			AppendOwnedCardCountNumber(name.hl, card_id);
			InitTextPrinting(d, card_id);
			uint16_t text = wDefaultText_ADDR;
			ProcessText(&text);
		} else {
			InitTextPrinting(d, e);
			uint16_t text = Text_9a36;
			ProcessText(&text);
		}
		--count;
		e = (uint8_t)(e + 2u);
	}

	if (gb_read8(hl) != 0u) {
		wUnableToScrollDown = FALSE;
		tile = SYM_CURSOR_D;
	} else {
		wUnableToScrollDown = TRUE;
		tile = wCursorAlternateTile;
	}
	WriteByteToBGMap0(tile, 19u, (uint8_t)(e - 2u));
}
/* <<< factory PrintCardSelectionList */

/* >>> factory PrintFilteredCardSelectionList */
void PrintFilteredCardSelectionList(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t input_a = a;
	uint8_t filter = (input_a < 9u) ? card_type_filters[input_a] : 0xffu;
	CreateCardCollectionListWithDeckCards(ALL_DECKS);
	(void)CreateFilteredCardList(filter, f, 0u, input_a, d, e, wCardListCoords_ADDR);
	gb_write8(wNumVisibleCardListEntries_ADDR, NUM_DECK_CONFIRMATION_VISIBLE_CARDS);
	gb_write8(wCardListCoords_ADDR, 0x05u);
	gb_write8((uint16_t)(wCardListCoords_ADDR + 1u), 0x02u);
	gb_write8(wCursorAlternateTile_ADDR, SYM_SPACE);
	PrintCardSelectionList();
}
/* <<< factory PrintFilteredCardSelectionList */

/* >>> factory PrintDeckBuildingCardList */
void PrintDeckBuildingCardList(void)
{
	uint8_t e = wCardListCoords;
	uint8_t d = gb_read8((uint16_t)(wCardListCoords_ADDR + 1u));
	uint8_t tile = (wCardListVisibleOffset != 0u) ? SYM_CURSOR_U : SYM_SPACE;
	WriteByteToBGMap0(tile, 19u, (uint8_t)(e - 1u));

	uint8_t offset = wCardListVisibleOffset;
	uint16_t hl = (uint16_t)(wFilteredCardList_ADDR + offset);
	uint8_t count = wNumVisibleCardListEntries;
	while (count != 0u) {
		uint8_t b = count;
		uint8_t card_id = gb_read8(hl++);
		if (card_id != 0u) {
			AddCardIDToVisibleList(b, card_id);
			LoadCardDataToBuffer1_FromCardID(card_id);
			CopyCardNameAndLevelResult name = CopyCardNameAndLevel(13u, b, offset, d, card_id);
			AppendOwnedCardCountAndStorageCountNumbers(name.hl, card_id);
			InitTextPrinting(d, e);
			uint16_t text = wDefaultText_ADDR;
			ProcessText(&text);
		} else {
			InitTextPrinting(d, e);
			uint16_t text = Text_9a30;
			ProcessText(&text);
		}
		count = (uint8_t)(count - 1u);
		e = (uint8_t)(e + 2u);
	}

	if (gb_read8(hl) != 0u) {
		wUnableToScrollDown = FALSE;
		tile = SYM_CURSOR_D;
	} else {
		wUnableToScrollDown = TRUE;
		tile = SYM_SPACE;
	}
	WriteByteToBGMap0(tile, 19u, (uint8_t)(e - 2u));
}
/* <<< factory PrintDeckBuildingCardList */

/* >>> factory PrintFilteredCardList */
PrintFilteredCardListResult PrintFilteredCardList(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t saved_a = a;
	uint8_t saved_f = f;
	static const uint8_t card_type_filters[] = {0x00u, 0x01u, 0x02u, 0x03u, 0x04u, 0x05u, 0x06u, 0x07u, FILTER_ENERGY};
	uint8_t filter = (a < 9u) ? card_type_filters[a] : 0xFFu;
	uint16_t src = sCardCollection_ADDR;
	uint16_t dst = wTempCardCollection_ADDR;
	EnableSRAM();
	CopyNBytesFromHLToDE(&src, &dst, (uint8_t)(CARD_COLLECTION_SIZE - 1u));
	DisableSRAM();
	if (gb_read8(wIncludeCardsInDeck_ADDR) != 0u) {
		dst = GetPointerToDeckCards();
		IncrementDeckCardsInTempCollection(dst);
	}
	CreateFilteredCardListResult filtered = CreateFilteredCardList(filter, saved_f, 0u, a, (uint8_t)(dst >> 8), (uint8_t)dst, src);
	a = filtered.a;
	f = filtered.f;
	b = filtered.b;
	c = filtered.c;
	d = filtered.d;
	e = filtered.e;
	hl = filtered.hl;
	gb_write8(wNumVisibleCardListEntries_ADDR, NUM_FILTERED_LIST_VISIBLE_CARDS);
	e = 0x13u;
	d = 0x01u;
	gb_write8(wCardListCoords_ADDR, 0x07u);
	gb_write8((uint16_t)(wCardListCoords_ADDR + 1u), 0x01u);
	hl = 0xCEE1u;
	PrintDeckBuildingCardList();
	return (PrintFilteredCardListResult){saved_a, saved_f, b, c, d, e, hl};
}
/* <<< factory PrintFilteredCardList */

/* >>> factory Func_9ced */
void Func_9ced(void)
{
	uint16_t hl = (uint16_t)(wVisibleListCardIDs_ADDR + wCardListCursorPos);
	uint8_t e = gb_read8(hl);
	/* `ld d, [hl]` reads the next byte, but `lb de, $38, $9f` overwrites d before
	 * anything reads it, so only the card ID in e is live. */
	LoadCardDataToBuffer1_FromCardID(e);
	uint16_t text_hl = SetupText(0x38u, 0x9fu);
	/* `bank1call` selects bank 1 for the callee and restores this routine's bank
	 * on return. OpenCardPage consumes only a and b: a is forced to 0 inside
	 * OpenCardPage_FromHand, and SetupText's counted $C600 clear loop exits with
	 * b at 0, the same value `ld b, $00` put there. */
	uint8_t saved = hBankROM;
	BankswitchROM(F9CED_BANK_DUEL_CORE);
	OpenCardPage_FromHand(0u, 0u, 0u, 0u, 0x38u, 0x9fu, text_hl);
	BankswitchROM(saved);
	wVBlankOAMCopyToggle = F9CED_TRUE;
}
/* <<< factory Func_9ced */

/* >>> factory OpenCardPageFromCardList */
void OpenCardPageFromCardList(void)
{
restart:
	uint16_t list_ptr = (uint16_t)gb_read8(wCurCardListPtr_ADDR);
	list_ptr |= (uint16_t)((uint16_t)gb_read8((uint16_t)(wCurCardListPtr_ADDR + 1u)) << 8);
	uint8_t cursor = gb_read8(wCardListCursorPos_ADDR);
	list_ptr = (uint16_t)(list_ptr + cursor);
	list_ptr = (uint16_t)(list_ptr + gb_read8(wCardListVisibleOffset_ADDR));
	uint8_t card_id = gb_read8(list_ptr);
	LoadCardDataToBuffer1_FromCardID(card_id);
	uint16_t text_hl = SetupText(0x38u, 0x9Fu);
	OpenCardPage_FromCheckHandOrDiscardPile(0u, 0u, 0u, 0u, 0x38u, 0x9Fu, text_hl);

handle_input:
	uint8_t held = gb_read8(hDPadHeld_ADDR);
	uint8_t b = held;
	uint8_t offset;
	if ((held & (PAD_A | PAD_B | PAD_SELECT | PAD_START)) != 0u)
		goto exit;

	gb_write8(wMenuInputSFX_ADDR, FALSE);
	uint8_t count = gb_read8(wCardListNumCursorPositions_ADDR);
	cursor = gb_read8(wCardListCursorPos_ADDR);
	if ((b & (uint8_t)(1u << B_PAD_UP)) != 0u) {
		gb_write8(wMenuInputSFX_ADDR, SFX_CURSOR);
		cursor = (uint8_t)(cursor - 1u);
		if ((cursor & 0x80u) == 0u)
			goto reopen_card_page;
		offset = gb_read8(wCardListVisibleOffset_ADDR);
		if (offset != 0u) {
			offset = (uint8_t)(offset - 1u);
			gb_write8(wCardListVisibleOffset_ADDR, offset);
			cursor = 0u;
			goto reopen_card_page;
		}
		goto handle_regular_card_page_input;
	}
	if ((b & (uint8_t)(1u << B_PAD_DOWN)) != 0u) {
		gb_write8(wMenuInputSFX_ADDR, SFX_CURSOR);
		cursor = (uint8_t)(cursor + 1u);
		if (cursor < count)
			goto reopen_card_page;
		list_ptr = (uint16_t)gb_read8(wCurCardListPtr_ADDR);
		list_ptr |= (uint16_t)((uint16_t)gb_read8((uint16_t)(wCurCardListPtr_ADDR + 1u)) << 8);
		cursor = gb_read8(wCardListCursorPos_ADDR);
		list_ptr = (uint16_t)(list_ptr + cursor);
		offset = (uint8_t)(gb_read8(wCardListVisibleOffset_ADDR) + 1u);
		list_ptr = (uint16_t)(list_ptr + offset);
		if (gb_read8(list_ptr) != 0u) {
			offset = (uint8_t)(gb_read8(wCardListVisibleOffset_ADDR) + 1u);
			gb_write8(wCardListVisibleOffset_ADDR, offset);
			cursor = (uint8_t)(cursor - 1u);
			goto reopen_card_page;
		}
	}

handle_regular_card_page_input:
	OpenCardPage(0u, 0u, 0u, 0u, 0u, card_id, 0u);
	goto handle_input;

reopen_card_page:
	gb_write8(wCardListCursorPos_ADDR, cursor);
	if (gb_read8(wMenuInputSFX_ADDR) == 0u)
		goto restart;
	PlaySFX(gb_read8(wMenuInputSFX_ADDR));
	goto restart;

exit:
	gb_write8(wVBlankOAMCopyToggle_ADDR, TRUE);
	cursor = gb_read8(wCardListCursorPos_ADDR);
	wTempCardListCursorPos = cursor;
}
/* <<< factory OpenCardPageFromCardList */

/* >>> factory CheckIfThereAreAnyBasicCardsInDeck */
CheckIfThereAreAnyBasicCardsInDeckResult CheckIfThereAreAnyBasicCardsInDeck(void)
{
	uint16_t hl = wCurDeckCards_ADDR;
	for (;;) {
		uint8_t card = gb_read8(hl++);
		if (card == 0u)
			return (CheckIfThereAreAnyBasicCardsInDeckResult){0u, 0x80u, 0u, hl};
	LoadCardDataToBuffer1_FromCardID(card);
		if ((uint8_t)(wLoadedCard1Type & TYPE_ENERGY) != 0u)
			continue;
		if (wLoadedCard1Stage != 0u)
			continue;
		return (CheckIfThereAreAnyBasicCardsInDeckResult){0u, 0x90u, card, hl};
	}
}
/* <<< factory CheckIfThereAreAnyBasicCardsInDeck */

/* >>> factory SortCurDeckCardsByID */
SortCurDeckCardsByIDResult SortCurDeckCardsByID(void)
{
	uint16_t src = wCurDeckCards_ADDR;
	uint16_t dst = wOpponentDeck_ADDR;
	uint16_t list = wDuelTempList_ADDR;
	uint8_t index = 0u;

	for (;;) {
		uint8_t card = gb_read8(src++);
		gb_write8(dst++, card);
		if (card == 0u) {
			gb_write8(list, 0xFFu);
			break;
		}
		gb_write8(list++, index++);
	}

	uint8_t saved_turn = hWhoseTurn;
	hWhoseTurn = OPPONENT_TURN;
	(void)SortCardsInDuelTempListByID((uint8_t)(list >> 8), (uint8_t)list, dst);
	hWhoseTurn = saved_turn;

	uint16_t out = wCurDeckCards_ADDR;
	uint16_t order = wDuelTempList_ADDR;
	for (;;) {
		uint8_t entry = gb_read8(order);
		if (entry == 0xFFu)
			break;
		gb_write8(out++, gb_read8((uint16_t)(wOpponentDeck_ADDR + entry)));
		order++;
	}
	gb_write8(out, 0u);
	return (SortCurDeckCardsByIDResult){(uint8_t)order};
}
/* <<< factory SortCurDeckCardsByID */

/* >>> factory GetCardTypeIconPalette */
GetCardTypeIconPaletteResult GetCardTypeIconPalette(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t palette = 0xffu;
	f = 0x80u;
	if (a == 0xe0u) {
		palette = 1u;
		f = 0xc0u;
	} else if (a == 0xe4u) {
		palette = 2u;
		f = 0xc0u;
	} else if (a == 0xe8u) {
		palette = 1u;
		f = 0xc0u;
	} else if (a == 0xecu) {
		palette = 2u;
		f = 0xc0u;
	} else if (a == 0xf0u) {
		palette = 3u;
		f = 0xc0u;
	} else if (a == 0xf4u) {
		palette = 3u;
		f = 0xc0u;
	} else if (a == 0xf8u) {
		palette = 0u;
		f = 0xc0u;
	} else if (a == 0xfcu || a == 0xd0u || a == 0xd4u || a == 0xd8u || a == 0xdcu) {
		palette = (a == 0xd8u) ? 1u : 2u;
		f = 0xc0u;
	}
	return (GetCardTypeIconPaletteResult){palette, f, b, c, d, e, hl};
}
/* <<< factory GetCardTypeIconPalette */

/* >>> factory DrawCardTypeIcons */
void DrawCardTypeIcons(void)
{
	static const uint8_t icons[] = {0xE4u, 0xE0u, 0xECu, 0xE8u, 0xF0u, 0xF4u, 0xF8u, 0xDCu, 0xFCu, 0x00u};
	static const uint8_t xs[] = {1u, 3u, 5u, 7u, 9u, 11u, 13u, 15u, 17u};
	for (uint8_t i = 0u; icons[i] != 0u; i++) {
		uint8_t tile = icons[i];
		uint8_t x = xs[i];
		uint16_t de = (uint16_t)(((uint16_t)x << 8) | 2u);
		FillRectangle(tile, 2u, 2u, de, 0x0102u);
		GetCardTypeIconPaletteResult palette = GetCardTypeIconPalette(tile, 0u, 0u, 0u, 0u, 0u, 0u);
		if (wConsole == 0x02u) {
			hBankVRAM = 1u;
			gb_write8(0xFF4Fu, 1u);
			FillRectangle(palette.a, 2u, 2u, de, 0x0000u);
			hBankVRAM = 0u;
			gb_write8(0xFF4Fu, 0u);
		}
	}
}
/* <<< factory DrawCardTypeIcons */

/* >>> factory PrintPlayersCardsHeaderInfo */
void PrintPlayersCardsHeaderInfo(void)
{
	Set_OBJ_8x8();
	PrepareMenuGraphics();
	FillBGMapLineWithA(0x1Cu, 0u, 4u);
	PrintTotalNumberOfCardsInCollection();
	PrintPlayersCardsText();
	DrawCardTypeIcons();
}
/* <<< factory PrintPlayersCardsHeaderInfo */

/* >>> factory PrintConfirmationCardList */
void PrintConfirmationCardList(uint8_t a, uint8_t d, uint8_t e, uint16_t *hl)
{
	uint8_t x = wCardListCoords;
	uint8_t y = gb_read8((uint16_t)(wCardListCoords_ADDR + 1u));
	uint8_t tile = wCardListVisibleOffset ? SYM_CURSOR_U : SYM_SPACE;
	WriteByteToBGMap0(tile, 19u, (uint8_t)(x - 1u));
	uint8_t offset = wCardListVisibleOffset;
	uint16_t list = (uint16_t)(wOwnedCardsCountList_ADDR + offset);
	uint8_t remaining = wNumVisibleCardListEntries;
	while (remaining != 0u) {
		uint8_t card = gb_read8(list++);
		if (card == 0u) break;
		uint8_t row = remaining;
		AddCardIDToVisibleList(row, card);
		LoadCardDataToBuffer1_FromCardID(card);
		CopyCardNameAndLevelResult name = CopyCardNameAndLevel(13u, row, 0u, 0u, card);
		uint16_t text = name.hl;
		while (gb_read8(text) != 0u) text++;
		GetCountOfCardInCurDeckResult count = GetCountOfCardInCurDeck(card);
		gb_write8(text++, TX_SYMBOL);
		gb_write8(text++, SYM_CROSS);
		ConvertToNumericalDigitsResult digits = ConvertToNumericalDigits(count.d, text);
		gb_write8(digits.hl, TX_END);
		uint8_t icon;
		if (wLoadedCard1Type < TYPE_ENERGY) icon = (uint8_t)(ICON_TILE_BASIC_POKEMON + (uint8_t)(wLoadedCard1Stage * 4u));
		else if (wLoadedCard1Type < TYPE_TRAINER) icon = (uint8_t)(ICON_TILE_FIRE + (uint8_t)((wLoadedCard1Type - TYPE_ENERGY) * 4u));
		else icon = ICON_TILE_TRAINER;
		uint16_t de = (uint16_t)((uint16_t)(y - 1u) << 8 | (uint8_t)(x - 2u));
		FillRectangle(icon, 2u, 2u, de, 0x0102u);
		GetCardTypeIconPaletteResult palette = GetCardTypeIconPalette(icon, 0u, 0u, 0u, 0u, 0u, de);
		if (wConsole == CONSOLE_CGB) { gb_write8(0xFF4Fu, 1u); FillRectangle(palette.a, 2u, 2u, de, 0x0102u); gb_write8(0xFF4Fu, 0u); }
		InitTextPrinting(0u, (uint8_t)(y + 2u));
		uint16_t text_ptr = wDefaultText_ADDR;
		ProcessText(&text_ptr);
		remaining = (uint8_t)(row - 1u);
		x = (uint8_t)(x + 2u);
	}
	if (gb_read8(list) == 0u) {
		/* PrintConfirmationCardList: set scroll guard */
		wUnableToScrollDown = 1u;
		tile = SYM_SPACE;
	} else {
		/* PrintConfirmationCardList: clear scroll guard */
		wUnableToScrollDown = 0u;
		tile = SYM_CURSOR_D;
	}
	WriteByteToBGMap0(tile, 19u, (uint8_t)(y - 2u));
	(void)a; (void)d; (void)e; (void)hl;
}
/* <<< factory PrintConfirmationCardList */

/* >>> factory CreateCurDeckUniqueCardList */
CreateCurDeckUniqueCardListResult CreateCurDeckUniqueCardList(void)
{
	uint8_t count = 0u;
	uint8_t previous = 0u;
	uint16_t hl = wCurDeckCards_ADDR;
	uint16_t de = wUniqueDeckCardList_ADDR;
	for (;;) {
		uint8_t card = gb_read8(hl++);
		if (card == previous)
			continue;
		previous = card;
		gb_write8(de++, card);
		if (card == 0u)
			break;
		++count;
	}
	wNumUniqueCards = count;
	return (CreateCurDeckUniqueCardListResult){count, 0x80u, count, previous, (uint8_t)(de >> 8), (uint8_t)de, hl};
}
/* <<< factory CreateCurDeckUniqueCardList */

/* >>> factory TryAddCardToDeck */
TryAddCardToDeckResult TryAddCardToDeck(uint8_t e)
{
	uint8_t d = wMaxNumCardsAllowed;
	if (wTotalCardCount == d)
		return (TryAddCardToDeckResult){0u, 0x90u};

	LoadCardDataToBuffer1_FromCardID(e);
	if (wLoadedCard1Type != TYPE_ENERGY_DOUBLE_COLORLESS &&
	    (wLoadedCard1Type & TYPE_ENERGY) != TYPE_ENERGY) {
		uint16_t name = (uint16_t)(wLoadedCard1Name |
			(uint16_t)wLoadedCard1Name_PTR[1] << 8);
		uint8_t same = 0u;
		uint8_t *cards = wCurDeckCards_PTR;
		while (*cards != 0u) {
			uint16_t card_name = GetCardName(*cards);
			if (card_name == name && ++same == wSameNameCardsLimit)
				return (TryAddCardToDeckResult){0u, (uint8_t)0x10u};
			++cards;
		}
	}

	GetCountOfCardInCurDeckResult count = GetCountOfCardInCurDeck(e);
	uint8_t *owned = wOwnedCardsCountList_PTR + wCardListVisibleOffset + wCardListCursorPos;
	if (count.a == *owned)
		return (TryAddCardToDeckResult){count.a, 0x40u};

	PlaySFX(SFX_CURSOR);
	uint8_t *slot = wCurDeckCards_PTR;
	while (*slot != 0u)
		++slot;
	*slot++ = e;
	*slot = 0u;
	++(wCardFilterCounts_PTR[wCurCardTypeFilter]);
	return (TryAddCardToDeckResult){0u, 0u};
}
/* <<< factory TryAddCardToDeck */

/* >>> factory AddCardToDeckAndUpdateCount */
AddCardToDeckAndUpdateCountResult AddCardToDeckAndUpdateCount(uint8_t e)
{
	TryAddCardToDeckResult r = TryAddCardToDeck(e);
	if (r.f & 0x10u)
		return (AddCardToDeckAndUpdateCountResult){r.a, r.f, e};
	PrintCardTypeCounts();
	PrintTotalCardCount(15u, 0u);
	GetCountOfCardInCurDeckResult r2 = GetCountOfCardInCurDeck(e);
	PrintNumberValueInCursorYPos(r2.a);
	return (AddCardToDeckAndUpdateCountResult){r2.a, r2.f, e};
}
/* <<< factory AddCardToDeckAndUpdateCount */

/* >>> factory HandleDeckCardSelectionList */
HandleDeckCardSelectionListResult HandleDeckCardSelectionList(void)
{
	wMenuInputSFX = FALSE;
	uint8_t dpad = hDPadHeld;
	uint8_t cursor = wCardListCursorPos;
	uint8_t a = cursor;
	HandleDeckCardSelectionListResult out = {0u, 0u, 0u, 0u, 0u, 0u, 0u};
	if (dpad != 0u) {
		uint8_t count = wCardListNumCursorPositions;
		if ((dpad & (1u << B_PAD_UP)) != 0u) {
			wMenuInputSFX = SFX_CURSOR; a = (uint8_t)(cursor - 1u);
			if ((a & 0x80u) != 0u && wCardListVisibleOffset != 0u) { --wCardListVisibleOffset; a = 0u; }
		} else if ((dpad & (1u << B_PAD_DOWN)) != 0u) {
			wMenuInputSFX = SFX_CURSOR; a = (uint8_t)(cursor + 1u);
			if (a >= count) { if (wUnableToScrollDown == 0u) { ++wCardListVisibleOffset; --a; } else { --a; wMenuInputSFX = FALSE; } }
		}
		(void)DrawListCursor_Invisible(); wCardListCursorPos = a; wCheckMenuCursorBlinkCounter = 0u;
	} else if (wced2 != 0u) {
		if ((dpad & (1u << B_PAD_LEFT)) != 0u) {
			uint8_t e = GetSelectedVisibleCardID(); RemoveCardFromDeckAndUpdateCount(out.b, out.c, out.d, e, out.hl);
		} else if ((dpad & (1u << B_PAD_RIGHT)) != 0u) {
			AddCardToDeckAndUpdateCount(GetSelectedVisibleCardID());
		}
	}
	hffb3 = wCardListCursorPos;
	if (wCardListHandlerFunction != 0u) {
		DrawListCursor_Visible(); PlaySFXConfirmOrCancel(MENU_CONFIRM); out.a = MENU_CONFIRM; out.f = 0x10u; out.e = wCardListCursorPos; return out;
	}
	uint8_t keys = hKeysPressed;
	if ((keys & (PAD_A | PAD_B)) != 0u) {
		if ((keys & PAD_A) != 0u) { DrawListCursor_Visible(); PlaySFXConfirmOrCancel(MENU_CONFIRM); out.a = MENU_CONFIRM; out.f = 0x10u; out.e = wCardListCursorPos; return out; }
		hffb3 = MENU_CANCEL; PlaySFXConfirmOrCancel(MENU_CANCEL); out.a = MENU_CANCEL; out.f = 0x10u; return out;
	}
	if (wMenuInputSFX != 0u) PlaySFX(wMenuInputSFX);
	uint8_t counter = (uint8_t)(wCheckMenuCursorBlinkCounter + 1u); wCheckMenuCursorBlinkCounter = counter;
	if ((counter & CURSOR_BLINK_PERIOD_MASK) == 0u) { if ((counter & (1u << B_CURSOR_BLINK_PERIOD)) == 0u) DrawListCursor(wVisibleCursorTile); else DrawListCursor_Invisible(); }
	return out;
}
/* <<< factory HandleDeckCardSelectionList */

/* >>> factory PrintCurDeckNumberAndName */
void PrintCurDeckNumberAndName(void)
{
	uint8_t current_deck = wCurDeck;
	if (current_deck != 0xFFu) {
		InitTextPrinting(3u, 2u);
		uint8_t deck_numeral = current_deck;
		if (deck_numeral & 0x80u)
			deck_numeral = (uint8_t)(deck_numeral & 0x7Fu);
		else
			deck_numeral = (uint8_t)(deck_numeral + 1u);
		ConvertToNumericalDigitsResult digits =
			ConvertToNumericalDigits(deck_numeral, wDefaultText_ADDR);
		gb_write8(digits.hl, PRINT_CUR_DECK_MIDDLE_DOT);
		gb_write8((uint16_t)(digits.hl + 1u), 0u);
		uint16_t numeral_text = wDefaultText_ADDR;
		ProcessText(&numeral_text);
	}

	uint16_t name_src = wCurDeckName_ADDR;
	uint16_t name_dst = wDefaultText_ADDR;
	CopyListFromHLToDE(&name_src, &name_dst);

	if (wCurDeck == 0xFFu) {
		InitTextPrinting(2u, 2u);
		uint16_t blank_text = wDefaultText_ADDR;
		ProcessText(&blank_text);
		return;
	}

	TextLength name_length = GetTextLengthInTiles(wDefaultText_ADDR);
	uint16_t suffix_base = wDefaultText_ADDR;
	uint16_t suffix_destination = (uint16_t)(suffix_base + name_length.c);
	uint16_t suffix_source = PRINT_CUR_DECK_NAME_SUFFIX_ADDR;
	CopyListFromHLToDE(&suffix_source, &suffix_destination);
	InitTextPrinting(6u, 2u);
	uint16_t name_text = wDefaultText_ADDR;
	ProcessText(&name_text);
}
/* <<< factory PrintCurDeckNumberAndName */

/* >>> factory UpdateConfirmationCardScreen */
void UpdateConfirmationCardScreen(void)
{
	hffb0 = 1u;
	PrintCurDeckNumberAndName();

	hffb0 = 0u;
	PrintConfirmationCardList(0u, 0u, 0u, (uint16_t *)0);
}
/* <<< factory UpdateConfirmationCardScreen */

/* >>> factory PrintSlashSixty */
/* deck_configuration.asm:1017-1035. Builds the TX_SYMBOL encoding for "/60",
 * then prints it at the caller-supplied d/e coordinates. */
void PrintSlashSixty(uint8_t d, uint8_t e)
{
	uint16_t text = wDefaultText_ADDR;
	gb_write8(text++, TX_SYMBOL);
	gb_write8(text++, SYM_SLASH);
	gb_write8(text++, TX_SYMBOL);
	gb_write8(text++, (uint8_t)(SYM_0 + 6u));
	gb_write8(text++, TX_SYMBOL);
	gb_write8(text++, SYM_0);
	gb_write8(text, TX_END);
	InitTextPrinting(d, e);
	text = wDefaultText_ADDR;
	ProcessText(&text);
}
/* <<< factory PrintSlashSixty */

/* >>> factory ShowDeckInfoHeader */
void ShowDeckInfoHeader(void)
{
	EmptyScreenAndLoadFontDuelAndHandCardsIcons();
	uint16_t box = 0u;
	DrawRegularTextBox(&box, 0u, 20u, 4u, 0u, 0u);
	if (wCurDeckName != 0u) {
		PrintCurDeckNumberAndName();
		uint8_t current_deck = wCurDeck;
		EnableSRAM();
		uint8_t selected_deck = sCurrentlySelectedDeck;
		DisableSRAM();
		if (selected_deck == current_deck)
			DrawHandCardsTileAtDE(0x0201u);
	}
	PrintTotalCardCount(14u, 1u);
	PrintSlashSixty(16u, 1u);
	(void)TallyCardsInCardFilterLists(16u, 1u);
	EnableLCD();
}
/* <<< factory ShowDeckInfoHeader */

/* >>> factory DrawCardTypeIconsAndPrintCardCounts */
void DrawCardTypeIconsAndPrintCardCounts(void)
{
	Set_OBJ_8x8();
	PrepareMenuGraphics();
	FillBGMapLineWithA(SYM_BOX_TOP, 0u, 5u);
	DrawCardTypeIcons();
	PrintCardTypeCounts();
	PrintTotalCardCount(15u, 0u);
	PrintSlashSixty(17u, 0u);
	EnableLCD();
}
/* <<< factory DrawCardTypeIconsAndPrintCardCounts */

/* >>> factory ShowConfirmationCardScreen */
void ShowConfirmationCardScreen(void)
{
	ShowDeckInfoHeader();
	wCardListCoords = 5u;
	gb_write8((uint16_t)(wCardListCoords_ADDR + 1u), 3u);
	PrintConfirmationCardList(0u, 3u, 5u, (uint16_t *)0);
}
/* <<< factory ShowConfirmationCardScreen */

/* >>> factory ShowDeckInfoHeaderAndWaitForBButton */
void ShowDeckInfoHeaderAndWaitForBButton(void)
{
	ShowDeckInfoHeader();
	for (;;) {
		DoFrame();
		if ((hKeysPressed & 0x02u) != 0u)
			break;
	}
	PlaySFXConfirmOrCancel(MENU_CANCEL);
}
/* <<< factory ShowDeckInfoHeaderAndWaitForBButton */

/* >>> factory HandleDeckConfirmationMenu */
/* deck_configuration.asm:2364-2438. The opening `jp z,
 * ShowDeckInfoHeaderAndWaitForBButton` is a tail call: its `ret` returns
 * straight to this routine's caller, so the port calls it and returns behind
 * it. That exit leaves the callee's registers while the cancel `ret z` in
 * .selection_made leaves a = [hffb3] = MENU_CANCEL and f = $C0; the two
 * disagree, so the contract observes no registers.
 *
 * The `jr .init_params` from .selected_card re-enters past the `xor a`, so
 * InitCardSelectionParams takes the a OpenCardPageFromCardList's .exit
 * leaves, [wCardListCursorPos] (deck_configuration.asm:2084-2089) -- the
 * same handoff HandleDeckMissingCardsList records. UpdateConfirmationCard
 * Screen is only parked in wCardListUpdateFunction for CallIndirect, which
 * this tree does not dispatch (see the note on HandleLeftRightInCardList);
 * the two bytes stored are the real bank-2 address, so the WRAM still
 * matches the reference. */
void HandleDeckConfirmationMenu(void)
{
	if (wTotalCardCount == 0u) { /* if deck is empty, just show deck info header with empty card list */
		ShowDeckInfoHeaderAndWaitForBButton();
		return;
	}

	/* create list of all unique cards */
	(void)SortCurDeckCardsByID();
	(void)CreateCurDeckUniqueCardList();

	wCardListVisibleOffset = 0u;
	uint8_t cursor = 0u; /* the `xor a` before .init_params */

	for (;;) { /* .init_params */
		uint16_t params = DECK_CONFIRMATION_MENU_CARD_SELECTION_PARAMS_ADDR;

		(void)InitCardSelectionParams(cursor, &params);

		uint8_t entries = wNumUniqueCards;

		wNumCardListEntries = entries;
		if (entries >= NUM_DECK_CONFIRMATION_VISIBLE_CARDS) /* jr c, .no_cap */
			entries = NUM_DECK_CONFIRMATION_VISIBLE_CARDS;
		wCardListNumCursorPositions = entries;
		wNumVisibleCardListEntries = entries;

		ShowConfirmationCardScreen();

		gb_write8(wCardListUpdateFunction_ADDR, (uint8_t)UPDATE_CONFIRMATION_CARD_SCREEN_ADDR);
		gb_write8((uint16_t)(wCardListUpdateFunction_ADDR + 1u),
			  (uint8_t)(UPDATE_CONFIRMATION_CARD_SCREEN_ADDR >> 8));

		wced2 = 0u;

		for (;;) { /* .loop_input */
			DoFrame();
			HandleDeckCardSelectionListResult selection = HandleDeckCardSelectionList();
			if (selection.f & 0x10u) { /* .selection_made */
				uint8_t selected = hffb3;

				if (selected == MENU_CANCEL)
					return; /* operation cancelled */
				break;
			}
			if ((HandleLeftRightInCardList().f & 0x10u) != 0u)
				continue;
			if ((hDPadHeld & PAD_START) == 0u)
				continue;
			break; /* .selected_card */
		}

		PlaySFXConfirmOrCancel(MENU_CONFIRM);
		wced7 = wCardListCursorPos;

		/* set wUniqueDeckCardList as current card list
		 * and show card page screen */
		gb_write8(wCurCardListPtr_ADDR, (uint8_t)wUniqueDeckCardList_ADDR);
		gb_write8((uint16_t)(wCurCardListPtr_ADDR + 1u),
			  (uint8_t)(wUniqueDeckCardList_ADDR >> 8));
		OpenCardPageFromCardList();
		cursor = wCardListCursorPos; /* jr .init_params */
	}
}
/* <<< factory HandleDeckConfirmationMenu */

/* >>> factory ConfirmDeckConfiguration */
void ConfirmDeckConfiguration(void)
{
	uint8_t visible_offset = wCardListVisibleOffset;
	wCardListVisibleOffsetBackup = visible_offset;
	HandleDeckConfirmationMenu();
	wCardListVisibleOffset = wCardListVisibleOffsetBackup;
	DrawCardTypeIconsAndPrintCardCounts();
	uint16_t params = FILTERS_CARD_SELECTION_PARAMS_ADDR;
	(void)InitCardSelectionParams(0u, &params);
	wTempCardTypeFilter = wCurCardTypeFilter;
	(void)DrawHorizontalListCursor_Visible();
	(void)PrintFilteredCardList(wCurCardTypeFilter, 0u, 0u, 0u, 0u, 0u, FILTERS_CARD_SELECTION_PARAMS_ADDR);
	wCardListCursorPos = wced6;
}
/* <<< factory ConfirmDeckConfiguration */

/* >>> factory SaveDeckConfiguration */
/* deck_configuration.asm:642 */
SaveDeckConfigurationResult SaveDeckConfiguration(uint16_t w0)
{
	/* Entered through JumpToFunctionInTable, so the word at sp is the return
	 * address back into HandleDeckConfigurationMenu. The two `add sp, $2`
	 * exits drop it to return one frame further out; the value is never read. */
	(void)w0;
	if (wTotalCardCount != DECK_SIZE) {
		(void)DrawWideTextBox_WaitForInput(ThisIsntA60CardDeckText);
		HandleYesOrNoMenuResult keep =
			YesOrNoMenuWithText(ReturnToOriginalConfigurationText);
		if ((keep.f & 0x10u) == 0u) {
			/* add sp, $2 / or a / ret */
			uint8_t or_a = keep.a;
			return (SaveDeckConfigurationResult){
				or_a, (uint8_t)(or_a == 0u ? 0x80u : 0x00u)};
		}
		(void)DrawWideTextBox_WaitForInput(TheDeckMustInclude60CardsText);
	} else {
		HandleYesOrNoMenuResult save = YesOrNoMenuWithText(SaveThisDeckText);
		if ((save.f & 0x10u) == 0u) {
			CheckIfThereAreAnyBasicCardsInDeckResult basic =
				CheckIfThereAreAnyBasicCardsInDeck();
			if ((basic.f & 0x10u) != 0u) {
				/* add sp, $2 / scf / ret: scf keeps Z, clears N and H */
				return (SaveDeckConfigurationResult){
					basic.a, (uint8_t)((basic.f & 0x80u) | 0x10u)};
			}
			(void)DrawWideTextBox_WaitForInput(ThereAreNoBasicPokemonInThisDeckText);
			(void)DrawWideTextBox_WaitForInput(YouMustIncludeABasicPokemonInTheDeckText);
		}
	}
	/* .go_back leaves with a plain `ret`, one frame out. Its flags are whatever
	 * PrintDeckBuildingCardList left behind, which that routine's ported void
	 * signature does not carry; every caller of this label falls straight into
	 * OpenDeckConfigurationMenu.skip_init without testing them. */
	DrawCardTypeIconsAndPrintCardCounts();
	PrintDeckBuildingCardList();
	uint8_t cursor = wced6;
	wCardListCursorPos = cursor;
	return (SaveDeckConfigurationResult){cursor, 0u};
}
/* <<< factory SaveDeckConfiguration */

/* >>> factory DismantleDeck */
/* deck_configuration.asm:684-716 */
uint8_t DismantleDeck(uint16_t w0)
{
	/* Entered through JumpToFunctionInTable, so the word at sp is the return
	 * address back into HandleDeckConfigurationMenu; the `add sp, $2` on the
	 * .Dismantle exit discards it to return one frame further out and never
	 * reads it. Only `a` is modelled: that exit leaves the flags produced by
	 * `add sp, $2`, which depend on the runtime sp. */
	(void)w0;

	HandleYesOrNoMenuResult confirm = YesOrNoMenuWithText(DismantleThisDeckText);
	if ((confirm.f & 0x10u) != 0u) {
		/* jr c, SaveDeckConfiguration.go_back */
		DrawCardTypeIconsAndPrintCardCounts();
		PrintDeckBuildingCardList();
		uint8_t back = wced6;
		wCardListCursorPos = back;
		return back;
	}

	if ((CheckIfHasOtherValidDecks() & 0x10u) != 0u) {
		/* carry: this is the only deck with cards, so it cannot be dismantled */
		(void)DrawWideTextBox_WaitForInput(ThereIsOnly1DeckSoCannotBeDismantledText);
		EmptyScreen();
		uint16_t params = FILTERS_CARD_SELECTION_PARAMS_ADDR;
		(void)InitCardSelectionParams(0u, &params);
		/* wTempCardTypeFilter and wCardListCursorPos are the same byte ($CEA4);
		 * the filter store happens first, exactly as in the asm. */
		wTempCardTypeFilter = wCurCardTypeFilter;
		(void)DrawHorizontalListCursor_Visible();
		PrintDeckBuildingCardList();
		EnableLCD();
		uint8_t cursor = wced6;
		wCardListCursorPos = cursor;
		return cursor;
	}

	/* .Dismantle */
	EnableSRAM();
	uint16_t name = GetPointerToDeckName();
	uint8_t a = gb_read8(name);
	if (a != 0u) {
		ClearMemory_Bank2(NAME_BUFFER_LENGTH, name);
		uint16_t cards = GetPointerToDeckCards();
		(void)AddDeckToCollection(cards);
		a = DECK_SIZE;
		ClearMemory_Bank2(DECK_SIZE, cards);
	}
	DisableSRAM();
	return a;
}
/* <<< factory DismantleDeck */

/* >>> factory CancelDeckModifications */
/* deck_configuration.asm:629-640 */
CancelDeckModificationsResult CancelDeckModifications(uint16_t w0)
{
	/* Reached through HandleDeckConfigurationMenu's JumpToFunctionInTable, so
	 * the word at sp is that menu's own return address. The `add sp, $2` exit
	 * drops it to return one frame further out; the value is never read, just
	 * as the landed SaveDeckConfiguration models its own w0. */
	(void)w0;

	CheckIfCurrentDeckWasChangedResult changed = CheckIfCurrentDeckWasChanged();
	uint8_t a = changed.a;

	if ((changed.f & 0x10u) != 0u) { /* deck was changed: prompt the player */
		HandleYesOrNoMenuResult quit = YesOrNoMenuWithText(QuitModifyingTheDeckText);
		if ((quit.f & 0x10u) != 0u) {
			/* jr c, SaveDeckConfiguration.go_back. That label is interior to
			 * the sibling routine and has no entry of its own, so its body is
			 * repeated here. It leaves with a plain `ret`, one frame in, and
			 * its flags are whatever PrintDeckBuildingCardList left behind,
			 * which that routine's ported void signature does not carry. */
			DrawCardTypeIconsAndPrintCardCounts();
			PrintDeckBuildingCardList();
			uint8_t cursor = wced6;
			wCardListCursorPos = cursor;
			return (CancelDeckModificationsResult){cursor, 0u};
		}
		a = quit.a;
	}

	/* .cancel_modification: add sp, $2 / or a / ret */
	return (CancelDeckModificationsResult){a, (uint8_t)(a == 0u ? 0x80u : 0x00u)};
}
/* <<< factory CancelDeckModifications */

/* >>> factory HandleSelectUpAndDownInList */
HandleSelectUpAndDownInListResult HandleSelectUpAndDownInList(void)
{
	uint8_t positions = wCardListNumCursorPositions;
	uint8_t old_offset = wCardListVisibleOffset;
	uint8_t held = hDPadHeld;

	if (held != (uint8_t)(PAD_SELECT | PAD_DOWN) &&
		held != (uint8_t)(PAD_SELECT | PAD_UP)) {
		return (HandleSelectUpAndDownInListResult){
			(uint8_t)(held == 0u ? 0x80u : 0u)
		};
	}

	uint8_t next;
	if (held == (uint8_t)(PAD_SELECT | PAD_DOWN)) {
		uint8_t candidate = (uint8_t)(old_offset + positions);
		uint8_t doubled = (uint8_t)(candidate + positions);
		if (doubled < wNumCardListEntries) {
			next = candidate;
		} else {
			next = (uint8_t)(wNumCardListEntries - positions);
		}
	} else {
		if (old_offset >= positions)
			next = (uint8_t)(old_offset - positions);
		else
			next = 0u;
	}

	wCardListVisibleOffset = next;
	if (next == old_offset)
		return (HandleSelectUpAndDownInListResult){0x90u};

	PlaySFX(SFX_CURSOR);
	uint16_t update_addr = (uint16_t)gb_read8(wCardListUpdateFunction_ADDR);
	update_addr = (uint16_t)(update_addr |
		((uint16_t)gb_read8((uint16_t)(wCardListUpdateFunction_ADDR + 1u)) << 8));
	if (update_addr == HANDLE_SELECT_PRINT_DECK_BUILDING_ADDR) {
		PrintDeckBuildingCardList();
	} else if (update_addr == HANDLE_SELECT_UPDATE_CONFIRM_ADDR) {
		UpdateConfirmationCardScreen();
	} else if (update_addr == HANDLE_SELECT_PRINT_CARD_ADDR) {
		PrintCardSelectionList();
	}
	return (HandleSelectUpAndDownInListResult){0x10u};
}
/* <<< factory HandleSelectUpAndDownInList */

/* >>> factory HandleDeckBuildScreen */
void HandleDeckBuildScreen(void)
{
	(void)WriteCardListsTerminatorBytes();
	CountNumberOfCardsForEachCardType();
	DrawCardTypeIconsAndPrintCardCounts();

	wCardListVisibleOffset = 0u;
	wCurCardTypeFilter = 0u;
	(void)PrintFilteredCardList(0u, 0u, 0u, 0u, 0u, 0u,
		HANDLE_DECK_BUILD_FILTERS_PARAMS_ADDR);

	uint16_t params;
	params = HANDLE_DECK_BUILD_FILTERS_PARAMS_ADDR;
	(void)InitCardSelectionParams(0u, &params);

	for (;;) {
		DoFrame();
		if ((hDPadHeld & PAD_START) != 0u) {
			PlaySFXConfirmOrCancel(MENU_CONFIRM);
			ConfirmDeckConfiguration();
			wTempCardTypeFilter = wCurCardTypeFilter;
			continue;
		}

		uint8_t current_filter = wCurCardTypeFilter;
		uint8_t temporary_filter = wTempCardTypeFilter;
		if (temporary_filter != current_filter) {
			wCurCardTypeFilter = temporary_filter;
			wCardListVisibleOffset = 0u;
			(void)PrintFilteredCardList(wCurCardTypeFilter, 0u, 0u, 0u, 0u, 0u,
				HANDLE_DECK_BUILD_FILTERS_PARAMS_ADDR);
			wCardListNumCursorPositions = NUM_FILTERS;
		}

		uint8_t jump_to_list = 0u;
		if ((hDPadHeld & PAD_DOWN) != 0u) {
			(void)ConfirmSelectionAndReturnCarry();
			jump_to_list = 1u;
		} else {
			HandleCardSelectionInputResult input = HandleCardSelectionInput();
			if (input.carry == 0u)
				continue;
			if (hffb3 == MENU_CANCEL) {
				OpenDeckConfigurationMenu();
				return;
			}
			jump_to_list = 1u;
		}

		if (jump_to_list == 0u || wNumEntriesInCurFilter == 0u)
			continue;

		uint8_t list_cursor = 0u;
		uint8_t back_to_filter = 0u;
		for (;;) {
			params = HANDLE_DECK_BUILD_FILTERED_PARAMS_ADDR;
			(void)InitCardSelectionParams(list_cursor, &params);
			uint8_t entries = wNumEntriesInCurFilter;
			wNumCardListEntries = entries;
			if (entries < wNumVisibleCardListEntries)
				wCardListNumCursorPositions = entries;

			wCardListUpdateFunction = (uint8_t)HANDLE_SELECT_PRINT_DECK_BUILDING_ADDR;
			gb_write8((uint16_t)(wCardListUpdateFunction_ADDR + 1u),
				(uint8_t)(HANDLE_SELECT_PRINT_DECK_BUILDING_ADDR >> 8));
			wced2 = 1u;

			uint8_t restart_list = 0u;
			for (;;) {
				DoFrame();
				if ((hDPadHeld & PAD_START) != 0u) {
					PlaySFXConfirmOrCancel(MENU_CONFIRM);
					wTempFilteredCardListNumCursorPositions = wCardListCursorPos;
					ConfirmDeckConfiguration();
					list_cursor = wTempFilteredCardListNumCursorPositions;
					restart_list = 1u;
					break;
				}

				HandleSelectUpAndDownInListResult page = HandleSelectUpAndDownInList();
				if ((page.f & 0x10u) != 0u)
					continue;

				HandleDeckCardSelectionListResult selection = HandleDeckCardSelectionList();
				if ((selection.f & 0x10u) == 0u)
					continue;

				(void)DrawListCursor_Invisible();
				wTempCardListCursorPos = wCardListCursorPos;
				if (hffb3 == MENU_CANCEL) {
					params = HANDLE_DECK_BUILD_FILTERS_PARAMS_ADDR;
					(void)InitCardSelectionParams(MENU_CANCEL, &params);
					wTempCardTypeFilter = wCurCardTypeFilter;
					back_to_filter = 1u;
					break;
				}

				PlaySFXConfirmOrCancel(MENU_CONFIRM);
				wTempCardListNumCursorPositions = wCardListNumCursorPositions;
				wTempCardListCursorPos = wCardListCursorPos;
				gb_write8(wCurCardListPtr_ADDR, (uint8_t)wFilteredCardList_ADDR);
				gb_write8((uint16_t)(wCurCardListPtr_ADDR + 1u),
					(uint8_t)(wFilteredCardList_ADDR >> 8));
				OpenCardPageFromCardList();
				DrawCardTypeIconsAndPrintCardCounts();

				params = HANDLE_DECK_BUILD_FILTERS_PARAMS_ADDR;
				(void)InitCardSelectionParams(0u, &params);
				wTempCardTypeFilter = wCurCardTypeFilter;
				(void)DrawHorizontalListCursor_Visible();
				PrintDeckBuildingCardList();
				params = HANDLE_DECK_BUILD_FILTERED_PARAMS_ADDR;
				(void)InitCardSelectionParams(0u, &params);
				wCardListNumCursorPositions = wTempCardListNumCursorPositions;
				list_cursor = wTempCardListCursorPos;
				wCardListCursorPos = list_cursor;
			}

			if (back_to_filter != 0u)
				break;
			if (restart_list != 0u)
				continue;
		}
	}
}
/* <<< factory HandleDeckBuildScreen */

/* >>> factory HandlePlayersCardsScreen */
void HandlePlayersCardsScreen(void)
{
	(void)WriteCardListsTerminatorBytes();
	(void)PrintPlayersCardsHeaderInfo();

	wCardListVisibleOffset = 0u;
	wCurCardTypeFilter = 0u;
	PrintFilteredCardSelectionList(0u, 0x80u, 0u, 0u, 0u, 0u, wCardListCoords_ADDR);
	EnableLCD();

	uint16_t filter_params = FILTERS_CARD_SELECTION_PARAMS_ADDR;
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

		uint16_t list_params = HANDLE_PLAYERS_CARDS_DATA_ADDR;
		(void)InitCardSelectionParams(0u, &list_params);
		uint8_t entries = wNumEntriesInCurFilter;
		wNumCardListEntries = entries;
		if (entries < wNumVisibleCardListEntries)
			wCardListNumCursorPositions = entries;
		gb_write8(wCardListUpdateFunction_ADDR, (uint8_t)HANDLE_PLAYERS_CARDS_PRINT_LIST_ADDR);
		gb_write8((uint16_t)(wCardListUpdateFunction_ADDR + 1u),
			  (uint8_t)(HANDLE_PLAYERS_CARDS_PRINT_LIST_ADDR >> 8));
		wced2 = 0u;

		uint8_t return_to_filter = 0u;
		for (;;) {
			DoFrame();
			HandleSelectUpAndDownInListResult move = HandleSelectUpAndDownInList();
			if ((move.f & 0x10u) != 0u)
				continue;
			HandleDeckCardSelectionListResult selection = HandleDeckCardSelectionList();
			if ((selection.f & 0x10u) != 0u) {
				(void)DrawListCursor_Invisible();
				wTempCardListCursorPos = wCardListCursorPos;
				if (hffb3 == MENU_CANCEL) {
					uint16_t params = FILTERS_CARD_SELECTION_PARAMS_ADDR;
					(void)InitCardSelectionParams(hffb3, &params);
					wTempCardTypeFilter = wCurCardTypeFilter;
					hffb0 = 1u;
					PrintPlayersCardsText();
					hffb0 = 0u;
					return_to_filter = 1u;
					break;
				}
			}
			else if ((hDPadHeld & PAD_START) == 0u) {
				continue;
			}

			PlaySFXConfirmOrCancel(MENU_CONFIRM);
			wTempCardListNumCursorPositions = wCardListNumCursorPositions;
			wTempCardListCursorPos = wCardListCursorPos;
			gb_write8(wCurCardListPtr_ADDR, (uint8_t)wFilteredCardList_ADDR);
			gb_write8((uint16_t)(wCurCardListPtr_ADDR + 1u),
			  (uint8_t)(wFilteredCardList_ADDR >> 8));
			OpenCardPageFromCardList();
			(void)PrintPlayersCardsHeaderInfo();
			filter_params = FILTERS_CARD_SELECTION_PARAMS_ADDR;
			(void)InitCardSelectionParams(0u, &filter_params);
			wTempCardTypeFilter = wCurCardTypeFilter;
			(void)DrawHorizontalListCursor_Visible();
			PrintCardSelectionList();
			EnableLCD();
			list_params = HANDLE_PLAYERS_CARDS_DATA_ADDR;
			(void)InitCardSelectionParams(0u, &list_params);
			wCardListNumCursorPositions = wTempCardListNumCursorPositions;
			wCardListCursorPos = wTempCardListCursorPos;
		}
		if (return_to_filter != 0u)
			continue;
	}
}
/* <<< factory HandlePlayersCardsScreen */
