#include "home/trainer_cards.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/duel.h"
#include "mem.h"
#include "home/random.h"
#define TYPE_TRAINER 0x10u
#define TYPE_ENERGY 0x08u

#include "home/card_data.h"
#include "home/duel.h"

#include "home/duel.h"
#include "home/card_data.h"

#include "home/trainer_cards.h"

#include "home/duel.h"
#include "home/card_data.h"
#include "home/trainer_cards.h"
#include "generated/wram.h"
#include "mem.h"
#define DUELVARS_NUMBER_OF_CARDS_IN_HAND 0xEEu
#define DUELVARS_ARENA_CARD_STATUS 0xF0u
#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK 0xBAu

#include "home/duel.h"
#include "home/card_data.h"
#include "home/trainer_cards.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/trainer_cards.h"
#include "home/duel.h"
#include "home/random.h"
#include "generated/wram.h"
#define DECK_SIZE 0x3cu

#include "home/duel.h"
#include "home/trainer_cards.h"
#include "generated/wram.h"
#define ENERGY_REMOVAL 0xd0u
#define MR_MIME 0x9bu
#define POKEMON_TRADER 0xc9u

#include "home/core.h"
#include "home/substatus.h"
#include "home/duel.h"
#include "home/common.h"
#include "home/trainer_cards.h"
#include "home/card_data.h"
#include "generated/wram.h"
#include "generated/hram.h"

#define BLASTOISE 0x43u
#define CARD_LOCATION_DISCARD_PILE 0x02u
#define DUELVARS_ARENA_CARD 0xbbu
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xefu
#define GO_GO_RAIN_DANCE_DECK_ID 0x12u
#define MUK 0x27u
#define PLAY_AREA_ARENA 0x00u

#include "home/duel.h"
#include "home/common.h"
#include "home/substatus.h"
#include "home/core.h"
#include "generated/wram.h"
#include "generated/hram.h"

#define ALAKAZAM 0x90u
#define DRAGONITE_LV41 0xc1u
#define DUELVARS_ARENA_CARD_HP 0xc8u
#define GENGAR 0x98u
#define VENUSAUR_LV64 0x0au
#define VENUSAUR_LV67 0x0bu
#define VILEPLUME 0x1eu

#define MOLTRES_LV35 0x3fu
#define MOLTRES_LV37 0x40u

#define ARTICUNO_LV35 0x5eu
#define ARTICUNO_LV37 0x5fu
#define CARD_LOCATION_DECK 0x00u
#define CHANSEY 0xb8u
#define DEWGONG 0x4cu
#define DITTO 0xbbu
#define LAPRAS 0x59u
#define SEEL 0x4bu

#define JIGGLYPUFF_LV12 0xadu
#define TAUROS 0xbau

#define ARCANINE_LV34 0x37u
#define DODRIO 0xb6u
#define DODUO 0xb5u
#define GROWLITHE 0x36u
#define RATICATE 0xa8u
#define RATTATA 0xa7u

#define GRIMER 0x26u
#define PROFESSOR_OAK 0xc3u

#define DIGLETT 0x79u
#define DOUBLE_COLORLESS_ENERGY 0x07u
#define DUGTRIO 0x7au
#define FIGHTING_ENERGY 0x05u
#define GEODUDE 0x80u
#define GOLEM 0x82u
#define GRAVELER 0x81u
#define ONIX 0x83u
#define RHYHORN 0x89u

#define ANGER_DECK_ID 0x31u
#define FIRE_CHARGE_DECK_ID 0x17u
#define ROCK_CRUSHER_DECK_ID 0x11u
#define WONDERS_OF_SCIENCE_DECK_ID 0x16u

#define DRAGONAIR 0xc0u
#define DRATINI 0xbfu
#define EEVEE 0xbcu
#define FLAREON_LV22 0x3du
#define JOLTEON_LV24 0x72u
#define VAPOREON_LV29 0x5au
#define ZAPDOS_LV68 0x76u
/* <<< factory statics */


/* >>> factory RemoveCardFromList */
/* trainer_cards.asm:2760-2776. Shifts the $ff-terminated list down by one byte,
 * removing the entry just before hl. Leaves hl decremented; de preserved. */
void RemoveCardFromList(uint16_t *hl)
{
	uint16_t src = *hl;
	uint16_t dst = (uint16_t)(src - 1u);
	uint8_t v;
	do {
		v = gb_read8(src);
		src = (uint16_t)(src + 1u);
		gb_write8(dst, v);
		dst = (uint16_t)(dst + 1u);
	} while (v != 0xFFu);
	*hl = (uint16_t)(*hl - 1u);
}
/* <<< factory RemoveCardFromList */


/* >>> factory FindDuplicateCards */
/* trainer_cards.asm:2788-2859 */
FindDupResult FindDuplicateCards(uint16_t hl)
{
	wce0f = 0xFFu;
	gb_write8((uint16_t)(wce0f_ADDR + 1u), 0xFFu);
	uint16_t outer = hl;
	for (;;) {
		uint8_t idx = gb_read8(outer);
		outer = (uint16_t)(outer + 1u);
		if (idx == 0xFFu)
			break;
		uint8_t b = (uint8_t)GetCardIDFromDeckIndex(idx);
		uint16_t inner = outer;
		for (;;) {
			uint8_t c = gb_read8(inner);
			inner = (uint16_t)(inner + 1u);
			if (c == 0xFFu)
				break;
			if ((uint8_t)GetCardIDFromDeckIndex(c) != b)
				continue;
			if (GetCardType(b) < TYPE_ENERGY)
				wce0f = c;
			else
				gb_write8((uint16_t)(wce0f_ADDR + 1u), c);
			break;
		}
	}
	uint8_t lo = wce0f;
	uint8_t hi = gb_read8((uint16_t)(wce0f_ADDR + 1u));
	if (lo == 0xFFu && hi == 0xFFu)
		return (FindDupResult){0xFFu, 0x90u, outer};
	uint8_t a = (lo != 0xFFu) ? lo : hi;
	return (FindDupResult){a, (uint8_t)(a == 0u ? 0x80u : 0x00u), outer};
}
/* <<< factory FindDuplicateCards */

/* >>> factory FindAndRemoveCardFromList */
/* trainer_cards.asm:3072-3082 */
void FindAndRemoveCardFromList(uint8_t a, uint16_t hl)
{
	uint16_t p = hl;
	uint8_t v;
	do {
		v = gb_read8(p);
		p = (uint16_t)(p + 1u);
	} while (v != a);
	RemoveCardFromList(&p);
}
/* <<< factory FindAndRemoveCardFromList */
/* >>> factory PickPokedexCards */
PickPokedexResult PickPokedexCards(void)
{
	DuelistVarResult remaining = GetTurnDuelistVariable(0xBAu);
	uint16_t deck = (uint16_t)((remaining.hl & 0xFF00u) |
				   (uint8_t)(remaining.a + 0x7Eu));
	uint8_t types[5], indices[5];
	wAIPokedexCounter = 0;
	for (uint8_t i = 0; i < 5; i++) {
		indices[i] = gb_read8((uint16_t)(deck + i));
		types[i] = GetCardType((uint8_t)GetCardIDFromDeckIndex(indices[i]));
		gb_write8((uint16_t)(wce08_ADDR + i), types[i]);
		gb_write8((uint16_t)(wce0f_ADDR + i), indices[i]);
	}
	gb_write8((uint16_t)(wce08_ADDR + 5u), 0xFFu);
	uint8_t out = 0;
	for (uint8_t wanted = 0; wanted < 3; wanted++) {
		for (uint8_t i = 0; i < 5; i++) {
			uint8_t type = types[i];
			if ((wanted == 0 && !(type & TYPE_ENERGY)) ||
			    (wanted == 1 && type >= TYPE_ENERGY) ||
			    (wanted == 2 && type != TYPE_TRAINER))
				continue;
			gb_write8((uint16_t)(wce1a_ADDR + out++), indices[i]);
		}
	}
	return (PickPokedexResult){0xFFu, 0x90u};
}
/* <<< factory PickPokedexCards */
/* >>> factory AIDecide_Recycle */
AIDecideResult AIDecide_Recycle(void)
{
	CardListResult discard = CreateDiscardPileCardList(0);
	if (discard.f & 0x10u)
		return (AIDecideResult){0x80u};
	uint8_t priority[5] = {0xFFu, 0xFFu, 0xFFu, 0xFFu, 0xFFu};
	uint16_t list = wDuelTempList_ADDR;
	uint8_t ghost = wOpponentDeckID == 0x0Du;
	for (;;) {
		uint8_t deck_index = gb_read8(list++);
		if (deck_index == 0xFFu)
			break;
		uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		if (!ghost) {
			if (card_id == 0x07u) priority[0] = deck_index;
			else if (card_id == 0xB8u) priority[1] = deck_index;
			else if (card_id == 0xBAu) priority[2] = deck_index;
			else if (card_id == 0xADu) priority[3] = deck_index;
		} else {
			if (card_id == 0x95u) priority[0] = deck_index;
			else if (card_id == 0x94u) priority[1] = deck_index;
			else if (card_id == 0x1Au) priority[2] = deck_index;
			else if (card_id == 0xBBu) priority[3] = deck_index;
			else if (card_id == 0xB2u) priority[4] = deck_index;
		}
	}
	for (uint8_t i = 0; i < 5u; i++)
		if (priority[i] != 0xFFu)
			return (AIDecideResult){0x10u};
	return (AIDecideResult){0x00u};
}
/* <<< factory AIDecide_Recycle */

/* >>> factory AIDecide_Maintenance */
AIDecideMaintenanceResult AIDecide_Maintenance(void)
{
	DuelistVarResult hand = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (wOpponentDeckID == 0x0Du) {
		if (Random(10u) >= 2u || hand.a < 3u)
			return (AIDecideMaintenanceResult){hand.a,
				(uint8_t)(hand.a == 0u ? 0x80u : 0u)};
		(void)CreateHandCardList(0);
		TempListResult count = CountCardsInDuelTempList();
		(void)ShuffleCards(count.a, wDuelTempList_ADDR);
		uint16_t p = wDuelTempList_ADDR;
		uint8_t target = wAITrainerCardToPlay, found = 0, out = 0;
		while (found < 2u) {
			uint8_t card = gb_read8(p++);
			if (card == 0xFFu)
				return (AIDecideMaintenanceResult){0, 0x00u};
			if (card == target)
				continue;
			gb_write8((uint16_t)(wce1a_ADDR + out++), card);
			found++;
		}
		return (AIDecideMaintenanceResult){0, 0x10u};
	}
	if (hand.a < 4u)
		return (AIDecideMaintenanceResult){hand.a,
			(uint8_t)(hand.a == 0u ? 0x80u : 0u)};
	(void)CreateHandCardList(0);
	FindAndRemoveCardFromList(wAITrainerCardToPlay, wDuelTempList_ADDR);
	FindDupResult first = FindDuplicateCards(wDuelTempList_ADDR);
	if (first.a == 0xFFu)
		return (AIDecideMaintenanceResult){first.a, 0x00u};
	wce1a = first.a;
	FindAndRemoveCardFromList(first.a, wDuelTempList_ADDR);
	FindDupResult second = FindDuplicateCards(wDuelTempList_ADDR);
	if (second.a == 0xFFu)
		return (AIDecideMaintenanceResult){second.a, 0x00u};
	wce1b = second.a;
	return (AIDecideMaintenanceResult){second.a, 0x10u};
}
/* <<< factory AIDecide_Maintenance */
/* >>> factory AIDecide_Lass */
AIDecideResult AIDecide_Lass(void)
{
	uint8_t hand_count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	if (hand_count < 7u)
		return (AIDecideResult){hand_count == 0u ? 0x80u : 0x00u};
	(void)CreateHandCardList(hand_count);
	uint16_t list = wDuelTempList_ADDR;
	for (;;) {
		uint8_t deck_index = gb_read8(list++);
		if (deck_index == 0xFFu)
			return (AIDecideResult){0x90u};
		uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		if (card_id == 0xC7u)
			continue;
		if (gb_read8(wLoadedCard1Type_ADDR) == 0x08u)
			return (AIDecideResult){0x00u};
	}
}
/* <<< factory AIDecide_Lass */

/* >>> factory AIDecide_Imakuni */
AIDecideResult AIDecide_Imakuni(void)
{
	uint8_t status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
	if ((status & 0x0Fu) == 0x01u)
		return (AIDecideResult){0x00u};
	return (AIDecideResult){0x10u};
}
/* <<< factory AIDecide_Imakuni */
/* >>> factory AIDecide_PokemonFlute */
AIDecidePokemonFluteResult AIDecide_PokemonFlute(uint8_t c)
{
	SwapTurn();
	CardListResult discard = CreateDiscardPileCardList(c);
	SwapTurn();
	if (discard.f & 0x10u)
		return (AIDecidePokemonFluteResult){discard.a, (uint8_t)(discard.a == 0u ? 0x80u : 0u)};
	uint8_t count = GetNonTurnDuelistVariable(0xEFu).a;
	if (count >= 6u)
		return (AIDecidePokemonFluteResult){count, (uint8_t)(count == 0u ? 0x80u : 0u)};
	wce06 = 0xFFu;
	wce08 = 0xFFu;
	for (uint16_t p = wDuelTempList_ADDR;; p++) {
		uint8_t index = gb_read8(p);
		if (index == 0xFFu)
			break;
		(void)LoadCardDataToBuffer1_FromDeckIndex(index);
		if (wLoadedCard1Type >= TYPE_ENERGY || wLoadedCard1Stage != 0u ||
		    wLoadedCard1HP >= wce06)
			continue;
		wce06 = wLoadedCard1HP;
		wce08 = index;
	}
	if (wOpponentDeckID == 0x34u) {
		if (Random(10u) >= 2u)
			return (AIDecidePokemonFluteResult){0, 0};
		return (AIDecidePokemonFluteResult){wce08, wce08 == 0xFFu ? 0u : 0x10u};
	}
	if (wce06 >= 50u)
		return (AIDecidePokemonFluteResult){wce06, 0};
	return (AIDecidePokemonFluteResult){wce08, 0x10u};
}
/* <<< factory AIDecide_PokemonFlute */
/* >>> factory AIDecide_ClefairyDollOrMysteriousFossil */
AIDecidePokemonFluteResult AIDecide_ClefairyDollOrMysteriousFossil(void)
{
	uint8_t count = GetTurnDuelistVariable(0xEFu).a;
	if (count >= 6u)
		return (AIDecidePokemonFluteResult){count, 0};
	uint8_t arena = GetTurnDuelistVariable(0xBBu).a;
	if ((uint8_t)GetCardIDFromDeckIndex(arena) == 0xB0u)
		return (AIDecidePokemonFluteResult){arena, 0x10u};
	return (AIDecidePokemonFluteResult){count, count < 4u ? 0x10u : 0};
}
/* <<< factory AIDecide_ClefairyDollOrMysteriousFossil */

/* >>> factory AIDecide_Defender_Phase14 */
AIDecideResult AIDecide_Defender_Phase14(void)
{
	uint8_t flag = CheckLoadedAttackFlag(0x06u).f;
	if (!(flag & 0x10u))
		flag = CheckLoadedAttackFlag(0x04u).f;
	if (!(flag & 0x10u))
		return (AIDecideResult){0x80u};
	uint8_t arena = GetTurnDuelistVariable(0xBBu).a;
	(void)LoadCardDataToBuffer2_FromDeckIndex(arena);
	uint8_t damage = wSelectedAttack == 0u ? wLoadedCard2Atk1EffectParam :
		wLoadedCard2Atk2EffectParam;
	uint8_t color = TranslateColorToWR(GetArenaCardColor());
	if (GetArenaCardWeakness() & color)
		damage = (uint8_t)(damage << 1);
	if (GetArenaCardResistance() & color) {
		if (damage < 30u)
			return (AIDecideResult){0};
		damage = (uint8_t)(damage - 30u);
	}
	if (damage == 0u)
		return (AIDecideResult){0};
	damage = (uint8_t)(damage - 20u);
	uint8_t hp = GetTurnDuelistVariable(0x08u).a;
	return (AIDecideResult){(uint8_t)(((damage != 0u) && (hp > damage)) ? 0x10u : 0)};
}
/* <<< factory AIDecide_Defender_Phase14 */

/* >>> factory AIDecide_Bill */
AIDecideResult AIDecide_Bill(void)
{
	uint8_t remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	uint8_t f = 0x40u;
	if ((remaining & 0x0Fu) < 3u)
		f |= 0x20u;
	if (remaining < 51u)
		f |= 0x10u;
	if (remaining == 51u)
		f |= 0x80u;
	return (AIDecideResult){f};
}
/* <<< factory AIDecide_Bill */

/* >>> factory AIDecide_Gambler */
AIDecideResult AIDecide_Gambler(void)
{
	if (wOpponentDeckID == 0x34u) {
		if (Random(10u) < 2u)
			return (AIDecideResult){0x10u};
		return (AIDecideResult){0x80u};
	}
	if (!(wAIBarrierFlagCounter & 0x80u))
		return (AIDecideResult){0x80u};
	uint8_t remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	return (AIDecideResult){(uint8_t)(remaining >= 56u ? 0x90u : 0x80u)};
}
/* <<< factory AIDecide_Gambler */

/* >>> factory AIDecide_Revive */
AIDecideReviveResult AIDecide_Revive(void)
{
	CardListResult discard = CreateDiscardPileCardList(0);
	if (discard.f & 0x10u)
		return (AIDecideReviveResult){discard.a, 0x80u};
	if (GetTurnDuelistVariable(0xEFu).a >= 4u) {
		uint8_t count = GetTurnDuelistVariable(0xEFu).a;
		return (AIDecideReviveResult){count, 0};
	}
	for (uint16_t p = wDuelTempList_ADDR;; p++) {
		uint8_t index = gb_read8(p);
		if (index == 0xFFu)
			return (AIDecideReviveResult){0xFFu, 0};
		uint8_t card = LoadCardDataToBuffer1_FromDeckIndex(index);
		if (card == 0x88u || card == 0x87u)
			return (AIDecideReviveResult){index, 0x90u};
		if (card == 0xBAu)
			return (AIDecideReviveResult){0, 0x10u};
	}
}
/* <<< factory AIDecide_Revive */

/* >>> factory AIDecide_ImposterProfessorOak */
AIDecideResult AIDecide_ImposterProfessorOak(void)
{
	uint8_t remaining = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	uint8_t hand = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	if (remaining < (60u - 14u)) {
		if (hand < 9u)
			return (AIDecideResult){(uint8_t)(hand == 0u ? 0x80u : 0x00u)};
		return (AIDecideResult){(uint8_t)(hand == 9u ? 0x90u : 0x10u)};
	}
	if (hand < 6u)
		return (AIDecideResult){0x10u};
	return (AIDecideResult){0x00u};
}
/* <<< factory AIDecide_ImposterProfessorOak */

/* >>> factory PickPokedexCards_Unreferenced */
PickPokedexResult PickPokedexCards_Unreferenced(void)
{
	DuelistVarResult remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	uint16_t deck = (uint16_t)((remaining.hl & 0xFF00u) |
				   (uint8_t)(remaining.a + 0x7Eu));
	uint8_t types[5], indices[5];
	wAIPokedexCounter = 0;
	for (uint8_t i = 0; i < 5u; i++) {
		indices[i] = gb_read8((uint16_t)(deck + i));
		types[i] = GetCardType((uint8_t)GetCardIDFromDeckIndex(indices[i]));
		gb_write8((uint16_t)(wce08_ADDR + i), types[i]);
		gb_write8((uint16_t)(wce0f_ADDR + i), indices[i]);
	}
	gb_write8((uint16_t)(wce08_ADDR + 5u), 0xFFu);
	uint8_t out = 0;
	for (uint8_t wanted = 0; wanted < 3u; wanted++) {
		for (uint8_t i = 0; i < 5u; i++) {
			uint8_t type = types[i];
			if ((wanted == 0u && type >= TYPE_ENERGY) ||
			    (wanted == 1u && type != TYPE_TRAINER) ||
			    (wanted == 2u && !(type & TYPE_ENERGY)))
				continue;
			gb_write8((uint16_t)(wce1a_ADDR + out++), indices[i]);
		}
	}
	return (PickPokedexResult){0xFFu, (uint8_t)(0x80u | 0x10u)};
}
/* <<< factory PickPokedexCards_Unreferenced */

/* >>> factory AIDecide_Pokedex */
AIDecidePokedexResult AIDecide_Pokedex(void)
{
	uint8_t counter = wAIPokedexCounter;
	if (counter < 6u)
		return (AIDecidePokedexResult){counter, (uint8_t)(counter == 0u ? 0x80u : 0u)};
	DuelistVarResult notindeck = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	if (notindeck.a >= (DECK_SIZE - 4u))
		return (AIDecidePokedexResult){notindeck.a, (uint8_t)(notindeck.a == 0u ? 0x80u : 0u)};
	uint8_t roll = Random(10u);
	if (roll >= 3u)
		return (AIDecidePokedexResult){roll, (uint8_t)(roll == 0u ? 0x80u : 0u)};
	PickPokedexResult picked = PickPokedexCards();
	return (AIDecidePokedexResult){picked.a, picked.f};
}
/* <<< factory AIDecide_Pokedex */

/* >>> factory AIDecide_ItemFinder */
AIDecide_ItemFinderResult AIDecide_ItemFinder(void)
{
	CardListResult discard = CreateDiscardPileCardList(0u);
	uint8_t a = discard.a;
	if (!(discard.f & 0x10u)) {
		uint16_t hl = wDuelTempList_ADDR;
		uint8_t deck_index = 0u;
		uint8_t found = 0u;
		for (;;) {
			deck_index = gb_read8(hl);
			hl = (uint16_t)(hl + 1u);
			if (deck_index == 0xFFu) {
				a = 0xFFu;
				break;
			}
			uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(deck_index);
			if (card_id == ENERGY_REMOVAL) {
				found = 1u;
				break;
			}
		}
		if (found) {
			wce06 = deck_index;

			(void)CreateHandCardList(0u);
			hl = wDuelTempList_ADDR;
			for (;;) {
				uint8_t v = gb_read8(hl);
				hl = (uint16_t)(hl + 1u);
				if (v == 0xFFu)
					break;
				uint8_t card_id2 = LoadCardDataToBuffer1_FromDeckIndex(v);
				if (card_id2 == MR_MIME || card_id2 == POKEMON_TRADER)
					RemoveCardFromList(&hl);
			}

			FindAndRemoveCardFromList(wAITrainerCardToPlay, wDuelTempList_ADDR);
			FindDupResult dup1 = FindDuplicateCards(wDuelTempList_ADDR);
			a = dup1.a;
			if (!(dup1.f & 0x10u)) {
				wce1a = dup1.a;
				FindAndRemoveCardFromList(dup1.a, wDuelTempList_ADDR);
				FindDupResult dup2 = FindDuplicateCards(wDuelTempList_ADDR);
				a = dup2.a;
				if (!(dup2.f & 0x10u)) {
					wce1b = dup2.a;
					return (AIDecide_ItemFinderResult){wce06, 0x10u};
				}
			}
		}
	}
	return (AIDecide_ItemFinderResult){a, (uint8_t)(a == 0u ? 0x80u : 0u)};
}
/* <<< factory AIDecide_ItemFinder */

/* >>> factory AIDecide_EnergyRetrieval */
AIDecideEnergyRetrievalResult AIDecide_EnergyRetrieval(uint8_t a)
{
	CoreCardListResult hand_energy = CreateEnergyCardListFromHand(a);
	if (!(hand_energy.f & 0x10u))
		return (AIDecideEnergyRetrievalResult){hand_energy.a, 0x00u};

	if (wOpponentDeckID == GO_GO_RAIN_DANCE_DECK_ID) {
		PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
		if (!(muk.f & 0x10u)) {
			PkmnPowerCountResult blastoise = CountTurnDuelistPokemonWithActivePkmnPower(BLASTOISE);
			if (!(blastoise.f & 0x10u))
				return (AIDecideEnergyRetrievalResult){blastoise.a, 0x00u};
		}
	}

	(void)CreateHandCardList(0u);
	FindDupResult dup = FindDuplicateCards(wDuelTempList_ADDR);
	if (dup.f & 0x10u)
		return (AIDecideEnergyRetrievalResult){dup.a, 0x00u};
	uint8_t saved_card = dup.a;

	FindBasicEnergyCardsInLocationResult discard = FindBasicEnergyCardsInLocation(CARD_LOCATION_DISCARD_PILE);
	if (discard.f & 0x10u)
		return (AIDecideEnergyRetrievalResult){discard.a, 0x00u};

	wce1a = 0xFFu;
	wce1b = 0xFFu;
	wce1c = 0xFFu;

	uint8_t d = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t e = PLAY_AREA_ARENA;
	while (d != 0u) {
		uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
		uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
		wTempCardID = card_id;
		LoadCardDataToBuffer1_FromCardID(card_id);
		wTempCardType = (uint8_t)(wLoadedCard1Type | TYPE_ENERGY);

		uint16_t hl = wDuelTempList_ADDR;
		for (;;) {
			uint8_t entry = gb_read8(hl);
			hl++;
			if (entry == 0xFFu)
				break;
			if (!(CheckIfEnergyIsUseful(entry).f & 0x10u))
				continue;
			if (wce1a != 0xFFu) {
				wce1b = entry;
				return (AIDecideEnergyRetrievalResult){saved_card, 0x10u};
			}
			wce1a = entry;
			RemoveCardFromList(&hl);
			break;
		}
		e++;
		d--;
	}

	uint16_t hl2 = wDuelTempList_ADDR;
	for (;;) {
		uint8_t entry = gb_read8(hl2);
		hl2++;
		if (entry == 0xFFu)
			break;
		if (wce1a != 0xFFu) {
			wce1b = entry;
			return (AIDecideEnergyRetrievalResult){saved_card, 0x10u};
		}
		wce1a = entry;
		RemoveCardFromList(&hl2);
	}

	if (wce1a != 0xFFu)
		return (AIDecideEnergyRetrievalResult){saved_card, 0x10u};
	return (AIDecideEnergyRetrievalResult){wce1a, 0x00u};
}
/* <<< factory AIDecide_EnergyRetrieval */

/* >>> factory AIDecide_SuperEnergyRetrieval */
AIDecideSuperEnergyRetrievalResult AIDecide_SuperEnergyRetrieval(uint8_t a)
{
	CoreCardListResult hand_energy = CreateEnergyCardListFromHand(a);
	if (!(hand_energy.f & 0x10u))
		return (AIDecideSuperEnergyRetrievalResult){hand_energy.a, 0x00u};

	if (wOpponentDeckID == GO_GO_RAIN_DANCE_DECK_ID) {
		PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
		if (!(muk.f & 0x10u)) {
			PkmnPowerCountResult blastoise = CountTurnDuelistPokemonWithActivePkmnPower(BLASTOISE);
			if (!(blastoise.f & 0x10u))
				return (AIDecideSuperEnergyRetrievalResult){blastoise.a, 0x00u};
		}
	}

	(void)CreateHandCardList(0u);
	FindDupResult dup1 = FindDuplicateCards(wDuelTempList_ADDR);
	if (dup1.f & 0x10u)
		return (AIDecideSuperEnergyRetrievalResult){dup1.a, 0x00u};
	wce06 = dup1.a;

	FindAndRemoveCardFromList(wce06, wDuelTempList_ADDR);
	FindDupResult dup2 = FindDuplicateCards(wDuelTempList_ADDR);
	if (dup2.f & 0x10u)
		return (AIDecideSuperEnergyRetrievalResult){dup2.a, 0x00u};
	wce08 = dup2.a;

	FindBasicEnergyCardsInLocationResult discard = FindBasicEnergyCardsInLocation(CARD_LOCATION_DISCARD_PILE);
	if (discard.f & 0x10u)
		return (AIDecideSuperEnergyRetrievalResult){discard.a, 0x00u};

	wce1b = 0xFFu;
	wce1c = 0xFFu;
	wce1d = 0xFFu;
	wce1e = 0xFFu;
	wce1f = 0xFFu;

	uint8_t d = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t e = PLAY_AREA_ARENA;
	while (d != 0u) {
		uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
		uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
		wTempCardID = card_id;
		LoadCardDataToBuffer1_FromCardID(card_id);
		wTempCardType = (uint8_t)(wLoadedCard1Type | TYPE_ENERGY);

		uint16_t hl = wDuelTempList_ADDR;
		for (;;) {
			uint8_t entry = gb_read8(hl);
			hl++;
			if (entry == 0xFFu)
				break;
			if (!(CheckIfEnergyIsUseful(entry).f & 0x10u))
				continue;
			if (wce1b == 0xFFu) {
				wce1b = entry;
				RemoveCardFromList(&hl);
			} else if (wce1c == 0xFFu) {
				wce1c = entry;
				RemoveCardFromList(&hl);
			} else if (wce1d == 0xFFu) {
				wce1d = entry;
				RemoveCardFromList(&hl);
			} else {
				wce1e = entry;
				wce1a = wce08;
				return (AIDecideSuperEnergyRetrievalResult){wce06, 0x10u};
			}
			break;
		}
		e++;
		d--;
	}

	uint16_t hl2 = wDuelTempList_ADDR;
	for (;;) {
		uint8_t entry = gb_read8(hl2);
		hl2++;
		if (entry == 0xFFu)
			break;
		if (wce1b == 0xFFu) {
			wce1b = entry;
			RemoveCardFromList(&hl2);
		} else if (wce1c == 0xFFu) {
			wce1c = entry;
			RemoveCardFromList(&hl2);
		} else if (wce1d == 0xFFu) {
			wce1d = entry;
			RemoveCardFromList(&hl2);
		} else {
			wce1e = entry;
			wce1a = wce08;
			return (AIDecideSuperEnergyRetrievalResult){wce06, 0x10u};
		}
	}

	if (wce1b != 0xFFu) {
		wce1a = wce08;
		return (AIDecideSuperEnergyRetrievalResult){wce06, 0x10u};
	}
	return (AIDecideSuperEnergyRetrievalResult){0xFFu, 0x00u};
}
/* <<< factory AIDecide_SuperEnergyRetrieval */

/* >>> factory AIDecide_PokemonBreeder */
AIDecidePokemonBreederResult AIDecide_PokemonBreeder(uint16_t hl_in)
{
	PrehistoricPowerResult power = IsPrehistoricPowerActive(hl_in);
	if (power.f & 0x10u)
		return (AIDecidePokemonBreederResult){power.a, power.f};

	ClearMemory_Bank8(7u, wce08_ADDR);
	wce06 = 0u;
	(void)CreateHandCardList(0u);
	uint16_t hl = wDuelTempList_ADDR;

	for (;;) {
		uint8_t deck_index = gb_read8(hl);
		hl++;
		if (deck_index == 0xFFu)
			break;

		uint8_t card_type = LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		if (card_type == VENUSAUR_LV64 || card_type == VENUSAUR_LV67 ||
		    card_type == BLASTOISE || card_type == VILEPLUME ||
		    card_type == ALAKAZAM || card_type == GENGAR) {
			uint8_t c = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
			uint8_t e = PLAY_AREA_ARENA;
			for (; c != 0u; c--, e++) {
				EvolveResult evolve = CheckIfCanEvolveInto_BasicToStage2(deck_index, e);
				if (evolve.f & 0x10u)
					continue;

				uint8_t damage = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + e)).a;
				uint8_t counters = ConvertHPToDamageCounters_Bank8(damage);
				uint8_t hi = (uint8_t)(((counters & 0x0Fu) << 4) | ((counters & 0xF0u) >> 4));
				(void)GetPlayAreaCardAttachedEnergies(e);
				uint8_t energies = wTotalAttachedEnergies;
				uint8_t lo = (energies >= 16u) ? 15u : energies;
				gb_write8((uint16_t)(wce08_ADDR + e), (uint8_t)(hi | lo));
				gb_write8((uint16_t)(wce0f_ADDR + e), deck_index);
				wce06++;
			}
		}
	}

	if (wce06 != 0u) {
		wce06 = 0u;
		uint8_t c = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		uint8_t e = PLAY_AREA_ARENA;
		uint8_t best_loc = 0u;
		for (; c != 0u; c--, e++) {
			uint8_t score = gb_read8((uint16_t)(wce08_ADDR + e));
			if (wce06 < score) {
				wce06 = score;
				best_loc = e;
			}
		}
		wce07 = best_loc;
		wce1a = gb_read8((uint16_t)(wce0f_ADDR + best_loc));
		return (AIDecidePokemonBreederResult){best_loc, 0x10u};
	}

	ClearMemory_Bank8(7u, wce08_ADDR);
	wce06 = 0u;
	(void)CreateHandCardList(0u);
	uint16_t hl2 = wDuelTempList_ADDR;

	for (;;) {
		uint8_t deck_index = gb_read8(hl2);
		hl2++;
		if (deck_index == 0xFFu)
			break;

		uint8_t c = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		uint8_t e = PLAY_AREA_ARENA;
		for (; c != 0u; c--, e++) {
			EvolveResult evolve = CheckIfCanEvolveInto_BasicToStage2(deck_index, e);
			if (evolve.f & 0x10u)
				continue;

			uint8_t evolving_id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
			uint8_t dragonite_carry = 0u;
			if (evolving_id == DRAGONITE_LV41) {
				if (e == 0u) {
					uint8_t hp = GetCardDamageAndMaxHP(PLAY_AREA_ARENA).a;
					uint8_t counters = ConvertHPToDamageCounters_Bank8(hp);
					CountNumberOfEnergyCardsAttachedResult energy =
						CountNumberOfEnergyCardsAttached(PLAY_AREA_ARENA);
					if (counters >= 5u || energy.a < 3u)
						dragonite_carry = 1u;
				} else {
					uint8_t total_count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
					uint8_t sum = 0u;
					uint8_t loc = total_count;
					while (loc != 0u) {
						loc--;
						uint8_t hp = GetCardDamageAndMaxHP(loc).a;
						sum = (uint8_t)(sum + ConvertHPToDamageCounters_Bank8(hp));
					}
					if (sum < 8u)
						dragonite_carry = 1u;
				}
			}
			if (dragonite_carry)
				continue;

			uint8_t damage = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + e)).a;
			uint8_t counters2 = ConvertHPToDamageCounters_Bank8(damage);
			uint8_t hi = (uint8_t)(((counters2 & 0x0Fu) << 4) | ((counters2 & 0xF0u) >> 4));
			(void)GetPlayAreaCardAttachedEnergies(e);
			uint8_t energies = wTotalAttachedEnergies;
			uint8_t lo = (energies >= 16u) ? 15u : energies;
			gb_write8((uint16_t)(wce08_ADDR + e), (uint8_t)(hi | lo));
			gb_write8((uint16_t)(wce0f_ADDR + e), deck_index);
			wce06++;
		}
	}

	if (wce06 == 0u)
		return (AIDecidePokemonBreederResult){0u, 0x80u};

	wce06 = 0u;
	wce07 = 0xFFu;
	{
		uint8_t c = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		uint8_t e = PLAY_AREA_ARENA;
		for (; c != 0u; c--, e++) {
			uint8_t score = gb_read8((uint16_t)(wce08_ADDR + e));
			if (wce06 < score) {
				uint8_t energy_count = (uint8_t)(score & 0x0Fu);
				if (energy_count >= 2u) {
					wce06 = score;
					wce07 = e;
				}
			}
		}
	}

	if (wce07 == 0xFFu)
		return (AIDecidePokemonBreederResult){0xFFu, 0x00u};

	wce1a = gb_read8((uint16_t)(wce0f_ADDR + wce07));
	return (AIDecidePokemonBreederResult){wce07, 0x10u};
}
/* <<< factory AIDecide_PokemonBreeder */

/* >>> factory AIDecide_PokemonTrader_LegendaryMoltres */
AIDecide_PokemonTrader_LegendaryMoltresResult AIDecide_PokemonTrader_LegendaryMoltres(void)
{
	LookForCardIDToTradeWithDifferentHandCardResult r = LookForCardIDToTradeWithDifferentHandCard(MOLTRES_LV37, MOLTRES_LV35);
	if (!(r.f & 0x10u)) {
		uint8_t f = (r.a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryMoltresResult){r.a, f};
	}
	wce1a = r.a;
	return (AIDecide_PokemonTrader_LegendaryMoltresResult){r.e, 0x10u};
}
/* <<< factory AIDecide_PokemonTrader_LegendaryMoltres */

/* >>> factory AIDecide_PokemonTrader_StrangePower */
AIDecide_PokemonTrader_StrangePowerResult AIDecide_PokemonTrader_StrangePower(void)
{
	LookForCardIDToTradeWithDifferentHandCardResult r = LookForCardIDToTradeWithDifferentHandCard(MR_MIME, MR_MIME);
	if (!(r.f & 0x10u)) {
		uint8_t f = (r.a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_StrangePowerResult){r.a, f};
	}
	wce1a = r.a;
	return (AIDecide_PokemonTrader_StrangePowerResult){r.e, 0x10u};
}
/* <<< factory AIDecide_PokemonTrader_StrangePower */

/* >>> factory AIDecide_PokemonTrader_LegendaryArticuno */
AIDecide_PokemonTrader_LegendaryArticunoResult AIDecide_PokemonTrader_LegendaryArticuno(void)
{
	LookForCardIDInHandAndPlayAreaResult r = LookForCardIDInHandAndPlayArea(ARTICUNO_LV35);
	if (r.f & 0x10u) {
		uint8_t f = (r.a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){r.a, f};
	}
	r = LookForCardIDInHandAndPlayArea(LAPRAS);
	if (r.f & 0x10u) {
		uint8_t f = (r.a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){r.a, f};
	}
	r = LookForCardIDInHandAndPlayArea(SEEL);
	uint8_t found_in_deck = 0u;
	if (!(r.f & 0x10u)) {
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, SEEL);
		if (loc.f & 0x10u) {
			wce1a = loc.a;
			found_in_deck = 1u;
		}
	}
	if (!found_in_deck) {
		r = LookForCardIDInHandAndPlayArea(DEWGONG);
		if (r.f & 0x10u) {
			uint8_t f = (r.a == 0u) ? 0x80u : 0u;
			return (AIDecide_PokemonTrader_LegendaryArticunoResult){r.a, f};
		}
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, DEWGONG);
		if (!(loc.f & 0x10u)) {
			uint8_t f = (loc.a == 0u) ? 0x80u : 0u;
			return (AIDecide_PokemonTrader_LegendaryArticunoResult){loc.a, f};
		}
		wce1a = loc.a;
	}
	CheckIfHasCardIDInHandResult h = CheckIfHasCardIDInHand(CHANSEY);
	if (h.f & 0x10u)
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, 0x10u};
	h = CheckIfHasCardIDInHand(DITTO);
	if (h.f & 0x10u)
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, 0x10u};
	h = CheckIfHasCardIDInHand(ARTICUNO_LV37);
	if (h.f & 0x10u)
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, 0x10u};
	uint8_t f = (h.a == 0u) ? 0x80u : 0u;
	return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, f};
}
/* <<< factory AIDecide_PokemonTrader_LegendaryArticuno */

/* >>> factory AIDecide_ComputerSearch_FireCharge */
AIDecide_ComputerSearch_FireChargeResult AIDecide_ComputerSearch_FireCharge(uint8_t b, uint8_t c)
{
	uint8_t target;
	LookForCardIDInHandListResult h = LookForCardIDInHandList_Bank8(CHANSEY);
	if (!(h.f & 0x10u)) {
		target = CHANSEY;
	} else {
		h = LookForCardIDInHandList_Bank8(TAUROS);
		if (!(h.f & 0x10u)) {
			target = TAUROS;
		} else {
			h = LookForCardIDInHandList_Bank8(JIGGLYPUFF_LV12);
			if (!(h.f & 0x10u)) {
				target = JIGGLYPUFF_LV12;
			} else {
				uint8_t f = (h.a == 0u) ? 0x80u : 0u;
				return (AIDecide_ComputerSearch_FireChargeResult){h.a, f};
			}
		}
	}

	LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, target);
	if (!(loc.f & 0x10u)) {
		uint8_t f = (loc.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_FireChargeResult){loc.a, f};
	}
	wce06 = loc.a;

	(void)CreateHandCardList(0u);
	uint8_t trainer_to_play = wAITrainerCardToPlay;
	RemoveFromListDifferentCardOfGivenTypeResult r1 =
		RemoveFromListDifferentCardOfGivenType(b, c, 0u, trainer_to_play, wDuelTempList_ADDR);
	if (!(r1.f & 0x10u)) {
		uint8_t f = (r1.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_FireChargeResult){r1.a, f};
	}
	wce1a = r1.a;
	RemoveFromListDifferentCardOfGivenTypeResult r2 =
		RemoveFromListDifferentCardOfGivenType(r1.b, r1.c, r1.d, r1.e, r1.hl);
	if (!(r2.f & 0x10u)) {
		uint8_t f = (r2.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_FireChargeResult){r2.a, f};
	}
	wce1b = r2.a;
	return (AIDecide_ComputerSearch_FireChargeResult){wce06, 0x90u};
}
/* <<< factory AIDecide_ComputerSearch_FireCharge */

/* >>> factory AIDecide_ComputerSearch_Anger */
AIDecide_ComputerSearch_AngerResult AIDecide_ComputerSearch_Anger(uint8_t b, uint8_t c)
{
	uint8_t a_val;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
	LookForCardIDInDeck_GivenCardIDInHandResult r2;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(RATICATE, RATTATA);
	a_val = r.a;
	if (r.f & 0x10u) goto find_discard_cards;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(RATTATA, RATICATE);
	a_val = r2.a;
	if (r2.f & 0x10u) goto find_discard_cards;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(ARCANINE_LV34, GROWLITHE);
	a_val = r.a;
	if (r.f & 0x10u) goto find_discard_cards;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(GROWLITHE, ARCANINE_LV34);
	a_val = r2.a;
	if (r2.f & 0x10u) goto find_discard_cards;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DODRIO, DODUO);
	a_val = r.a;
	if (r.f & 0x10u) goto find_discard_cards;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(DODUO, DODRIO);
	a_val = r2.a;
	if (r2.f & 0x10u) goto find_discard_cards;

	{
		uint8_t f = (a_val == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_AngerResult){a_val, f};
	}

find_discard_cards:
	wce06 = a_val;
	(void)CreateHandCardList(0u);
	uint8_t trainer_to_play = wAITrainerCardToPlay;
	RemoveFromListDifferentCardOfGivenTypeResult rm1 =
		RemoveFromListDifferentCardOfGivenType(b, c, 0u, trainer_to_play, wDuelTempList_ADDR);
	if (!(rm1.f & 0x10u)) {
		uint8_t f = (rm1.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_AngerResult){rm1.a, f};
	}
	wce1a = rm1.a;
	RemoveFromListDifferentCardOfGivenTypeResult rm2 =
		RemoveFromListDifferentCardOfGivenType(rm1.b, rm1.c, rm1.d, rm1.e, rm1.hl);
	if (!(rm2.f & 0x10u)) {
		uint8_t f = (rm2.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_AngerResult){rm2.a, f};
	}
	wce1b = rm2.a;
	return (AIDecide_ComputerSearch_AngerResult){wce06, 0x90u};
}
/* <<< factory AIDecide_ComputerSearch_Anger */

/* >>> factory AIDecide_ComputerSearch_WondersOfScience */
AIDecide_ComputerSearch_WondersOfScienceResult AIDecide_ComputerSearch_WondersOfScience(uint8_t b, uint8_t c)
{
	uint8_t a_val;
	DuelistVarResult hand_count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (hand_count.a < 5u) {
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PROFESSOR_OAK);
		a_val = loc.a;
		if (loc.f & 0x10u) goto find_discard_cards;
	}

	{
		LookForCardIDInHandListResult h = LookForCardIDInHandList_Bank8(GRIMER);
		if (!(h.f & 0x10u)) {
			LookForCardIDInLocationBank8Result loc2 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, GRIMER);
			a_val = loc2.a;
			if (loc2.f & 0x10u) goto find_discard_cards;
			goto no_carry;
		}
		h = LookForCardIDInHandList_Bank8(MUK);
		if (!(h.f & 0x10u)) {
			LookForCardIDInLocationBank8Result loc3 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, MUK);
			a_val = loc3.a;
			if (loc3.f & 0x10u) goto find_discard_cards;
			goto no_carry;
		}
		a_val = h.a;
	}

no_carry: ;
	{
		uint8_t f = (a_val == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_WondersOfScienceResult){a_val, f};
	}

find_discard_cards:
	wce06 = a_val;
	(void)CreateHandCardList(0u);
	uint8_t trainer_to_play = wAITrainerCardToPlay;
	RemoveFromListDifferentCardOfGivenTypeResult rm1 =
		RemoveFromListDifferentCardOfGivenType(b, c, 0u, trainer_to_play, wDuelTempList_ADDR);
	if (!(rm1.f & 0x10u)) {
		uint8_t f = (rm1.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_WondersOfScienceResult){rm1.a, f};
	}
	wce1a = rm1.a;
	RemoveFromListDifferentCardOfGivenTypeResult rm2 =
		RemoveFromListDifferentCardOfGivenType(rm1.b, rm1.c, rm1.d, rm1.e, rm1.hl);
	if (!(rm2.f & 0x10u)) {
		uint8_t f = (rm2.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_WondersOfScienceResult){rm2.a, f};
	}
	wce1b = rm2.a;
	return (AIDecide_ComputerSearch_WondersOfScienceResult){wce06, 0x90u};
}
/* <<< factory AIDecide_ComputerSearch_WondersOfScience */

/* >>> factory AIDecide_ComputerSearch_RockCrusher */
AIDecide_ComputerSearch_RockCrusherResult AIDecide_ComputerSearch_RockCrusher(uint8_t b, uint8_t c)
{
	uint8_t final_a;
	DuelistVarResult hand_count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (hand_count.a == 3u) {
		LookForCardIDInLocationBank8Result oak = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PROFESSOR_OAK);
		if (!(oak.f & 0x10u)) {
			final_a = oak.a;
			goto no_carry;
		}
		wce06 = oak.a;
		wce1a = 0xFFu;
		wce1b = 0xFFu;
		(void)CreateHandCardList(c);
		uint16_t scan = wDuelTempList_ADDR;
		uint16_t store = wce1a_ADDR;
		uint8_t trainer_to_play = wAITrainerCardToPlay;
		for (;;) {
			uint8_t idx = gb_read8(scan);
			scan = (uint16_t)(scan + 1u);
			if (idx == 0xFFu)
				break;
			uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(idx);
			if (card_id == PROFESSOR_OAK || card_id == FIGHTING_ENERGY ||
			    card_id == DOUBLE_COLORLESS_ENERGY || card_id == DIGLETT ||
			    card_id == GEODUDE || card_id == ONIX || card_id == RHYHORN) {
				final_a = card_id;
				goto no_carry;
			}
			if (card_id == trainer_to_play)
				continue;
			gb_write8(store, idx);
			store = (uint16_t)(store + 1u);
		}
		if (gb_read8(wce1b_ADDR) != 0xFFu)
			return (AIDecide_ComputerSearch_RockCrusherResult){wce06, 0x10u};
		final_a = 0xFFu;
		goto no_carry;
	}

	{
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, GRAVELER);
		if (loc.f & 0x10u) {
			wce06 = loc.a;
			LookForCardIDInHandAndPlayAreaResult geo = LookForCardIDInHandAndPlayArea(GEODUDE);
			if (geo.f & 0x10u) {
				LookForCardIDInHandListResult grav_hand = LookForCardIDInHandList_Bank8(GRAVELER);
				if (!(grav_hand.f & 0x10u)) {
					(void)CreateHandCardList(c);
					uint16_t hl = wDuelTempList_ADDR;
					(void)RemoveCardIDInList(&hl, GEODUDE);
					goto find_discard_cards_2;
				}
			}
		}
	}

	{
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, GOLEM);
		if (loc.f & 0x10u) {
			wce06 = loc.a;
			LookForCardIDInPlayAreaResult grav_pa = LookForCardIDInPlayArea_Bank8(GRAVELER, b);
			if (grav_pa.f & 0x10u) {
				LookForCardIDInHandListResult golem_hand = LookForCardIDInHandList_Bank8(GOLEM);
				if (!(golem_hand.f & 0x10u)) {
					(void)CreateHandCardList(c);
					goto find_discard_cards_2;
				}
			}
		}
	}

	{
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, DUGTRIO);
		if (!(loc.f & 0x10u)) {
			final_a = loc.a;
			goto no_carry;
		}
		wce06 = loc.a;
		LookForCardIDInPlayAreaResult dig_pa = LookForCardIDInPlayArea_Bank8(DIGLETT, b);
		if (!(dig_pa.f & 0x10u)) {
			final_a = dig_pa.a;
			goto no_carry;
		}
		LookForCardIDInHandListResult dug_hand = LookForCardIDInHandList_Bank8(DUGTRIO);
		if (dug_hand.f & 0x10u) {
			final_a = dug_hand.a;
			goto no_carry;
		}
		(void)CreateHandCardList(c);
		goto find_discard_cards_2;
	}

no_carry: ;
	{
		uint8_t f = (final_a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_RockCrusherResult){final_a, f};
	}

find_discard_cards_2:
	wce1a = 0xFFu;
	wce1b = 0xFFu;
	{
		uint16_t bc_ptr = wce1a_ADDR;
		uint8_t d = 0u;
		uint8_t trainer_to_play2 = wAITrainerCardToPlay;
		for (;;) {
			RemoveFromListDifferentCardOfGivenTypeResult r =
				RemoveFromListDifferentCardOfGivenType(b, c, d, trainer_to_play2, wDuelTempList_ADDR);
			if (r.f & 0x10u) {
				gb_write8(bc_ptr, r.a);
				bc_ptr = (uint16_t)(bc_ptr + 1u);
				if (gb_read8(wce1b_ADDR) != 0xFFu)
					return (AIDecide_ComputerSearch_RockCrusherResult){wce06, 0x10u};
				continue;
			}
			d = (uint8_t)(d + 1u);
			if (d == 3u) {
				final_a = r.a;
				goto no_carry;
			}
		}
	}
}
/* <<< factory AIDecide_ComputerSearch_RockCrusher */

/* >>> factory AIDecide_ComputerSearch */
AIDecide_ComputerSearchResult AIDecide_ComputerSearch(uint8_t b, uint8_t c)
{
	DuelistVarResult hand_count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (hand_count.a < 3u) {
		uint8_t f = (hand_count.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearchResult){hand_count.a, f};
	}
	uint8_t deck_id = wOpponentDeckID;
	if (deck_id == ROCK_CRUSHER_DECK_ID) {
		AIDecide_ComputerSearch_RockCrusherResult r = AIDecide_ComputerSearch_RockCrusher(b, c);
		return (AIDecide_ComputerSearchResult){r.a, r.f};
	}
	if (deck_id == WONDERS_OF_SCIENCE_DECK_ID) {
		AIDecide_ComputerSearch_WondersOfScienceResult r = AIDecide_ComputerSearch_WondersOfScience(b, c);
		return (AIDecide_ComputerSearchResult){r.a, r.f};
	}
	if (deck_id == FIRE_CHARGE_DECK_ID) {
		AIDecide_ComputerSearch_FireChargeResult r = AIDecide_ComputerSearch_FireCharge(b, c);
		return (AIDecide_ComputerSearchResult){r.a, r.f};
	}
	if (deck_id == ANGER_DECK_ID) {
		AIDecide_ComputerSearch_AngerResult r = AIDecide_ComputerSearch_Anger(b, c);
		return (AIDecide_ComputerSearchResult){r.a, r.f};
	}
	uint8_t f = (deck_id == 0u) ? 0x80u : 0u;
	return (AIDecide_ComputerSearchResult){deck_id, f};
}
/* <<< factory AIDecide_ComputerSearch */

/* >>> factory AIDecide_PokemonTrader_LegendaryRonald */
AIDecide_PokemonTrader_LegendaryRonaldResult AIDecide_PokemonTrader_LegendaryRonald(void)
{
	uint8_t target_a;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
	LookForCardIDInDeck_GivenCardIDInHandResult r2;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(FLAREON_LV22, EEVEE);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(VAPOREON_LV29, EEVEE);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(JOLTEON_LV24, EEVEE);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(EEVEE, FLAREON_LV22);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(EEVEE, VAPOREON_LV29);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(EEVEE, JOLTEON_LV24);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DRAGONAIR, DRATINI);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DRAGONITE_LV41, DRAGONAIR);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(DRATINI, DRAGONAIR);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(DRAGONAIR, DRAGONITE_LV41);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	goto no_carry;

choose_hand: ;
	wce1a = target_a;
	{
		LookForCardIDInHandListResult h = LookForCardIDInHandList_Bank8(ZAPDOS_LV68);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryRonaldResult){h.a, 0x90u};
		h = LookForCardIDInHandList_Bank8(ARTICUNO_LV37);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryRonaldResult){h.a, 0x90u};
		h = LookForCardIDInHandList_Bank8(MOLTRES_LV37);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryRonaldResult){h.a, 0x90u};
		target_a = h.a;
	}

no_carry: ;
	{
		uint8_t f = (target_a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryRonaldResult){target_a, f};
	}
}
/* <<< factory AIDecide_PokemonTrader_LegendaryRonald */
