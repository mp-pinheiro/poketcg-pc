#include "home/deck_configuration.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define DECK_SIZE 60u
#define SCARDCOLLECTION_ADDR 0xA100u
#define MAX_AMOUNT_OF_CARD 99u
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
