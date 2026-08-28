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

#include "home/duel.h"
#include "generated/wram.h"
#define MAX_PLAY_AREA_POKEMON 0x06u

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/duel.h"

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/duel.h"
#include "mem.h"

#define DECK_SIZE 0x3cu
#define DUELVARS_CARD_LOCATIONS 0x00u

#define MEWTWO_LV53 0x9du

#include "home/duel.h"
#include "home/card_data.h"
#include "generated/wram.h"
#include "generated/hram.h"
#define TYPE_TRAINER 0x10u

#include "home/duel.h"
#include "home/card_data.h"

#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xEFu

#define PLAY_AREA_ARENA 0x00u

#define CARD_LOCATION_DECK 0x00u

#include "home/common.h"
#include "home/duel.h"
#include "home/card_data.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/duel.h"
#include "home/core.h"
#include "home/card_data.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define DUELVARS_ARENA_CARD_480 0xBBu
#define TYPE_ENERGY_480 0x08u

#include "home/core.h"
#include "generated/wram.h"

#define AI_MEWTWO_MILL_F 0x07u
#define AI_MEWTWO_MILL (1u << AI_MEWTWO_MILL_F)
#define AI_TRAINER_CARD_PHASE_05 0x05u

#include "home/booster_pack.h"

#include "home/printer.h"

#include "generated/wram.h"
#include "home/attacks.h"
#include "home/duel.h"
#define ATTACK_FLAG1_ADDRESS 0x00u
#define HIGH_RECOIL_F 0x06u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/sound.h"
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

/* >>> factory LookForCardIDInPlayArea_Bank8 */
LookForCardIDInPlayAreaResult LookForCardIDInPlayArea_Bank8(uint8_t a, uint8_t b)
{
	wTempCardIDToLook = a;
	for (;;) {
		DuelistVarResult r = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + b));
		if (r.a == 0xffu)
			return (LookForCardIDInPlayAreaResult){0xffu, b, 0xc0u};
		uint8_t c = LoadCardDataToBuffer1_FromDeckIndex(r.a);
		if (wTempCardIDToLook == c)
			return (LookForCardIDInPlayAreaResult){b, b, 0x90u};
		b++;
		if (b == MAX_PLAY_AREA_POKEMON)
			return (LookForCardIDInPlayAreaResult){MAX_PLAY_AREA_POKEMON, 0xffu, 0x00u};
	}
}
/* <<< factory LookForCardIDInPlayArea_Bank8 */

/* >>> factory CheckIfHasCardIDInHand */
CheckIfHasCardIDInHandResult CheckIfHasCardIDInHand(uint8_t a)
{
	wTempCardIDToLook = a;
	(void)CreateHandCardList(0u);
	uint8_t *scan = wDuelTempList_PTR;
	uint8_t count = 0u;
	for (;;) {
		uint8_t index = *scan++;
		if (index == 0xFFu)
			return (CheckIfHasCardIDInHandResult){0xFFu, 0xC0u};
		hTempCardIndex_ff98 = index;
		uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(index);
		if (card_id != wTempCardIDToLook)
			continue;
		if (count != 0u)
			return (CheckIfHasCardIDInHandResult){hTempCardIndex_ff98, 0x10u};
		count++;
	}
}
/* <<< factory CheckIfHasCardIDInHand */

/* >>> factory FindBasicEnergyCardsInLocation */
FindBasicEnergyCardsInLocationResult FindBasicEnergyCardsInLocation(uint8_t a)
{
	wTempAI = a;
	uint8_t count = 0u;
	uint8_t e = 0u;
	uint16_t hl = wDuelTempList_ADDR;
	for (; e < DECK_SIZE; e++) {
		DuelistVarResult location = GetTurnDuelistVariable(
			(uint8_t)(DUELVARS_CARD_LOCATIONS + e));
		if (location.a != wTempAI)
			continue;

		uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(e);
		if (card_id >= DOUBLE_COLORLESS_ENERGY)
			continue;

		gb_write8(hl++, e);
		count++;
	}
	if (count == 0u)
		return (FindBasicEnergyCardsInLocationResult){0u, 0x90u, 0u, e, hl};

	gb_write8(hl, 0xffu);
	return (FindBasicEnergyCardsInLocationResult){count, 0x00u, count, e, hl};
}
/* <<< factory FindBasicEnergyCardsInLocation */

/* >>> factory CalculateBDividedByA_Bank8 */
CalculateBDividedByA_Bank8Result CalculateBDividedByA_Bank8(uint8_t a, uint8_t b)
{
	uint8_t divisor = a;
	uint8_t remainder = b;
	uint8_t quotient = 0u;

	for (;;) {
		uint8_t result = (uint8_t)(remainder - divisor);
		if (remainder < divisor) {
			uint8_t flags = 0x50u;
			if ((remainder & 0x0Fu) < (divisor & 0x0Fu))
				flags = (uint8_t)(flags | 0x20u);
			if (result == 0u)
				flags = (uint8_t)(flags | 0x80u);
			return (CalculateBDividedByA_Bank8Result){quotient, flags};
		}
		remainder = result;
		quotient = (uint8_t)(quotient + 1u);
	}
}
/* <<< factory CalculateBDividedByA_Bank8 */

/* >>> factory CheckIfPlayerHasPokemonOtherThanMewtwoLv53 */
/* common.asm:4-45 */
CheckIfPlayerHasPokemonOtherThanMewtwoLv53Result CheckIfPlayerHasPokemonOtherThanMewtwoLv53(uint8_t b, uint8_t c, uint8_t d, uint16_t hl)
{
	uint8_t e = 0u;
	SwapTurn();
	for (; e < DECK_SIZE; e++) {
		(void)LoadCardDataToBuffer2_FromDeckIndex(e);
		if (wLoadedCard2Type >= TYPE_ENERGY)
			continue;
		uint8_t card_id = wLoadedCard2ID;
		if (card_id != MEWTWO_LV53) {
			SwapTurn();
			return (CheckIfPlayerHasPokemonOtherThanMewtwoLv53Result){card_id, F_C, b, c, d, e, hl};
		}
	}
	SwapTurn();
	return (CheckIfPlayerHasPokemonOtherThanMewtwoLv53Result){DECK_SIZE, 0x00u, b, c, d, e, hl};
}
/* <<< factory CheckIfPlayerHasPokemonOtherThanMewtwoLv53 */

/* >>> factory RemoveFromListDifferentCardOfGivenType */
RemoveFromListDifferentCardOfGivenTypeResult RemoveFromListDifferentCardOfGivenType(
	uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint16_t orig_hl = hl;
	uint8_t count = CountCardsInDuelTempList().a;
	(void)ShuffleCards(count, hl);

	uint16_t p = hl;
	for (;;) {
		uint8_t deck_index = gb_read8(p);
		p = (uint16_t)(p + 1u);
		if (deck_index == 0xFFu)
			return (RemoveFromListDifferentCardOfGivenTypeResult){0xFFu, 0x00u, b, c, d, e, orig_hl};
		if (deck_index == e)
			continue;

		hTempCardIndex_ff98 = deck_index;
		uint16_t card_id16 = GetCardIDFromDeckIndex(deck_index);
		uint8_t card_type = GetCardType((uint8_t)card_id16);

		uint8_t matches;
		if (card_type < TYPE_ENERGY)
			matches = (d == 0x01u);
		else if (card_type != TYPE_TRAINER)
			matches = (d == 0x02u);
		else
			matches = (d == 0x00u);

		if (!matches)
			continue;

		uint16_t src = p;
		uint16_t dst = (uint16_t)(p - 1u);
		uint8_t v;
		do {
			v = gb_read8(src);
			src = (uint16_t)(src + 1u);
			gb_write8(dst, v);
			dst = (uint16_t)(dst + 1u);
		} while (v != 0xFFu);

		return (RemoveFromListDifferentCardOfGivenTypeResult){deck_index, 0x90u, b, c, d, e, orig_hl};
	}
}
/* <<< factory RemoveFromListDifferentCardOfGivenType */

/* >>> factory CountPokemonCardsInHandAndInPlayArea */
uint8_t CountPokemonCardsInHandAndInPlayArea(uint8_t c)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	gb_write8(wTempAI_ADDR, count);
	CreateHandCardList(c);
	uint16_t hl = wDuelTempList_ADDR;
	for (;;) {
		uint8_t deck_index = gb_read8(hl);
		hl++;
		if (deck_index == 0xFFu)
			break;
		uint16_t card_id = GetCardIDFromDeckIndex(deck_index);
		uint8_t type = GetCardType((uint8_t)card_id);
		if (type < TYPE_ENERGY) {
			count = (uint8_t)(count + 1u);
			gb_write8(wTempAI_ADDR, count);
		}
	}
	return count;
}
/* <<< factory CountPokemonCardsInHandAndInPlayArea */

/* >>> factory LookForCardIDInLocation_Bank8 */
LookForCardIDInLocationBank8Result LookForCardIDInLocation_Bank8(uint8_t location, uint8_t card_id_byte)
{
	for (uint8_t e = 0u; e < DECK_SIZE; e++) {
		uint8_t loc = GetTurnDuelistVariable((uint8_t)(DUELVARS_CARD_LOCATIONS + e)).a;
		if (loc != location)
			continue;
		uint16_t card_id = GetCardIDFromDeckIndex(e);
		if ((uint8_t)card_id == card_id_byte)
			return (LookForCardIDInLocationBank8Result){e, 0x90u};
	}
	return (LookForCardIDInLocationBank8Result){DECK_SIZE, 0x00u};
}
/* <<< factory LookForCardIDInLocation_Bank8 */

/* >>> factory LookForCardIDInHandList_Bank8 */
LookForCardIDInHandListResult LookForCardIDInHandList_Bank8(uint8_t a)
{
	wTempCardIDToLook = a;
	(void)CreateHandCardList(0u);
	uint8_t *scan = wDuelTempList_PTR;
	for (;;) {
		uint8_t index = *scan++;
		if (index == 0xFFu)
			return (LookForCardIDInHandListResult){0xFFu, 0xC0u};
		hTempCardIndex_ff98 = index;
		uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(index);
		if (card_id == wTempCardIDToLook)
			return (LookForCardIDInHandListResult){hTempCardIndex_ff98, 0x90u};
	}
}
/* <<< factory LookForCardIDInHandList_Bank8 */

/* >>> factory LookForCardIDInHandAndPlayArea */
LookForCardIDInHandAndPlayAreaResult LookForCardIDInHandAndPlayArea(uint8_t a)
{
	LookForCardIDInHandListResult r1 = LookForCardIDInHandList_Bank8(a);
	if (r1.f & 0x10u)
		return (LookForCardIDInHandAndPlayAreaResult){r1.a, r1.f};
	LookForCardIDInPlayAreaResult r2 = LookForCardIDInPlayArea_Bank8(a, PLAY_AREA_ARENA);
	if (r2.f & 0x10u)
		return (LookForCardIDInHandAndPlayAreaResult){r2.a, r2.f};
	uint8_t f = (r2.a == 0u) ? 0x80u : 0u;
	return (LookForCardIDInHandAndPlayAreaResult){r2.a, f};
}
/* <<< factory LookForCardIDInHandAndPlayArea */

/* >>> factory LookForCardIDToTradeWithDifferentHandCard */
LookForCardIDToTradeWithDifferentHandCardResult LookForCardIDToTradeWithDifferentHandCard(uint8_t a, uint8_t e)
{
	wCurCardCanAttack = e;
	wTempAI = a;
	LookForCardIDInHandListResult r1 = LookForCardIDInHandList_Bank8(a);
	if (r1.f & 0x10u) {
		uint8_t f = (r1.a == 0u) ? 0x80u : 0u;
		return (LookForCardIDToTradeWithDifferentHandCardResult){r1.a, f, e};
	}
	LookForCardIDInLocationBank8Result r2 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, wTempAI);
	if (!(r2.f & 0x10u)) {
		uint8_t f = (r2.a == 0u) ? 0x80u : 0u;
		return (LookForCardIDToTradeWithDifferentHandCardResult){r2.a, f, e};
	}
	wTempAI = r2.a;
	uint8_t c = wCurCardCanAttack;
	(void)CreateHandCardList(0u);
	uint8_t *scan = wDuelTempList_PTR;
	for (;;) {
		uint8_t index = *scan++;
		if (index == 0xFFu)
			return (LookForCardIDToTradeWithDifferentHandCardResult){0xFFu, 0x00u, e};
		uint8_t b = index;
		uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(index);
		if (card_id == c)
			continue;
		if (wLoadedCard1Type < TYPE_ENERGY)
			return (LookForCardIDToTradeWithDifferentHandCardResult){wTempAI, 0x10u, b};
	}
}
/* <<< factory LookForCardIDToTradeWithDifferentHandCard */

/* >>> factory LookForCardIDInDeck_GivenCardIDInHand */
LookForCardIDInDeck_GivenCardIDInHandResult LookForCardIDInDeck_GivenCardIDInHand(uint8_t a, uint8_t b)
{
	wTempAI = b;
	wCurCardCanAttack = a;
	LookForCardIDInLocationBank8Result r1 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, a);
	if (!(r1.f & 0x10u))
		return (LookForCardIDInDeck_GivenCardIDInHandResult){r1.a, r1.f};
	wTempAIPokemonCard = r1.a;
	LookForCardIDInHandListResult r2 = LookForCardIDInHandList_Bank8(wTempAI);
	if (!(r2.f & 0x10u))
		return (LookForCardIDInDeck_GivenCardIDInHandResult){r2.a, r2.f};
	LookForCardIDInHandAndPlayAreaResult r3 = LookForCardIDInHandAndPlayArea(wCurCardCanAttack);
	if (r3.f & 0x10u) {
		uint8_t f = (r3.a == 0u) ? 0x80u : 0u;
		return (LookForCardIDInDeck_GivenCardIDInHandResult){r3.a, f};
	}
	uint8_t f = (uint8_t)((r3.f & 0x80u) | 0x10u);
	return (LookForCardIDInDeck_GivenCardIDInHandResult){wTempAIPokemonCard, f};
}
/* <<< factory LookForCardIDInDeck_GivenCardIDInHand */

/* >>> factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */
LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(uint8_t a, uint8_t b)
{
	wTempAI = b;
	wCurCardCanAttack = a;
	LookForCardIDInLocationBank8Result r1 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, a);
	if (!(r1.f & 0x10u))
		return (LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult){r1.a, r1.f};
	wTempAIPokemonCard = r1.a;
	LookForCardIDInHandAndPlayAreaResult r2 = LookForCardIDInHandAndPlayArea(wTempAI);
	if (!(r2.f & 0x10u))
		return (LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult){r2.a, r2.f};
	LookForCardIDInHandAndPlayAreaResult r3 = LookForCardIDInHandAndPlayArea(wCurCardCanAttack);
	if (r3.f & 0x10u) {
		uint8_t f = (r3.a == 0u) ? 0x80u : 0u;
		return (LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult){r3.a, f};
	}
	uint8_t f = (uint8_t)((r3.f & 0x80u) | 0x10u);
	return (LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult){wTempAIPokemonCard, f};
}
/* <<< factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */

/* >>> factory AddStarterDeck */
void AddStarterDeck(uint8_t a)
{
	_AddStarterDeck(a);
}
/* <<< factory AddStarterDeck */

/* >>> factory FindDuplicatePokemonCards */
FindDuplicatePokemonCardsResult FindDuplicatePokemonCards(void)
{
	wTempAI = 0xFFu;
	(void)CreateHandCardList(0u);

	uint16_t list = wDuelTempList_ADDR;
	uint8_t outer = 0u;
	for (;;) {
		uint8_t outer_idx = gb_read8((uint16_t)(list + outer));
		if (outer_idx == 0xFFu)
			break;
		uint8_t outer_id = (uint8_t)GetCardIDFromDeckIndex(outer_idx);
		uint8_t inner = (uint8_t)(outer + 1u);
		for (;;) {
			uint8_t inner_idx = gb_read8((uint16_t)(list + inner));
			if (inner_idx == 0xFFu)
				break;
			uint8_t inner_id = (uint8_t)GetCardIDFromDeckIndex(inner_idx);
			if (inner_id == outer_id) {
				uint8_t type = GetCardType(inner_id);
				if (type < TYPE_ENERGY)
					wTempAI = inner_idx;
				break;
			}
			inner = (uint8_t)(inner + 1u);
		}
		outer = (uint8_t)(outer + 1u);
	}

	uint8_t final_val = wTempAI;
	if (final_val == 0xFFu)
		return (FindDuplicatePokemonCardsResult){final_val, 0x00u};
	return (FindDuplicatePokemonCardsResult){final_val, 0x10u};
}
/* <<< factory FindDuplicatePokemonCards */

/* >>> factory AIPickEnergyCardToDiscard */
uint8_t AIPickEnergyCardToDiscard(uint8_t a)
{
	gb_write8(hTempPlayAreaLocation_ff9d_ADDR, a);
	(void)CreateArenaOrBenchEnergyCardList(a);
	uint8_t loc = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
	(void)GetPlayAreaCardAttachedEnergies(loc);
	uint8_t total = gb_read8(wTotalAttachedEnergies_ADDR);
	if (total == 0u)
		return 0xFFu;

	uint8_t b = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
	DuelistVarResult var = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_480 + b));
	uint16_t id16 = GetCardIDFromDeckIndex(var.a);
	uint8_t card_id = (uint8_t)id16;
	gb_write8(wTempCardID_ADDR, card_id);
	LoadCardDataToBuffer1_FromCardID(card_id);
	uint8_t type = (uint8_t)(gb_read8(wLoadedCard1Type_ADDR) | TYPE_ENERGY_480);
	gb_write8(wTempCardType_ADDR, type);

	uint16_t hl = wDuelTempList_ADDR;
	for (;;) {
		uint8_t v = gb_read8(hl);
		if (v == 0xFFu)
			return gb_read8(wDuelTempList_ADDR);
		CheckIfEnergyIsUsefulResult r = CheckIfEnergyIsUseful(v);
		if ((r.f & 0x10u) == 0u)
			return v;
		hl = (uint16_t)(hl + 1u);
	}
}
/* <<< factory AIPickEnergyCardToDiscard */

/* >>> factory HandleAIAntiMewtwoDeckStrategy */
HandleAIAntiMewtwoDeckStrategyResult HandleAIAntiMewtwoDeckStrategy(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t carry_z;
	a = wAIBarrierFlagCounter;
	if ((a & (1u << AI_MEWTWO_MILL_F)) == 0u) {
		carry_z = 0x80u;
		goto set_carry;
	}
	if (a >= (uint8_t)(AI_MEWTWO_MILL + 2u)) {
		wAIBarrierFlagCounter = 0u;
		a = 0u;
		carry_z = 0x80u;
		goto set_carry;
	}
	CountNumberOfSetUpBenchPokemonResult bench = CountNumberOfSetUpBenchPokemon(a, f, b, c, d, e, hl);
	if (bench.a < 4u)
		return (HandleAIAntiMewtwoDeckStrategyResult){bench.a, 0x10u};
	AIProcessHandTrainerCardsWrapResult trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_05);
	f = (trainer.a == 0u) ? 0x80u : 0x00u;
	return (HandleAIAntiMewtwoDeckStrategyResult){trainer.a, f};
set_carry:
	f = carry_z;
	f = (uint8_t)((f & 0x80u) | 0x10u);
	return (HandleAIAntiMewtwoDeckStrategyResult){a, f};
}
/* <<< factory HandleAIAntiMewtwoDeckStrategy */

/* >>> factory OpenBoosterPack */
void OpenBoosterPack(void)
{
	_OpenBoosterPack();
}
/* <<< factory OpenBoosterPack */

/* >>> factory PreparePrinterConnection */
/* menus/common.asm:26. `farcall _PreparePrinterConnection` / `ret`.
 * FarCall (home/farcall.asm:62-88) pushes af/de/hl before the bank switch and
 * pops them back immediately before jumping to the target, and the return
 * trampoline SwitchToBankAtSP (farcall.asm:44-53) saves and restores af/hl
 * around its own bankswitch, so the wrapper is register-transparent: whatever
 * the callee leaves is what this routine's caller sees. The ported callee's
 * result is carry alone -- the single caller HandlePrinterMenu
 * (engine/menus/printer.asm:232) tests nothing else -- so only f is
 * forwarded, and it is forwarded rather than recomputed. */
uint8_t PreparePrinterConnection(uint16_t hl)
{
	return _PreparePrinterConnection(hl).f;
}
/* <<< factory PreparePrinterConnection */

/* >>> factory AICheckIfAttackIsHighRecoil */
AICheckIfAttackIsHighRecoilResult AICheckIfAttackIsHighRecoil(void)
{
	AIProcessAttacksResult processed = AIProcessButDontUseAttack();
	if ((processed.f & 0x10u) == 0u)
		return (AICheckIfAttackIsHighRecoilResult){processed.f};
	uint8_t selected_attack = wSelectedAttack;
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	(void)CopyAttackDataAndDamage_FromDeckIndex(arena.a, selected_attack);
	AttackFlagResult flag = CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | HIGH_RECOIL_F);
	return (AICheckIfAttackIsHighRecoilResult){(uint8_t)(flag.f ^ 0x10u)};
}
/* <<< factory AICheckIfAttackIsHighRecoil */

/* >>> factory PrintDeckConfiguration */
void PrintDeckConfiguration(uint8_t a)
{
	_PrintDeckConfiguration(a);
}
/* <<< factory PrintDeckConfiguration */

/* >>> factory ShowPromotionalCardScreen */
/* menus/common.asm:46. `farcall _ShowPromotionalCardScreen` / `ret`.
 * The callee never returns without the timer ISR: its `.loop` (06:6680) spins
 * on `call AssertSongFinished` / `or a` / `jr nz` until wCurSongID reads $80,
 * and the call-level runner arms VBlank alone. Completion is therefore declared
 * pre-ret at that wait, and the body ported here is the prefix the reference
 * has executed by then: promotional_card.asm:41-50 loads the card data, pauses
 * the field song, starts MUSIC_MEDAL ($1D) and sets hWhoseTurn to PLAYER_TURN
 * ($C2). The screen work in between (_DisplayCardDetailScreen) rewrites neither
 * observed byte, and everything after the wait -- ResumeSong,
 * OpenCardPage_FromHand -- is past the stop. */
void ShowPromotionalCardScreen(uint8_t a)
{
	LoadCardDataToBuffer1_FromCardID(a);
	PauseSong();
	PlaySong(0x1Du);
	hWhoseTurn = 0xC2u;
}
/* <<< factory ShowPromotionalCardScreen */
