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
