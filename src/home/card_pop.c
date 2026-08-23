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

#include "home/card_pop.h"
#include "home/switch_sram.h"
#include "home/card_data.h"
#include "home/duel.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "generated/sram.h"
#define CIRCLE 0x00u
#define DIAMOND 0x01u
#define STAR 0x02u
#define MEW_LV15 0xa1u
#define MUSIC_BOOSTER_PACK 0x1cu
#define MUSIC_MATCH_VICTORY 0x18u
#define MUSIC_MEDAL 0x1du
#define PLAYER_TURN 0xc2u
#define VENUSAUR_LV64 0x0au
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

/* >>> factory DecideCardToReceiveFromCardPop */
uint8_t DecideCardToReceiveFromCardPop(void)
{
	hWhoseTurn = PLAYER_TURN;
	uint16_t hl1 = sPlayerName_ADDR;
	uint16_t de1;
	EnableSRAM();
	CalculateNameHash(&hl1, &de1);
	DisableSRAM();
	uint16_t bc = de1;

	uint16_t hl2 = wNameBuffer_ADDR;
	uint16_t de2;
	CalculateNameHash(&hl2, &de2);

	uint8_t b = (uint8_t)(bc >> 8);
	uint8_t c = (uint8_t)bc;
	uint8_t d_hi = (uint8_t)(de2 >> 8);
	uint8_t e_lo = (uint8_t)de2;

	uint8_t d = (uint8_t)(b - d_hi);
	uint8_t e = (uint8_t)(c - e_lo);
	gb_write8(wRNG1_ADDR, d);
	gb_write8((uint16_t)(wRNG1_ADDR + 1u), e);
	gb_write8((uint16_t)(wRNG1_ADDR + 2u), 0u);

	uint8_t card_e;
	uint8_t song;
	if (e == 5u) {
		song = MUSIC_MEDAL;
		gb_write8(wCardPopCardObtainSong_ADDR, song);
		card_e = (d & 0x01u) ? MEW_LV15 : VENUSAUR_LV64;
	} else {
		uint8_t rarity;
		if (e < 64u) {
			song = MUSIC_MATCH_VICTORY;
			rarity = STAR;
		} else if (e < 154u) {
			song = MUSIC_BOOSTER_PACK;
			rarity = DIAMOND;
		} else {
			song = MUSIC_BOOSTER_PACK;
			rarity = CIRCLE;
		}
		gb_write8(wCardPopCardObtainSong_ADDR, song);
		uint8_t count = CreateCardPopCandidateList(rarity);
		(void)ShuffleCards(count, wCardPopCardCandidates_ADDR);
		card_e = gb_read8(wCardPopCardCandidates_ADDR);
	}

	LoadCardDataToBuffer1_FromCardID(card_e);
	return card_e;
}
/* <<< factory DecideCardToReceiveFromCardPop */
