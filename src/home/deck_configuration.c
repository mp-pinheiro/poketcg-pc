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
