#include "home/card_pop.h"

#include "generated/wram.h"
#include "home/card_data.h"
#include "mem.h"

#define CARDPOP_NAME_LENGTH 16u
#define FIRST_CARD_ID 8u
#define TYPE_ENERGY 0x08u
#define PROMOTIONAL 0x40u

uint8_t CreateCardPopCandidateList(uint8_t a)
{
	uint16_t out = wCardPopCardCandidates_ADDR;
	uint8_t rarity = a;
	for (uint16_t id = FIRST_CARD_ID; id < 256u; id++) {
		CardPtrResult ptr = GetCardPointer((uint8_t)id);
		if (ptr.carry)
			break;
		LoadCardDataToBuffer1_FromCardID((uint8_t)id);
		if ((uint8_t)(wLoadedCard1Type & TYPE_ENERGY) != 0)
			continue;
		if (wLoadedCard1Rarity != rarity)
			continue;
		if ((uint8_t)(wLoadedCard1Set & 0xf0u) == PROMOTIONAL)
			continue;
		gb_write8(out, (uint8_t)id);
		out++;
	}
	gb_write8(out, 0);
	uint8_t count = 0;
	while (gb_read8(wCardPopCardCandidates_ADDR + count) != 0)
		count++;
	return count;
}

void CalculateNameHash(uint16_t *hl, uint16_t *de)
{
	uint8_t low = 0;
	uint8_t high = 0;
	uint16_t cursor = *hl;
	for (uint8_t i = 0; i < CARDPOP_NAME_LENGTH; i++) {
		uint8_t value = gb_read8(cursor);
		low = (uint8_t)(low + value);
		high ^= value;
		cursor++;
	}
	*hl = cursor;
	*de = (uint16_t)((uint16_t)high << 8 | low);
}
