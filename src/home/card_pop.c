#include "home/card_pop.h"

#include "generated/wram.h"
#include "home/card_data.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "generated/sram.h"
#include "home/switch_sram.h"
#include "mem.h"
#define CARDPOP_NAME_LIST_MAX_ELEMS 0x10u
#define NAME_BUFFER_LENGTH 0x10u
/* <<< factory statics */

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

/* >>> factory LookUpNameInCardPopNameList */
void LookUpNameInCardPopNameList(void)
{
	uint8_t result = 0;
	uint16_t own_cursor = wCardPopNameList_ADDR;
	for (uint8_t i = 0; i < CARDPOP_NAME_LIST_MAX_ELEMS; i++) {
		uint8_t same = 1;
		for (uint8_t j = 0; j < NAME_BUFFER_LENGTH; j++) {
			if (gb_read8((uint16_t)(own_cursor + j)) != gb_read8((uint16_t)(wNameBuffer_ADDR + j))) {
				same = 0;
				break;
			}
		}
		if (same) {
			result = 0xff;
			goto done;
		}
		own_cursor = (uint16_t)(own_cursor + NAME_BUFFER_LENGTH);
	}

	EnableSRAM();
	uint16_t other_cursor = wOtherPlayerCardPopNameList_ADDR;
	for (uint8_t i = 0; i < CARDPOP_NAME_LIST_MAX_ELEMS; i++) {
		for (uint8_t j = 0; j < NAME_BUFFER_LENGTH; j++) {
			if (gb_read8((uint16_t)(other_cursor + j)) != gb_read8((uint16_t)(sPlayerName_ADDR + j)))
				break;
		}
		other_cursor = (uint16_t)(other_cursor + NAME_BUFFER_LENGTH);
	}

done:
	DisableSRAM();
	gb_write8(wCardPopNameSearchResult_ADDR, result);
}
/* <<< factory LookUpNameInCardPopNameList */
