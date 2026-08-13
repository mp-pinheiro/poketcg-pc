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
	uint8_t flag = CheckLoadedAttackFlag(0x00u).f;
	if (!(flag & 0x10u))
		flag = CheckLoadedAttackFlag(0x01u).f;
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
