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
