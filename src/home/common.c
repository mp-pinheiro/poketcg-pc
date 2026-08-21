#include "home/common.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/core.h"

#define CARD_LIST_TERMINATOR 0xFFu
#define F_Z 0x80u
#define F_C 0x10u

#include "home/card_data.h"
#include "home/core.h"
#include "home/duel.h"
#include "mem.h"

#define DOUBLE_COLORLESS_ENERGY 0x07u
#define DUELVARS_ARENA_CARD     0xbbu
#define TYPE_ENERGY             0x08u

#include "home/card_data.h"
#include "home/duel.h"
#include "mem.h"

#include "generated/hram.h"
#include "generated/wram.h"

#include "mem.h"
/* <<< factory statics */

/* >>> factory CountOppEnergyCardsInHand */
/* common.asm:434-452 */
CountOppEnergyResult CountOppEnergyCardsInHand(uint8_t a, uint8_t b)
{
	CoreCardListResult r = CreateEnergyCardListFromHand(a);
	if (r.f & F_C)
		return (CountOppEnergyResult){r.a, r.f, b};
	uint8_t count = 0u;
	uint16_t hl = wDuelTempList_ADDR;
	while (gb_read8(hl) != CARD_LIST_TERMINATOR) {
		hl = (uint16_t)(hl + 1u);
		count++;
	}
	return (CountOppEnergyResult){count, (uint8_t)(count ? 0x00u : F_Z), count};
}
/* <<< factory CountOppEnergyCardsInHand */

/* >>> factory ConvertHPToDamageCounters_Bank8 */
/* common.asm:454-466 */
uint8_t ConvertHPToDamageCounters_Bank8(uint8_t a)
{
	return (uint8_t)(a / 10u);
}
/* <<< factory ConvertHPToDamageCounters_Bank8 */

/* >>> factory CalculateWordTensDigit */
/* common.asm:468-481 */
uint16_t CalculateWordTensDigit(uint16_t hl)
{
	return (uint16_t)(hl / 10u);
}
/* <<< factory CalculateWordTensDigit */

/* >>> factory PickTwoAttachedEnergyCards */
/* common.asm:285-411 */
PickTwoResult PickTwoAttachedEnergyCards(uint8_t a)
{
	hTempPlayAreaLocation_ff9d = a;
	(void)CreateArenaOrBenchEnergyCardList(a);
	uint8_t loc = hTempPlayAreaLocation_ff9d;
	if (CountNumberOfEnergyCardsAttached(loc).a < 2u)
		return (PickTwoResult){0xffu, 0u, 0u};

	loc = hTempPlayAreaLocation_ff9d;
	uint8_t deckindex = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + loc)).a;
	uint16_t id = GetCardIDFromDeckIndex(deckindex);
	wTempCardID = (uint8_t)id;
	LoadCardDataToBuffer1_FromCardID((uint8_t)id);
	wTempCardType = (uint8_t)(wLoadedCard1Type | TYPE_ENERGY);
	wTempAI = 0xffu;
	wCurCardCanAttack = 0xffu;

	uint16_t hl = wDuelTempList_ADDR;
	uint8_t v;
	for (;;) {
		v = gb_read8(hl);
		if (v == 0xffu)
			break;
		if ((uint8_t)GetCardIDFromDeckIndex(v) == DOUBLE_COLORLESS_ENERGY) {
			if (wTempAI != 0xffu) {
				wCurCardCanAttack = gb_read8(hl);
				goto done;
			}
			wTempAI = gb_read8(hl);
			hl = (uint16_t)(hl + 1u);
			continue;
		}
		hl = (uint16_t)(hl + 1u);
	}

	hl = wDuelTempList_ADDR;
	for (;;) {
		v = gb_read8(hl);
		if (v == 0xffu)
			break;
		if (CheckIfEnergyIsUseful(v).f & 0x10u) {
			if (wTempAI != 0xffu) {
				wCurCardCanAttack = gb_read8(hl);
				goto done;
			}
			wTempAI = gb_read8(hl);
			hl = (uint16_t)(hl + 1u);
			continue;
		}
		hl = (uint16_t)(hl + 1u);
	}

	hl = wDuelTempList_ADDR;
	if (wTempAI == 0xffu) {
		wTempAI = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		wCurCardCanAttack = gb_read8(hl);
	} else {
		uint8_t b = wTempAI;
		do {
			v = gb_read8(hl);
			hl = (uint16_t)(hl + 1u);
		} while (v == b);
		wCurCardCanAttack = v;
	}

done:
	return (PickTwoResult){wTempAI, wCurCardCanAttack, 1u};
}
/* <<< factory PickTwoAttachedEnergyCards */

/* >>> factory ClearMemory_Bank8 */
/* common.asm:414-426 */
void ClearMemory_Bank8(uint8_t a, uint16_t hl)
{
	uint32_t n = a ? (uint32_t)a : 0x100u;
	for (uint32_t i = 0; i < n; i++)
		gb_write8((uint16_t)(hl + i), 0u);
}
/* <<< factory ClearMemory_Bank8 */

/* >>> factory PickAttachedEnergyCardToRemove */
uint8_t PickAttachedEnergyCardToRemove(uint8_t a)
{
	hTempPlayAreaLocation_ff9d = a;
	(void)CreateArenaOrBenchEnergyCardList(a);
	uint8_t loc = hTempPlayAreaLocation_ff9d;
	(void)GetPlayAreaCardAttachedEnergies(loc);
	if (wTotalAttachedEnergies == 0u)
		return 0xffu;

	uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + loc)).a;
	uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
	wTempCardID = card_id;
	LoadCardDataToBuffer1_FromCardID(card_id);
	wTempCardType = (uint8_t)(wLoadedCard1Type | TYPE_ENERGY);

	uint16_t hl = wDuelTempList_ADDR;
	for (;;) {
		uint8_t deck = gb_read8(hl);
		if (deck == 0xffu)
			break;
		if ((uint8_t)GetCardIDFromDeckIndex(deck) == DOUBLE_COLORLESS_ENERGY)
			return deck;
		hl = (uint16_t)(hl + 1u);
	}

	hl = wDuelTempList_ADDR;
	for (;;) {
		uint8_t deck = gb_read8(hl);
		if (deck == 0xffu)
			break;
		if (CheckIfEnergyIsUseful(deck).f & 0x10u)
			return deck;
		hl = (uint16_t)(hl + 1u);
	}

	return gb_read8(wDuelTempList_ADDR);
}
/* <<< factory PickAttachedEnergyCardToRemove */

/* >>> factory CopyListWithFFTerminatorFromHLToDE_Bank8 */
CopyListBank8Result CopyListWithFFTerminatorFromHLToDE_Bank8(uint16_t *hl, uint16_t *de)
{
	uint16_t src = *hl;
	uint16_t dst = *de;

	for (;;) {
		uint8_t a = gb_read8(src);
		src = (uint16_t)(src + 1u);
		gb_write8(dst, a);
		if (a == 0xFFu) {
			*hl = src;
			*de = dst;
			return (CopyListBank8Result){a, 0xC0u};
		}
		dst = (uint16_t)(dst + 1u);
	}
}
/* <<< factory CopyListWithFFTerminatorFromHLToDE_Bank8 */
