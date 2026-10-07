/* >>> part includes_2 */
#include "home/card_id_bus.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/duel.h"
#include "mem.h"
#include "home/random.h"

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
/* <<< part includes_2 */
/* >>> factory FindDuplicateCards */
/* trainer_cards.asm:2788-2859 */
FindDupResult FindDuplicateCards(uint16_t hl, uint8_t d)
{
	wce0f = 0xFFu;
	gb_write8((uint16_t)(wce0f_ADDR + 1u), 0xFFu);
	uint16_t outer = hl;
	for (;;) {
		uint8_t idx = gb_read8(outer);
		outer = (uint16_t)(outer + 1u);
		if (idx == 0xFFu)
			break;
		CardId b = GetCardIDFromDeckIndex(idx);
		d = (uint8_t)(b >> 8);
		uint16_t inner = outer;
		for (;;) {
			uint8_t c = gb_read8(inner);
			inner = (uint16_t)(inner + 1u);
			if (c == 0xFFu)
				break;
			CardId current = GetCardIDFromDeckIndex(c);
			d = (uint8_t)(current >> 8);
			if (current != b)
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
		return (FindDupResult){0xFFu, 0x90u, outer, d};
	uint8_t a = (lo != 0xFFu) ? lo : hi;
	return (FindDupResult){a, (uint8_t)(a == 0u ? 0x80u : 0x00u), outer, d};
}
/* <<< factory FindDuplicateCards */
/* >>> factory AIDecide_Maintenance */
AIDecideMaintenanceResult AIDecide_Maintenance(uint8_t d)
{
	DuelistVarResult hand = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (wOpponentDeckID == IMAKUNI_DECK_ID) {
		/* trainer_cards.asm:4204-4246 `.imakuni`: every `.no_carry` exit is
		 * `or a` on the value in hand -- the roll, the hand count or the
		 * list's $ff -- and the found-two exit is `scf` after `dec c`. */
		uint8_t roll = Random(10u);
		if (roll >= 2u)
			return (AIDecideMaintenanceResult){roll, 0x00u, d};
		hand = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
		if (hand.a < 3u)
			return (AIDecideMaintenanceResult){hand.a,
				(uint8_t)(hand.a == 0u ? 0x80u : 0u), d};
		(void)CreateHandCardList(0);
		TempListResult count = CountCardsInDuelTempList();
		(void)ShuffleCards(count.a, wDuelTempList_ADDR);
		uint16_t p = wDuelTempList_ADDR;
		/* trainer_cards.asm:4232-4245: a is the hand card just read - the
		 * $ff terminator on the refusal, the second chosen card on the carry
		 * exit, which the caller stores as wAITrainerCardParameter. */
		uint8_t target = wAITrainerCardToPlay, found = 0, out = 0, card = 0;
		while (found < 2u) {
			card = gb_read8(p++);
			if (card == 0xFFu)
				return (AIDecideMaintenanceResult){card, 0x00u,
					(uint8_t)(wce1a_ADDR >> 8)};
			if (card == target)
				continue;
			gb_write8((uint16_t)(wce1a_ADDR + out++), card);
			found++;
		}
		/* `dec c` reached zero and `scf` keeps its Z: Z|C. */
		return (AIDecideMaintenanceResult){card, 0x90u,
			(uint8_t)(wce1a_ADDR >> 8)};
	}
	if (hand.a < 4u)
		return (AIDecideMaintenanceResult){hand.a,
			(uint8_t)(hand.a == 0u ? 0x80u : 0u), d};
	(void)CreateHandCardList(0);
	FindAndRemoveCardFromList(wAITrainerCardToPlay, wDuelTempList_ADDR);
	FindDupResult first = FindDuplicateCards(wDuelTempList_ADDR, 0xC5u);
	if (first.a == 0xFFu)
		return (AIDecideMaintenanceResult){first.a, 0x00u, first.d};
	wce1a = first.a;
	FindAndRemoveCardFromList(first.a, wDuelTempList_ADDR);
	FindDupResult second = FindDuplicateCards(wDuelTempList_ADDR, first.d);
	if (second.a == 0xFFu)
		return (AIDecideMaintenanceResult){second.a, 0x00u, second.d};
	wce1b = second.a;
	return (AIDecideMaintenanceResult){second.a, 0x10u, second.d};
}
/* <<< factory AIDecide_Maintenance */
/* >>> factory AIDecide_ClefairyDollOrMysteriousFossil */
/* trainer_cards.asm:4784-4812. The play area count is parked in wce06 for
 * the later phases; a Wigglytuff in the arena plays the card outright, with
 * `cp WIGGLYTUFF`'s Z under the carry. */
AIDecidePokemonFluteResult AIDecide_ClefairyDollOrMysteriousFossil(uint8_t d)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	if (count >= MAX_PLAY_AREA_POKEMON)
		return (AIDecidePokemonFluteResult){count, count == 0u ? 0x80u : 0u, d};
	wce06 = count;
	CardId arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	CardId card_id = GetCardIDFromDeckIndex((uint8_t)arena);
	if (card_id == WIGGLYTUFF)
		return (AIDecidePokemonFluteResult){(uint8_t)card_id, 0x90u, 0u};
	if (count < 4u)
		return (AIDecidePokemonFluteResult){count, 0x10u, 0u};
	return (AIDecidePokemonFluteResult){count, count == 0u ? 0x80u : 0u, 0u};
}
/* <<< factory AIDecide_ClefairyDollOrMysteriousFossil */
/* --- factory AIDecide_Defender_Phase14 */
/* >>> factory AIDecide_Revive */
AIDecideReviveResult AIDecide_Revive(uint8_t d)
{
	CardListResult discard = CreateDiscardPileCardList(0u);
	if (discard.f & 0x10u)
		return (AIDecideReviveResult){discard.a, 0x80u, discard.d};
	if (GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a >= 4u)
		return (AIDecideReviveResult){GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a,
			0u, discard.d};
	uint16_t p = wDuelTempList_ADDR;
	for (;;) {
		uint8_t index = gb_read8(p++);
		if (index == 0xFFu)
			return (AIDecideReviveResult){0xFFu, 0u, d};
		(void)LoadCardDataToBuffer1_FromDeckIndex(index);
		CardId card_id = card_id_read_at(wLoadedCard1ID_ADDR);
		d = (uint8_t)(card_id >> 8);
		if (card_id == HITMONCHAN || card_id == HITMONLEE ||
		    card_id == TAUROS || card_id == KANGASKHAN)
			return (AIDecideReviveResult){index, 0x90u, d};
	}
}
/* <<< factory AIDecide_Revive */
/* --- factory PickPokedexCards_Unreferenced */
/* >>> factory AIDecide_Pokedex */
static PickPokedexResult pick_pokedex_pokemon_first(void)
{
	DuelistVarResult remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	uint16_t deck = (uint16_t)((remaining.hl & 0xFF00u) |
				   (uint8_t)(remaining.a + 0x7Eu));
	uint8_t types[5], indices[5];
	wAIPokedexCounter = 0;
	for (uint8_t i = 0; i < 5u; i++) {
		indices[i] = gb_read8((uint16_t)(deck + i));
		types[i] = GetCardType(GetCardIDFromDeckIndex(indices[i]));
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
	return (PickPokedexResult){0xFFu, 0x90u, (uint8_t)((wce1a_ADDR + out) >> 8)};
}

AIDecidePokedexResult AIDecide_Pokedex(uint8_t d)
{
	uint8_t counter = wAIPokedexCounter;
	if (counter < 6u)
		return (AIDecidePokedexResult){counter, (uint8_t)(counter == 0u ? 0x80u : 0u), d};
	DuelistVarResult notindeck = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	if (notindeck.a >= (DECK_SIZE - 4u))
		return (AIDecidePokedexResult){notindeck.a, (uint8_t)(notindeck.a == 0u ? 0x80u : 0u), d};
	uint8_t roll = Random(10u);
	if (roll >= 3u)
		return (AIDecidePokedexResult){roll, (uint8_t)(roll == 0u ? 0x80u : 0u), d};
	PickPokedexResult picked = wOpponentDeckID == WONDERS_OF_SCIENCE_DECK_ID
		? pick_pokedex_pokemon_first() : PickPokedexCards();
	return (AIDecidePokedexResult){picked.a, picked.f, picked.d};
}
/* <<< factory AIDecide_Pokedex */
/* >>> factory AIDecide_ItemFinder */
AIDecide_ItemFinderResult AIDecide_ItemFinder(uint8_t d)
{
	CardListResult discard = CreateDiscardPileCardList(0u);
	uint8_t a = discard.a;
	d = discard.d;
	if (!(discard.f & 0x10u)) {
		uint16_t hl = wDuelTempList_ADDR;
		uint8_t deck_index = 0u;
		uint8_t found = 0u;
		for (;;) {
			deck_index = gb_read8(hl++);
			if (deck_index == 0xFFu) {
				a = 0xFFu;
				break;
			}
			(void)LoadCardDataToBuffer1_FromDeckIndex(deck_index);
			CardId card_id = card_id_read_at(wLoadedCard1ID_ADDR);
			d = (uint8_t)(card_id >> 8);
			if (card_id == ENERGY_REMOVAL) {
				found = 1u;
				break;
			}
		}
		if (found) {
			wce06 = deck_index;

			HandListResult hand = CreateHandCardList(0u);
			d = hand.d;
			hl = wDuelTempList_ADDR;
			for (;;) {
				uint8_t v = gb_read8(hl);
				hl++;
				if (v == 0xFFu)
					break;
				(void)LoadCardDataToBuffer1_FromDeckIndex(v);
				CardId card_id = card_id_read_at(wLoadedCard1ID_ADDR);
				d = (uint8_t)(card_id >> 8);
				if (card_id == MR_MIME || card_id == POKEMON_TRADER)
					RemoveCardFromList(&hl);
			}

			FindAndRemoveCardFromList(wAITrainerCardToPlay, wDuelTempList_ADDR);
			FindDupResult dup1 = FindDuplicateCards(wDuelTempList_ADDR, d);
			a = dup1.a;
			d = dup1.d;
			if (!(dup1.f & 0x10u)) {
				wce1a = dup1.a;
				FindAndRemoveCardFromList(dup1.a, wDuelTempList_ADDR);
				FindDupResult dup2 = FindDuplicateCards(wDuelTempList_ADDR, d);
				a = dup2.a;
				d = dup2.d;
				if (!(dup2.f & 0x10u)) {
					wce1b = dup2.a;
					return (AIDecide_ItemFinderResult){wce06, 0x10u, d};
				}
			}
		}
	}
	return (AIDecide_ItemFinderResult){a, (uint8_t)(a == 0u ? 0x80u : 0u), d};
}
/* <<< factory AIDecide_ItemFinder */
/* >>> factory AIDecide_EnergyRetrieval */
AIDecideEnergyRetrievalResult AIDecide_EnergyRetrieval(uint8_t a, uint8_t d)
{
	CoreCardListResult hand_energy = CreateEnergyCardListFromHand(a);
	if (!(hand_energy.f & 0x10u))
		return (AIDecideEnergyRetrievalResult){hand_energy.a, (uint8_t)(hand_energy.a == 0u ? 0x80u : 0u), d};

	if (wOpponentDeckID == GO_GO_RAIN_DANCE_DECK_ID) {
		PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
		if (!(muk.f & 0x10u)) {
			PkmnPowerCountResult blastoise = CountTurnDuelistPokemonWithActivePkmnPower(BLASTOISE);
			if (!(blastoise.f & 0x10u))
				return (AIDecideEnergyRetrievalResult){blastoise.a, (uint8_t)(blastoise.a == 0u ? 0x80u : 0u), d};
		}
	}

	/* CreateHandCardList leaves de on wDuelTempList's page. */
	d = CreateHandCardList(0u).d;
	FindDupResult dup = FindDuplicateCards(wDuelTempList_ADDR, d);
	d = dup.d;
	if (dup.f & 0x10u)
		return (AIDecideEnergyRetrievalResult){dup.a, (uint8_t)(dup.a == 0u ? 0x80u : 0u), d};
	/* trainer_cards.asm:2649: the duplicate goes to wce06 before the discard
	 * pile is searched, so a refusal there still leaves it written, and
	 * `.set_carry` reads it back from there. */
	wce06 = dup.a;

	FindBasicEnergyCardsInLocationResult discard = FindBasicEnergyCardsInLocation(CARD_LOCATION_DISCARD_PILE);
	d = discard.d;
	if (discard.f & 0x10u)
		return (AIDecideEnergyRetrievalResult){discard.a, (uint8_t)(discard.a == 0u ? 0x80u : 0u), d};

	wce1a = 0xFFu;
	wce1b = 0xFFu;
	wce1c = 0xFFu;

	d = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t e = PLAY_AREA_ARENA;
	while (d != 0u) {
		uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
		CardId card_id = GetCardIDFromDeckIndex(deck_index);
		uint16_t temp_card_id = wTempCardID_ADDR;
		card_id_write(&temp_card_id, card_id);
		LoadCardDataToBuffer1_FromCardID(card_id);

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
				return (AIDecideEnergyRetrievalResult){wce06, 0x10u, d};
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
			return (AIDecideEnergyRetrievalResult){wce06, 0x10u, d};
		}
		wce1a = entry;
		RemoveCardFromList(&hl2);
	}

	if (wce1a != 0xFFu)
		return (AIDecideEnergyRetrievalResult){wce06, 0x10u, d};
	return (AIDecideEnergyRetrievalResult){wce1a, (uint8_t)(wce1a == 0u ? 0x80u : 0u), d};
}
/* <<< factory AIDecide_EnergyRetrieval */
/* >>> factory AIDecide_SuperEnergyRetrieval */
AIDecideSuperEnergyRetrievalResult AIDecide_SuperEnergyRetrieval(uint8_t a, uint8_t d)
{
	CoreCardListResult hand_energy = CreateEnergyCardListFromHand(a);
	if (!(hand_energy.f & 0x10u))
		return (AIDecideSuperEnergyRetrievalResult){hand_energy.a, (uint8_t)(hand_energy.a == 0u ? 0x80u : 0u), d};

	if (wOpponentDeckID == GO_GO_RAIN_DANCE_DECK_ID) {
		PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
		if (!(muk.f & 0x10u)) {
			PkmnPowerCountResult blastoise = CountTurnDuelistPokemonWithActivePkmnPower(BLASTOISE);
			if (!(blastoise.f & 0x10u))
				return (AIDecideSuperEnergyRetrievalResult){blastoise.a, (uint8_t)(blastoise.a == 0u ? 0x80u : 0u), d};
		}
	}

	/* CreateHandCardList leaves de on wDuelTempList's page. */
	d = CreateHandCardList(0u).d;
	FindDupResult dup1 = FindDuplicateCards(wDuelTempList_ADDR, d);
	d = dup1.d;
	if (dup1.f & 0x10u)
		return (AIDecideSuperEnergyRetrievalResult){dup1.a, (uint8_t)(dup1.a == 0u ? 0x80u : 0u), d};
	wce06 = dup1.a;

	FindAndRemoveCardFromList(wce06, wDuelTempList_ADDR);
	FindDupResult dup2 = FindDuplicateCards(wDuelTempList_ADDR, d);
	d = dup2.d;
	if (dup2.f & 0x10u)
		return (AIDecideSuperEnergyRetrievalResult){dup2.a, (uint8_t)(dup2.a == 0u ? 0x80u : 0u), d};
	wce08 = dup2.a;

	FindBasicEnergyCardsInLocationResult discard = FindBasicEnergyCardsInLocation(CARD_LOCATION_DISCARD_PILE);
	d = discard.d;
	if (discard.f & 0x10u)
		return (AIDecideSuperEnergyRetrievalResult){discard.a, (uint8_t)(discard.a == 0u ? 0x80u : 0u), d};

	wce1b = 0xFFu;
	wce1c = 0xFFu;
	wce1d = 0xFFu;
	wce1e = 0xFFu;
	wce1f = 0xFFu;

	d = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t e = PLAY_AREA_ARENA;
	while (d != 0u) {
		uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
		CardId card_id = GetCardIDFromDeckIndex(deck_index);
		uint16_t temp_card_id = wTempCardID_ADDR;
		card_id_write(&temp_card_id, card_id);
		LoadCardDataToBuffer1_FromCardID(card_id);

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
				return (AIDecideSuperEnergyRetrievalResult){wce06, 0x10u, d};
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
			return (AIDecideSuperEnergyRetrievalResult){wce06, 0x10u, d};
		}
	}

	if (wce1b != 0xFFu) {
		wce1a = wce08;
		return (AIDecideSuperEnergyRetrievalResult){wce06, 0x10u, d};
	}
	return (AIDecideSuperEnergyRetrievalResult){0xFFu, 0x00u, d};
}
/* <<< factory AIDecide_SuperEnergyRetrieval */
/* >>> factory AIDecide_PokemonBreeder */
AIDecidePokemonBreederResult AIDecide_PokemonBreeder(uint16_t hl_in, uint8_t d)
{
	/* d: the entry value on the Prehistoric Power refusal; `ld d, a` takes
	 * each hand card's deck index in the two hand loops (their callees are
	 * bracketed in `push de` / `pop de`), CreateHandCardList leaves
	 * wDuelTempList's page when the hand is empty, and the score loops start
	 * from `ld d, $00`. */
	PrehistoricPowerResult power = IsPrehistoricPowerActive(hl_in);
	if (power.f & 0x10u)
		return (AIDecidePokemonBreederResult){power.a, power.f, d};

	ClearMemory_Bank8(7u, wce08_ADDR);
	wce06 = 0u;
	d = CreateHandCardList(0u).d;
	uint16_t hl = wDuelTempList_ADDR;

	for (;;) {
		uint8_t deck_index = gb_read8(hl);
		hl++;
		if (deck_index == 0xFFu)
			break;
		d = deck_index;

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
		return (AIDecidePokemonBreederResult){best_loc, 0x10u, 0u};
	}

	ClearMemory_Bank8(7u, wce08_ADDR);
	wce06 = 0u;
	d = CreateHandCardList(0u).d;
	uint16_t hl2 = wDuelTempList_ADDR;

	for (;;) {
		uint8_t deck_index = gb_read8(hl2);
		hl2++;
		if (deck_index == 0xFFu)
			break;
		d = deck_index;

		uint8_t c = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		uint8_t e = PLAY_AREA_ARENA;
		for (; c != 0u; c--, e++) {
			EvolveResult evolve = CheckIfCanEvolveInto_BasicToStage2(deck_index, e);
			if (evolve.f & 0x10u)
				continue;

			CardId evolving_id = GetCardIDFromDeckIndex(deck_index);
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
		return (AIDecidePokemonBreederResult){0u, 0x80u, d};

	wce06 = 0u;
	wce07 = 0xFFu;
	d = 0u;
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
		return (AIDecidePokemonBreederResult){0xFFu, 0x00u, d};

	wce1a = gb_read8((uint16_t)(wce0f_ADDR + wce07));
	return (AIDecidePokemonBreederResult){wce07, 0x10u, d};
}
/* <<< factory AIDecide_PokemonBreeder */
/* >>> factory AIDecide_PokemonTrader_LegendaryArticuno */
AIDecide_PokemonTrader_LegendaryArticunoResult AIDecide_PokemonTrader_LegendaryArticuno(uint8_t d)
{
	LookForCardIDInHandAndPlayAreaResult r =
		LookForCardIDInHandAndPlayArea(ARTICUNO_LV35);
	if (r.f & 0x10u)
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){r.a,
			(uint8_t)(r.a == 0u ? 0x80u : 0u), 0u};
	r = LookForCardIDInHandAndPlayArea(LAPRAS);
	if (r.f & 0x10u)
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){r.a,
			(uint8_t)(r.a == 0u ? 0x80u : 0u), 0u};

	r = LookForCardIDInHandAndPlayArea(SEEL);
	if (!(r.f & 0x10u)) {
		LookForCardIDInLocationBank8Result loc =
			LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, SEEL);
		d = 0u;
		if (loc.f & 0x10u) {
			wce1a = loc.a;
			goto check_articuno_trader_hand;
		}
	}

	r = LookForCardIDInHandAndPlayArea(DEWGONG);
	if (r.f & 0x10u)
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){r.a,
			(uint8_t)(r.a == 0u ? 0x80u : 0u), 0u};
	{
		LookForCardIDInLocationBank8Result loc =
			LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, DEWGONG);
		d = 0u;
		if (!(loc.f & 0x10u))
			return (AIDecide_PokemonTrader_LegendaryArticunoResult){loc.a,
				(uint8_t)(loc.a == 0u ? 0x80u : 0u), d};
		wce1a = loc.a;
	}

check_articuno_trader_hand:
	{
		CheckIfHasCardIDInHandResult h = CheckIfHasCardIDInHand(CHANSEY);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, 0x10u, 0u};
		h = CheckIfHasCardIDInHand(DITTO);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, 0x10u, 0u};
		h = CheckIfHasCardIDInHand(ARTICUNO_LV37);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, 0x10u, 0u};
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a,
			(uint8_t)(h.a == 0u ? 0x80u : 0u), 0u};
	}
}
/* <<< factory AIDecide_PokemonTrader_LegendaryArticuno */
/* >>> factory AIDecide_Pokeball */
AIDecide_PokeballResult AIDecide_Pokeball(uint8_t d)
{
	uint8_t deck_id = wOpponentDeckID;

	if (deck_id == FIRE_CHARGE_DECK_ID) {
		LookForCardIDInLocationBank8Result r;
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, CHANSEY);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, TAUROS);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, JIGGLYPUFF_LV12);
		d = 0u;
		return (AIDecide_PokeballResult){r.a, r.f, d};
	}

	if (deck_id == HARD_POKEMON_DECK_ID) {
		LookForCardIDInLocationBank8Result r;
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, RHYHORN);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, RHYDON);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, ONIX);
		d = 0u;
		return (AIDecide_PokeballResult){r.a, r.f, d};
	}

	if (deck_id == PIKACHU_DECK_ID) {
		LookForCardIDInLocationBank8Result r;
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_LV14);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_LV16);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_ALT_LV16);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_LV12);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, FLYING_PIKACHU);
		d = 0u;
		return (AIDecide_PokeballResult){r.a, r.f, d};
	}

	if (deck_id == ETCETERA_DECK_ID) {
		LookForCardIDInHandListResult h;
		LookForCardIDInLocationBank8Result r;

		h = LookForCardIDInHandList_Bank8(FIRE_ENERGY);
		d = 0xC5u;
		if (h.f & 0x10u) {
			h = LookForCardIDInHandList_Bank8(CHARMANDER);
			d = 0xC5u;
			if (!(h.f & 0x10u)) {
				h = LookForCardIDInHandList_Bank8(MAGMAR_LV31);
				d = 0xC5u;
				if (!(h.f & 0x10u)) {
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, CHARMANDER);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, MAGMAR_LV31);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
				}
			}
		}

		h = LookForCardIDInHandList_Bank8(LIGHTNING_ENERGY);
		d = 0xC5u;
		if (h.f & 0x10u) {
			h = LookForCardIDInHandList_Bank8(PIKACHU_LV12);
			d = 0xC5u;
			if (!(h.f & 0x10u)) {
				h = LookForCardIDInHandList_Bank8(MAGNEMITE_LV13);
				d = 0xC5u;
				if (!(h.f & 0x10u)) {
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_LV12);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, MAGNEMITE_LV13);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
				}
			}
		}

		h = LookForCardIDInHandList_Bank8(FIGHTING_ENERGY);
		d = 0xC5u;
		if (h.f & 0x10u) {
			h = LookForCardIDInHandList_Bank8(DIGLETT);
			d = 0xC5u;
			if (!(h.f & 0x10u)) {
				h = LookForCardIDInHandList_Bank8(MACHOP);
				d = 0xC5u;
				if (!(h.f & 0x10u)) {
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, DIGLETT);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, MACHOP);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
				}
			}
		}

		h = LookForCardIDInHandList_Bank8(PSYCHIC_ENERGY);
		d = 0xC5u;
		if (h.f & 0x10u) {
			h = LookForCardIDInHandList_Bank8(GASTLY_LV8);
			d = 0xC5u;
			if (!(h.f & 0x10u)) {
				h = LookForCardIDInHandList_Bank8(JYNX);
				d = 0xC5u;
				if (!(h.f & 0x10u)) {
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, GASTLY_LV8);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, JYNX);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
				}
			}
		}

		return (AIDecide_PokeballResult){h.a, or_a_flags(h.a), d};
	}

	if (deck_id == LOVELY_NIDORAN_DECK_ID) {
		LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
		LookForCardIDInDeck_GivenCardIDInHandResult r2;

		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NIDORINO, NIDORANM);
		d = r.d;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NIDOKING, NIDORINO);
		d = r.d;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r2 = LookForCardIDInDeck_GivenCardIDInHand(NIDORANM, NIDORINO);
		d = r2.d;
		if (r2.f & 0x10u) return (AIDecide_PokeballResult){r2.a, r2.f, d};
		r2 = LookForCardIDInDeck_GivenCardIDInHand(NIDORINO, NIDOKING);
		d = r2.d;
		if (r2.f & 0x10u) return (AIDecide_PokeballResult){r2.a, r2.f, d};
		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NIDORINA, NIDORANF);
		d = r.d;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NIDOQUEEN, NIDORINA);
		d = r.d;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r2 = LookForCardIDInDeck_GivenCardIDInHand(NIDORANF, NIDORINA);
		d = r2.d;
		if (r2.f & 0x10u) return (AIDecide_PokeballResult){r2.a, r2.f, d};
		r2 = LookForCardIDInDeck_GivenCardIDInHand(NIDORINA, NIDOQUEEN);
		d = r2.d;
		return (AIDecide_PokeballResult){r2.a, r2.f, d};
	}

	uint8_t f = (deck_id == 0u) ? 0x80u : 0u;
	return (AIDecide_PokeballResult){deck_id, f, d};
}
/* <<< factory AIDecide_Pokeball */
/* >>> factory AIDecide_MrFuji */
AIDecideParameterResult AIDecide_MrFuji(uint8_t d)
{
	gb_write8(wce06_ADDR, 0xFFu);
	gb_write8(wce08_ADDR, 0xFFu);

	DuelistVarResult r1 = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t count = r1.a;
	if (count == 1u)
		return (AIDecideParameterResult){count, 0xC0u, d};

	d = (uint8_t)(count - 1u);
	uint8_t e = PLAY_AREA_BENCH_1;

	while (d != 0u) {
		DuelistVarResult r2 = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e));
		(void)LoadCardDataToBuffer1_FromDeckIndex(r2.a);

		uint8_t maxHP = wLoadedCard1HP;

		CardDamageResult dmg = GetCardDamageAndMaxHP(e);
		uint8_t counters = ConvertHPToDamageCounters_Bank8(dmg.a);
		if (counters != 0u) {
			CalculateBDividedByA_Bank8Result div = CalculateBDividedByA_Bank8(counters, maxHP);
			if (div.a < 20u && div.a < wce08) {
				wce08 = div.a;
				wce06 = e;
			}
		}
		e++;
		d--;
	}

	uint8_t chosen = wce06;
	if (chosen == 0xFFu)
		return (AIDecideParameterResult){chosen, 0xC0u, 0u};
	return (AIDecideParameterResult){chosen, 0x10u, 0u};
}
/* <<< factory AIDecide_MrFuji */
/* >>> factory AIDecide_PokemonTrader_PowerGenerator */
AIDecide_PokemonTrader_PowerGeneratorResult AIDecide_PokemonTrader_PowerGenerator(uint8_t d)
{
	uint8_t a = 0u;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r1 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(RAICHU_LV40, PIKACHU_LV14);
	d = r1.d;
	a = r1.a;
	if (r1.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r2 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(RAICHU_LV40, PIKACHU_LV12);
		d = r2.d;
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r3 =
		LookForCardIDInDeck_GivenCardIDInHand(PIKACHU_LV14, RAICHU_LV40);
		d = r3.d;
	a = r3.a;
	if (r3.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r4 =
		LookForCardIDInDeck_GivenCardIDInHand(PIKACHU_LV12, RAICHU_LV40);
		d = r4.d;
	a = r4.a;
	if (r4.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r5 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(ELECTRODE_LV42, VOLTORB);
		d = r5.d;
	a = r5.a;
	if (r5.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r6 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(ELECTRODE_LV35, VOLTORB);
		d = r6.d;
	a = r6.a;
	if (r6.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r7 =
		LookForCardIDInDeck_GivenCardIDInHand(VOLTORB, ELECTRODE_LV42);
		d = r7.d;
	a = r7.a;
	if (r7.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r8 =
		LookForCardIDInDeck_GivenCardIDInHand(VOLTORB, ELECTRODE_LV35);
		d = r8.d;
	a = r8.a;
	if (r8.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r9 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(MAGNETON_LV35, MAGNEMITE_LV13);
		d = r9.d;
	a = r9.a;
	if (r9.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r10 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(MAGNETON_LV35, MAGNEMITE_LV15);
		d = r10.d;
	a = r10.a;
	if (r10.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r11 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(MAGNETON_LV28, MAGNEMITE_LV13);
		d = r11.d;
	a = r11.a;
	if (r11.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r12 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(MAGNETON_LV28, MAGNEMITE_LV15);
		d = r12.d;
	a = r12.a;
	if (r12.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r13 =
		LookForCardIDInDeck_GivenCardIDInHand(MAGNEMITE_LV15, MAGNETON_LV35);
		d = r13.d;
	a = r13.a;
	if (r13.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r14 =
		LookForCardIDInDeck_GivenCardIDInHand(MAGNEMITE_LV13, MAGNETON_LV35);
		d = r14.d;
	a = r14.a;
	if (r14.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r15 =
		LookForCardIDInDeck_GivenCardIDInHand(MAGNEMITE_LV15, MAGNETON_LV28);
		d = r15.d;
	a = r15.a;
	if (r15.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r16 =
		LookForCardIDInDeck_GivenCardIDInHand(MAGNEMITE_LV13, MAGNETON_LV28);
		d = r16.d;
		a = r16.a;
		if (r16.f & 0x10u)
			goto find_duplicates;
		return (AIDecide_PokemonTrader_PowerGeneratorResult){a,
			(uint8_t)(a == 0u ? 0x80u : 0u), d};

find_duplicates:
	wce1a = a;
	{
		FindDuplicatePokemonCardsResult dup = FindDuplicatePokemonCards();
		d = dup.d;
		if (dup.f & 0x10u)
			return (AIDecide_PokemonTrader_PowerGeneratorResult){dup.a, 0x10u, d};
		return (AIDecide_PokemonTrader_PowerGeneratorResult){dup.a, 0x00u, d};
	}
}
/* <<< factory AIDecide_PokemonTrader_PowerGenerator */
/* >>> factory AIDecide_EnergySearch */
static AIEnergySearchScanResult energy_search_scan(uint8_t type_filter)
{
	uint8_t d = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t e = PLAY_AREA_ARENA;
	for (;;) {
		uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
		CardId card_id = GetCardIDFromDeckIndex(deck_index);
		uint16_t temp_card_id = wTempCardID_ADDR;
		card_id_write(&temp_card_id, card_id);
		LoadCardDataToBuffer1_FromCardID(card_id);
		uint8_t type = (uint8_t)(wLoadedCard1Type | TYPE_ENERGY);
		if (type_filter == ENERGY_SEARCH_ANY_TYPE
		    || type == type_filter
		    || (type_filter == TYPE_ENERGY_FIRE && type == TYPE_ENERGY_LIGHTNING)) {
			wTempCardType = type;
			uint16_t hl = wDuelTempList_ADDR;
			for (;;) {
				uint8_t entry = gb_read8(hl);
				hl++;
				if (entry == 0xFFu)
					break;
				if (CheckIfEnergyIsUseful(entry).f & 0x10u)
					return (AIEnergySearchScanResult){entry,
						(uint8_t)(entry == 0u ? 0x80u : 0x00u), d, e};
			}
		}
		e++;
		if (e == d)
			return (AIEnergySearchScanResult){e, (uint8_t)(0xC0u | 0x10u), d, e};
	}
}

AIDecideEnergySearchResult AIDecide_EnergySearch(uint8_t a, uint8_t d)
{
	CoreCardListResult hand = CreateEnergyCardListFromHand(a);
	if (!(hand.f & 0x10u)) {
		AIEnergySearchScanResult useful = energy_search_scan(ENERGY_SEARCH_ANY_TYPE);
		d = useful.d;
		if (!(useful.f & 0x10u))
			return (AIDecideEnergySearchResult){useful.a, useful.f, d};
	}

	uint8_t deck_id = wOpponentDeckID;
	uint8_t filter;
	if (deck_id == HEATED_BATTLE_DECK_ID)
		filter = TYPE_ENERGY_FIRE;
	else if (deck_id == WONDERS_OF_SCIENCE_DECK_ID)
		filter = TYPE_ENERGY_GRASS;
	else
		filter = ENERGY_SEARCH_ANY_TYPE;

	FindBasicEnergyCardsInLocationResult deck = FindBasicEnergyCardsInLocation(CARD_LOCATION_DECK);
	if (deck.f & 0x10u)
		return (AIDecideEnergySearchResult){deck.a, (uint8_t)(deck.a == 0u ? 0x80u : 0x00u), deck.d};

	AIEnergySearchScanResult scan = energy_search_scan(filter);
	if (!(scan.f & 0x10u))
		return (AIDecideEnergySearchResult){scan.a, (uint8_t)(scan.f | 0x10u), scan.d};
	if (filter != ENERGY_SEARCH_ANY_TYPE)
		return (AIDecideEnergySearchResult){scan.a,
			(uint8_t)(scan.a == 0u ? 0x80u : 0x00u), scan.d};
	return (AIDecideEnergySearchResult){wDuelTempList, 0x90u, scan.d};
}
/* <<< factory AIDecide_EnergySearch */
/* >>> factory _AIProcessHandTrainerCards */
/* Adapters: every decide routine yields (a, f) -- a is the parameter stored
 * in wAITrainerCardParameter on carry -- and every play routine yields f.
 * Register arguments the C signatures still carry are the asm's incidental
 * inputs; the loop hands them the scratch values it has. */
typedef struct { uint8_t a; uint8_t f; uint8_t d; uint8_t e; } TrainerDecision;
static TrainerDecision decide_AIDecide_Bill(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Bill(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_ClefairyDollOrMysteriousFossil(uint8_t d, uint8_t e) { AIDecidePokemonFluteResult r = AIDecide_ClefairyDollOrMysteriousFossil(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_ComputerSearch(uint8_t d, uint8_t e) { AIDecide_ComputerSearchResult r = AIDecide_ComputerSearch(0u, 0u, d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Defender1(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Defender1(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Defender2(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Defender2(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_EnergyRemoval(uint8_t d, uint8_t e) { AIDecideEnergyRemovalResult r = AIDecide_EnergyRemoval(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_EnergyRetrieval(uint8_t d, uint8_t e) { AIDecideEnergyRetrievalResult r = AIDecide_EnergyRetrieval(0u, d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_EnergySearch(uint8_t d, uint8_t e) { AIDecideEnergySearchResult r = AIDecide_EnergySearch(0u, d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_FullHeal(uint8_t d, uint8_t e) { AIDecideFullHealResult r = AIDecide_FullHeal(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Gambler(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Gambler(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_GustOfWind(uint8_t d, uint8_t e) { AIDecideGustOfWindResult r = AIDecide_GustOfWind(d, e); return (TrainerDecision){r.a, r.f, r.d, r.e}; }
static TrainerDecision decide_AIDecide_Imakuni(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Imakuni(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_ImposterProfessorOak(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_ImposterProfessorOak(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_ItemFinder(uint8_t d, uint8_t e) { AIDecide_ItemFinderResult r = AIDecide_ItemFinder(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Lass(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Lass(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Maintenance(uint8_t d, uint8_t e) { AIDecideMaintenanceResult r = AIDecide_Maintenance(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_MrFuji(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_MrFuji(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_PlusPower1(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_PlusPower1(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_PlusPower2(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_PlusPower2(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Pokeball(uint8_t d, uint8_t e) { AIDecide_PokeballResult r = AIDecide_Pokeball(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Pokedex(uint8_t d, uint8_t e) { AIDecidePokedexResult r = AIDecide_Pokedex(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_PokemonBreeder(uint8_t d, uint8_t e) { AIDecidePokemonBreederResult r = AIDecide_PokemonBreeder(0u, d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_PokemonCenter(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_PokemonCenter(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_PokemonFlute(uint8_t d, uint8_t e) { AIDecidePokemonFluteResult r = AIDecide_PokemonFlute(0u, d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_PokemonTrader(uint8_t d, uint8_t e) { AIDecide_PokemonTraderResult r = AIDecide_PokemonTrader(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Potion_Phase07(uint8_t d, uint8_t e) { AIDecidePotionPhase07Result r = AIDecide_Potion_Phase07(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Potion_Phase10(uint8_t d, uint8_t e) { AIDecidePotionPhase10Result r = AIDecide_Potion_Phase10(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_ProfessorOak(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_ProfessorOak(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Recycle(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Recycle(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Revive(uint8_t d, uint8_t e) { AIDecideReviveResult r = AIDecide_Revive(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_ScoopUp(uint8_t d, uint8_t e) { AIDecide_ScoopUpResult r = AIDecide_ScoopUp(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_SuperEnergyRemoval(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_SuperEnergyRemoval(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_SuperEnergyRetrieval(uint8_t d, uint8_t e) { AIDecideSuperEnergyRetrievalResult r = AIDecide_SuperEnergyRetrieval(0u, d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_SuperPotion1(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_SuperPotion1(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_SuperPotion2(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_SuperPotion2(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Switch(uint8_t d, uint8_t e) { AIDecide_SwitchResult r = AIDecide_Switch(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static uint8_t play_AIPlay_Bill(uint8_t d, uint8_t e) { return AIPlay_Bill(d, e).f; }
static uint8_t play_AIPlay_ClefairyDollOrMysteriousFossil(uint8_t d, uint8_t e) { return AIPlay_ClefairyDollOrMysteriousFossil(d, e).f; }
static uint8_t play_AIPlay_ComputerSearch(uint8_t d, uint8_t e) { return AIPlay_ComputerSearch(d, e).f; }
static uint8_t play_AIPlay_Defender(uint8_t d, uint8_t e) { return AIPlay_Defender(d, e).f; }
static uint8_t play_AIPlay_EnergyRemoval(uint8_t d, uint8_t e) { return AIPlay_EnergyRemoval(d, e).f; }
static uint8_t play_AIPlay_EnergyRetrieval(uint8_t d, uint8_t e) { return AIPlay_EnergyRetrieval(d, e).f; }
static uint8_t play_AIPlay_EnergySearch(uint8_t d, uint8_t e) { return AIPlay_EnergySearch(d, e).f; }
static uint8_t play_AIPlay_FullHeal(uint8_t d, uint8_t e) { return AIPlay_FullHeal(d, e).f; }
static uint8_t play_AIPlay_Gambler(uint8_t d, uint8_t e) { return AIPlay_Gambler(d, e).f; }
static uint8_t play_AIPlay_GustOfWind(uint8_t d, uint8_t e) { return AIPlay_GustOfWind(d, e).f; }
static uint8_t play_AIPlay_Imakuni(uint8_t d, uint8_t e) { return AIPlay_Imakuni(d, e).f; }
static uint8_t play_AIPlay_ImposterProfessorOak(uint8_t d, uint8_t e) { return AIPlay_ImposterProfessorOak(d, e).f; }
static uint8_t play_AIPlay_ItemFinder(uint8_t d, uint8_t e) { return AIPlay_ItemFinder(d, e).f; }
static uint8_t play_AIPlay_Lass(uint8_t d, uint8_t e) { return AIPlay_Lass(d, e).f; }
static uint8_t play_AIPlay_Maintenance(uint8_t d, uint8_t e) { return AIPlay_Maintenance(d, e).f; }
static uint8_t play_AIPlay_MrFuji(uint8_t d, uint8_t e) { return AIPlay_MrFuji(d, e).f; }
static uint8_t play_AIPlay_PlusPower(uint8_t d, uint8_t e) { return AIPlay_PlusPower(d, e).f; }
static uint8_t play_AIPlay_Pokeball(uint8_t d, uint8_t e) { return AIPlay_Pokeball(d, e).f; }
static uint8_t play_AIPlay_Pokedex(uint8_t d, uint8_t e) { return AIPlay_Pokedex(d, e).f; }
static uint8_t play_AIPlay_PokemonBreeder(uint8_t d, uint8_t e) { return AIPlay_PokemonBreeder(d, e).f; }
static uint8_t play_AIPlay_PokemonCenter(uint8_t d, uint8_t e) { return AIPlay_PokemonCenter(d, e).f; }
static uint8_t play_AIPlay_PokemonFlute(uint8_t d, uint8_t e) { return AIPlay_PokemonFlute(d, e).f; }
static uint8_t play_AIPlay_PokemonTrader(uint8_t d, uint8_t e) { return AIPlay_PokemonTrader(d, e).f; }
static uint8_t play_AIPlay_Potion(uint8_t d, uint8_t e) { return AIPlay_Potion(d, e).f; }
static uint8_t play_AIPlay_ProfessorOak(uint8_t d, uint8_t e) { return AIPlay_ProfessorOak(d, e).f; }
static uint8_t play_AIPlay_Recycle(uint8_t d, uint8_t e) { return AIPlay_Recycle(d, e).f; }
static uint8_t play_AIPlay_Revive(uint8_t d, uint8_t e) { return AIPlay_Revive(d, e).f; }
static uint8_t play_AIPlay_ScoopUp(uint8_t d, uint8_t e) { return AIPlay_ScoopUp(d, e).f; }
static uint8_t play_AIPlay_SuperEnergyRemoval(uint8_t d, uint8_t e) { return AIPlay_SuperEnergyRemoval(d, e).f; }
static uint8_t play_AIPlay_SuperEnergyRetrieval(uint8_t d, uint8_t e) { return AIPlay_SuperEnergyRetrieval(d, e).f; }
static uint8_t play_AIPlay_SuperPotion(uint8_t d, uint8_t e) { return AIPlay_SuperPotion(d, e).f; }
static uint8_t play_AIPlay_Switch(uint8_t d, uint8_t e) { return AIPlay_Switch(d, e).f; }

typedef struct {
	uint8_t phase;
	CardId card;
	TrainerDecision (*decide)(uint8_t d, uint8_t e);
	uint8_t (*play)(uint8_t d, uint8_t e);
} TrainerLogic;

/* data/duel/ai_trainer_card_logic.asm, in table order. */
static const TrainerLogic trainer_logic[] = {
	{AI_TRAINER_CARD_PHASE_07, POTION, decide_AIDecide_Potion_Phase07, play_AIPlay_Potion}, /* POTION */
	{AI_TRAINER_CARD_PHASE_10, POTION, decide_AIDecide_Potion_Phase10, play_AIPlay_Potion}, /* POTION */
	{AI_TRAINER_CARD_PHASE_08, SUPER_POTION, decide_AIDecide_SuperPotion1, play_AIPlay_SuperPotion}, /* SUPER_POTION */
	{AI_TRAINER_CARD_PHASE_11, SUPER_POTION, decide_AIDecide_SuperPotion2, play_AIPlay_SuperPotion}, /* SUPER_POTION */
	{AI_TRAINER_CARD_PHASE_13, DEFENDER, decide_AIDecide_Defender1, play_AIPlay_Defender}, /* DEFENDER */
	{AI_TRAINER_CARD_PHASE_14, DEFENDER, decide_AIDecide_Defender2, play_AIPlay_Defender}, /* DEFENDER */
	{AI_TRAINER_CARD_PHASE_13, PLUSPOWER, decide_AIDecide_PlusPower1, play_AIPlay_PlusPower}, /* PLUSPOWER */
	{AI_TRAINER_CARD_PHASE_14, PLUSPOWER, decide_AIDecide_PlusPower2, play_AIPlay_PlusPower}, /* PLUSPOWER */
	{AI_TRAINER_CARD_PHASE_09, SWITCH, decide_AIDecide_Switch, play_AIPlay_Switch}, /* SWITCH */
	{AI_TRAINER_CARD_PHASE_07, GUST_OF_WIND, decide_AIDecide_GustOfWind, play_AIPlay_GustOfWind}, /* GUST_OF_WIND */
	{AI_TRAINER_CARD_PHASE_10, GUST_OF_WIND, decide_AIDecide_GustOfWind, play_AIPlay_GustOfWind}, /* GUST_OF_WIND */
	{AI_TRAINER_CARD_PHASE_04, BILL, decide_AIDecide_Bill, play_AIPlay_Bill}, /* BILL */
	{AI_TRAINER_CARD_PHASE_05, ENERGY_REMOVAL, decide_AIDecide_EnergyRemoval, play_AIPlay_EnergyRemoval}, /* ENERGY_REMOVAL */
	{AI_TRAINER_CARD_PHASE_05, SUPER_ENERGY_REMOVAL, decide_AIDecide_SuperEnergyRemoval, play_AIPlay_SuperEnergyRemoval}, /* SUPER_ENERGY_REMOVAL */
	{AI_TRAINER_CARD_PHASE_07, POKEMON_BREEDER, decide_AIDecide_PokemonBreeder, play_AIPlay_PokemonBreeder}, /* POKEMON_BREEDER */
	{AI_TRAINER_CARD_PHASE_15, PROFESSOR_OAK, decide_AIDecide_ProfessorOak, play_AIPlay_ProfessorOak}, /* PROFESSOR_OAK */
	{AI_TRAINER_CARD_PHASE_10, ENERGY_RETRIEVAL, decide_AIDecide_EnergyRetrieval, play_AIPlay_EnergyRetrieval}, /* ENERGY_RETRIEVAL */
	{AI_TRAINER_CARD_PHASE_11, SUPER_ENERGY_RETRIEVAL, decide_AIDecide_SuperEnergyRetrieval, play_AIPlay_SuperEnergyRetrieval}, /* SUPER_ENERGY_RETRIEVAL */
	{AI_TRAINER_CARD_PHASE_06, POKEMON_CENTER, decide_AIDecide_PokemonCenter, play_AIPlay_PokemonCenter}, /* POKEMON_CENTER */
	{AI_TRAINER_CARD_PHASE_07, IMPOSTER_PROFESSOR_OAK, decide_AIDecide_ImposterProfessorOak, play_AIPlay_ImposterProfessorOak}, /* IMPOSTER_PROFESSOR_OAK */
	{AI_TRAINER_CARD_PHASE_12, ENERGY_SEARCH, decide_AIDecide_EnergySearch, play_AIPlay_EnergySearch}, /* ENERGY_SEARCH */
	{AI_TRAINER_CARD_PHASE_03, POKEDEX, decide_AIDecide_Pokedex, play_AIPlay_Pokedex}, /* POKEDEX */
	{AI_TRAINER_CARD_PHASE_07, FULL_HEAL, decide_AIDecide_FullHeal, play_AIPlay_FullHeal}, /* FULL_HEAL */
	{AI_TRAINER_CARD_PHASE_10, MR_FUJI, decide_AIDecide_MrFuji, play_AIPlay_MrFuji}, /* MR_FUJI */
	{AI_TRAINER_CARD_PHASE_10, SCOOP_UP, decide_AIDecide_ScoopUp, play_AIPlay_ScoopUp}, /* SCOOP_UP */
	{AI_TRAINER_CARD_PHASE_02, MAINTENANCE, decide_AIDecide_Maintenance, play_AIPlay_Maintenance}, /* MAINTENANCE */
	{AI_TRAINER_CARD_PHASE_03, RECYCLE, decide_AIDecide_Recycle, play_AIPlay_Recycle}, /* RECYCLE */
	{AI_TRAINER_CARD_PHASE_13, LASS, decide_AIDecide_Lass, play_AIPlay_Lass}, /* LASS */
	{AI_TRAINER_CARD_PHASE_04, ITEM_FINDER, decide_AIDecide_ItemFinder, play_AIPlay_ItemFinder}, /* ITEM_FINDER */
	{AI_TRAINER_CARD_PHASE_01, IMAKUNI_CARD, decide_AIDecide_Imakuni, play_AIPlay_Imakuni}, /* IMAKUNI_CARD */
	{AI_TRAINER_CARD_PHASE_01, GAMBLER, decide_AIDecide_Gambler, play_AIPlay_Gambler}, /* GAMBLER */
	{AI_TRAINER_CARD_PHASE_05, REVIVE, decide_AIDecide_Revive, play_AIPlay_Revive}, /* REVIVE */
	{AI_TRAINER_CARD_PHASE_13, POKEMON_FLUTE, decide_AIDecide_PokemonFlute, play_AIPlay_PokemonFlute}, /* POKEMON_FLUTE */
	{AI_TRAINER_CARD_PHASE_05, CLEFAIRY_DOLL, decide_AIDecide_ClefairyDollOrMysteriousFossil, play_AIPlay_ClefairyDollOrMysteriousFossil}, /* CLEFAIRY_DOLL */
	{AI_TRAINER_CARD_PHASE_05, MYSTERIOUS_FOSSIL, decide_AIDecide_ClefairyDollOrMysteriousFossil, play_AIPlay_ClefairyDollOrMysteriousFossil}, /* MYSTERIOUS_FOSSIL */
	{AI_TRAINER_CARD_PHASE_02, POKE_BALL, decide_AIDecide_Pokeball, play_AIPlay_Pokeball}, /* POKE_BALL */
	{AI_TRAINER_CARD_PHASE_02, COMPUTER_SEARCH, decide_AIDecide_ComputerSearch, play_AIPlay_ComputerSearch}, /* COMPUTER_SEARCH */
	{AI_TRAINER_CARD_PHASE_02, POKEMON_TRADER, decide_AIDecide_PokemonTrader, play_AIPlay_PokemonTrader}, /* POKEMON_TRADER */
};

static uint16_t relist_hand(void)
{
	(void)CreateHandCardList(0u);
	uint16_t hl = wDuelTempList_ADDR;
	uint16_t de = wTempHandCardList_ADDR;
	(void)CopyListWithFFTerminatorFromHLToDE_Bank8(&hl, &de);
	return de;
}

/* trainer_cards.asm:3-148. For every card in hand, every table row of the
 * requested phase naming that card is tried: the card must be playable
 * (Headache, its own initial effect, the AI's random abstention), its decide
 * routine must return carry, and the Play Trainer screen must not end the
 * turn. A hand modified by the card's effect is re-listed from the top. */
AIProcessHandTrainerCardsResult _AIProcessHandTrainerCards(uint8_t a)
{
	wAITrainerCardPhase = a;
	/* e is the register the asm never reloads: the list copy leaves de on the
	 * hand list's terminator, every decide routine is entered with the e its
	 * predecessor left, and a played card's effect commands receive the
	 * decide routine's exit de (PlayAttackAnimation stores that de into
	 * wDamageAnimAmount). AIDecide_GustOfWind reports its exit e; the other
	 * decide routines and the play routines pass the entry e through, which is
	 * exact for the ones whose asm never touches de and unmodeled for the
	 * rest (their exit e only ever reaches memory through that one store). */
	uint8_t e = (uint8_t)relist_hand();
	uint16_t hand = wTempHandCardList_ADDR;
	for (;;) {
		uint8_t card = gb_read8(hand++);
		wAITrainerCardToPlay = card;
		if (card == 0xffu)
			return (AIProcessHandTrainerCardsResult){0xffu, 0xc0u};
		uint8_t d = wAITrainerCardPhase;
		for (size_t row = 0; row < sizeof trainer_logic / sizeof trainer_logic[0]; row++) {
			const TrainerLogic *logic = &trainer_logic[row];
			wCurrentAIFlags = 0u;
			if (logic->phase != d)
				continue;
			(void)LoadCardDataToBuffer1_FromDeckIndex(wAITrainerCardToPlay);
			CardId id = card_id_read_at(wLoadedCard1ID_ADDR);
			if (id == SWITCH && (wPreviousAIFlags & AI_FLAG_USED_SWITCH) != 0u)
				continue;
			d = (uint8_t)(id >> 8);
			e = (uint8_t)id;
			if (id != logic->card)
				continue;
			hTempCardIndex_ff9f = wAITrainerCardToPlay;
			if ((CheckCantUseTrainerDueToEffect().f & 0x10u) != 0u)
				continue;
			LoadEffectResult loaded = LoadNonPokemonCardEffectCommands();
			if ((TryExecuteEffectCommandFunction(EFFECTCMDTYPE_INITIAL_EFFECT_1, 0u, (uint8_t)(loaded.de >> 8), (uint8_t)loaded.de).f & 0x10u) != 0u)
				continue;
			if ((AIChooseRandomlyNotToDoAction().f & 0x10u) != 0u)
				continue;
			TrainerDecision decision = logic->decide(d, e);
			d = decision.d;
			e = decision.e;
			if ((decision.f & 0x10u) == 0u)
				continue;
			wAITrainerCardParameter = decision.a;
			hTempCardIndex_ff9f = wAITrainerCardToPlay;
			if ((AIMakeDecision(OPPACTION_PLAY_TRAINER, 0u, 0u, 0u, 0u).f & 0x10u) != 0u)
				continue;
			(void)logic->play(d, e);
			wPreviousAIFlags = (uint8_t)(wPreviousAIFlags | wCurrentAIFlags);
			if ((wPreviousAIFlags & AI_FLAG_MODIFIED_HAND) != 0u) {
				e = (uint8_t)relist_hand();
				hand = wTempHandCardList_ADDR;
				wPreviousAIFlags = (uint8_t)(wPreviousAIFlags & (uint8_t)~AI_FLAG_MODIFIED_HAND);
			}
			break;
		}
	}
}
/* <<< factory _AIProcessHandTrainerCards */
/* === factory AIPlay_Bill */
/* >>> part AIDecide_Defender1 */
AIDecideParameterResult AIDecide_Defender1(uint8_t d)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
	d = ko.d;
	if (ko.f & 0x10u) {
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(ko.a, ko.f, 0u, 0u, d, 0u, 0u);
		d = unusable.d;
		if ((unusable.f & 0x10u) == 0u)
			return (AIDecideParameterResult){unusable.a, or_a_flags(unusable.a), d};
		LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
		d = energy.d;
		if (energy.f & 0x10u)
			return (AIDecideParameterResult){energy.a, or_a_flags(energy.a), d};
	}
	CheckIfAnyDefendingPokemonAttackDealsSameDamageAsHPResult same =
		CheckIfAnyDefendingPokemonAttackDealsSameDamageAsHP();
	d = same.d;
	if ((same.f & 0x10u) == 0u)
		return (AIDecideParameterResult){same.a, or_a_flags(same.a), d};
	SwapTurn();
	CheckIfSelectedAttackIsUnusableResult selected =
		CheckIfSelectedAttackIsUnusable(same.a, same.f, 0u, 0u, d, 0u, 0u);
	SwapTurn();
	d = selected.d;
	if (selected.f & 0x10u)
		return (AIDecideParameterResult){selected.a, or_a_flags(selected.a), d};
	(void)EstimateDamage_FromDefendingPokemon(wSelectedAttack);
	uint8_t selected_damage = wDamage;
	wce06 = selected_damage;
	d = selected_damage;
	wSelectedAttack = (uint8_t)(SECOND_ATTACK - wSelectedAttack);
	SwapTurn();
	CheckIfSelectedAttackIsUnusableResult other =
		CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, d, 0u, 0u);
	SwapTurn();
	uint8_t switch_back = (other.f & 0x10u) != 0u;
	if (!switch_back) {
		(void)EstimateDamage_FromDefendingPokemon(wSelectedAttack);
		switch_back = wDamage < selected_damage;
	}
	if (switch_back) {
		wSelectedAttack = (uint8_t)(SECOND_ATTACK - wSelectedAttack);
		wDamage = wce06;
	}
	uint8_t after_defender = (uint8_t)(wDamage - 20u);
	d = after_defender;
	uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t left = (uint8_t)(hp - after_defender);
	if (hp <= after_defender)
		return (AIDecideParameterResult){left, or_a_flags(left), d};
	return (AIDecideParameterResult){left, 0x10u, d};
}
/* <<< part AIDecide_Defender1 */
/* >>> part AIDecide_Defender2 */
AIDecideParameterResult AIDecide_Defender2(uint8_t d)
{
	AttackFlagResult recoil = CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | HIGH_RECOIL_F);
	if ((recoil.f & 0x10u) == 0u)
		recoil = CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | LOW_RECOIL_F);
	if ((recoil.f & 0x10u) == 0u)
		return (AIDecideParameterResult){recoil.a, or_a_flags(recoil.a), d};
	(void)LoadCardDataToBuffer2_FromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
	uint8_t damage = wSelectedAttack == 0u ? wLoadedCard2Atk1EffectParam : wLoadedCard2Atk2EffectParam;
	uint8_t color = TranslateColorToWR(GetArenaCardColor());
	if (GetArenaCardWeakness() & color)
		damage = (uint8_t)(damage << 1);
	color = TranslateColorToWR(GetArenaCardColor());
	if (GetArenaCardResistance() & color) {
		uint8_t reduced = (uint8_t)(damage - 30u);
		if (damage < 30u)
			return (AIDecideParameterResult){reduced, or_a_flags(reduced), damage};
		damage = reduced;
	}
	if (damage == 0u)
		return (AIDecideParameterResult){0u, 0x80u, damage};
	damage = (uint8_t)(damage - 20u);
	uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t left = (uint8_t)(hp - damage);
	if (hp <= damage)
		return (AIDecideParameterResult){left, or_a_flags(left), damage};
	return (AIDecideParameterResult){left, 0x10u, damage};
}
/* <<< part AIDecide_Defender2 */
/* --- factory AIDecide_PlusPower_Phase14 */
/* >>> factory AIDecide_GustOfWind */
/* trainer_cards.asm AIDecide_GustOfWind. The local routines that stand a
 * bench card in for the player's arena card restore it through two `pop af`,
 * so the Z each carry-exit keeps is GetNonTurnDuelistVariable's own
 * `cp PLAYER_TURN`. */
static uint8_t non_turn_z(void)
{
	return hWhoseTurn == PLAYER_TURN ? 0x80u : 0x00u;
}

/* .CheckIfAttackDealsNoDamage: carry when the attack is a Pokemon Power or
 * can deal no damage at all to the defending card. */
static uint8_t gust_attack_deals_no_damage(uint8_t *d, uint8_t *e)
{
	AttackCopyResult copy = CopyAttackDataAndDamage_FromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a, wSelectedAttack);
	*d = (uint8_t)(copy.de >> 8);
	*e = (uint8_t)copy.de;
	if (wLoadedAttackCategory == POKEMON_POWER)
		return 1u;
	if (wDamage == 0u)
		return 0u;
	DamageCalculationResult estimate = EstimateDamage_VersusDefendingCard(wSelectedAttack);
	*d = estimate.d;
	*e = estimate.e;
	return wAIMaxDamage == 0u;
}

/* .CheckIfNoAttackDealsDamage */
static uint8_t gust_no_attack_deals_damage(uint8_t *d, uint8_t *e)
{
	wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
	if (!gust_attack_deals_no_damage(d, e))
		return 0u;
	wSelectedAttack = SECOND_ATTACK;
	return gust_attack_deals_no_damage(d, e);
}

/* Stand the player's bench card at `location` in as the arena card, run
 * `check`, put the arena card back. Returns the check's verdict. */
typedef uint8_t (*GustArenaCheck)(uint8_t location);

static uint8_t gust_with_bench_card_in_arena(uint8_t location, GustArenaCheck check)
{
	DuelistVarResult arena = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint8_t arena_card = arena.a;
	gb_write8(arena.hl, GetNonTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD)).a);
	uint8_t bench_hp = GetNonTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD_HP)).a;
	DuelistVarResult hp = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	uint8_t arena_hp = hp.a;
	gb_write8(hp.hl, bench_hp);
	uint8_t verdict = check(location);
	gb_write8(GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).hl, arena_hp);
	gb_write8(GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD).hl, arena_card);
	return verdict;
}

/* .CheckIfAttackKnocksOut against the card in location e. */
static uint8_t gust_attack_knocks_out(uint8_t attack, uint8_t location)
{
	(void)EstimateDamage_VersusDefendingCard(attack);
	return GetNonTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + location)).a <= wDamage;
}

/* .CheckIfAnyAttackKnocksOut, then whether that attack can actually be used:
 * usable now, or usable once the energy in hand is attached. */
static uint8_t gust_knockout_check(uint8_t location)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	if (!gust_attack_knocks_out(FIRST_ATTACK_OR_PKMN_POWER, location)
	    && !gust_attack_knocks_out(SECOND_ATTACK, location))
		return 0u;
	if ((CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) == 0u)
		return 1u;
	return (LookForEnergyNeededForAttackInHand().f & 0x10u) != 0u;
}

/* .FindBenchCardToKnockOut */
static uint8_t gust_find_bench_card_to_knock_out(uint8_t *location_out)
{
	uint16_t bench = GetNonTurnDuelistVariable(DUELVARS_BENCH).hl;
	for (uint8_t location = PLAY_AREA_BENCH_1;; location++) {
		if (gb_read8(bench++) == 0xFFu)
			return 0u;
		if (gust_with_bench_card_in_arena(location, gust_knockout_check)) {
			*location_out = location;
			return 1u;
		}
	}
}

/* .CheckIfCanDamageBenchedCard's check */
static uint8_t gust_can_damage_arena(uint8_t location)
{
	(void)location;
	return (CheckIfCanDamageDefendingPokemon(PLAY_AREA_ARENA, 0x80u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) != 0u;
}

/* .FindBenchCardWithWeakness: a player's bench card weak to color b that the
 * arena card can damage. Carry-exit F keeps CheckIfCanDamageDefendingPokemon's Z. */
static uint8_t gust_find_bench_card_with_weakness(uint8_t color, uint8_t *location_out, uint8_t *z_out, uint8_t *d, uint8_t *e)
{
	uint16_t bench = GetNonTurnDuelistVariable(DUELVARS_BENCH).hl;
	for (uint8_t location = PLAY_AREA_BENCH_1;; location++) {
		uint8_t card = gb_read8(bench++);
		if (card == 0xFFu)
			return 0u;
		SwapTurn();
		(void)LoadCardDataToBuffer1_FromDeckIndex(card);
		SwapTurn();
		if ((wLoadedCard1Weakness & color) == 0u)
			continue;
		/* .check_can_damage saves only bc and hl around the call: d and e are
		 * the damage check's on every later exit, and the next probe starts
		 * from them. */
		CheckIfCanDamageDefendingPokemonResult damage =
			CheckIfCanDamageDefendingPokemon(PLAY_AREA_ARENA, 0x80u, 0u, 0u, *d, *e, 0u);
		*d = damage.d;
		*e = damage.e;
		if (damage.f & 0x10u) {
			*location_out = location;
			*z_out = (uint8_t)(damage.f & 0x80u);
			return 1u;
		}
	}
}

AIDecideGustOfWindResult AIDecide_GustOfWind(uint8_t d, uint8_t e)
{
	/* d follows the callees: GetCardIDFromDeckIndex clears it at .check_id,
	 * .FindBenchCardToKnockOut restores it through `pop de`, the damage
	 * probes of .FindBenchCardWithWeakness leave theirs, and `ld d, a` makes
	 * it the bench countdown in the two energy/HP loops. e travels the same
	 * way: the attack checks leave their damage estimate's e, .check_id makes
	 * it the arena card id, .FindBenchCardToKnockOut counts the bench in it
	 * (`pop de` / `inc e`) and hands back the location on a hit, the two
	 * energy/HP loops count in it, and the damage probes leave theirs. The
	 * exit e matters: a played Gust of Wind carries it into
	 * PlayAttackAnimation's wDamageAnimAmount store. */
	uint8_t bench_count = (uint8_t)(GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a - 1u);
	if (bench_count == 0u)
		return (AIDecideGustOfWindResult){0u, 0x80u, d, e};
	uint8_t used = (uint8_t)(wPreviousAIFlags & AI_FLAG_USED_GUST_OF_WIND);
	if (used != 0u)
		return (AIDecideGustOfWindResult){used, 0x20u, d, e};
	CheckIfActivePokemonCanUseAnyNonResidualAttackResult attack =
		CheckIfActivePokemonCanUseAnyNonResidualAttack(used, 0xA0u, 0u, 0u, d, e, 0u);
	d = attack.d;
	e = attack.e;
	if ((attack.f & 0x10u) == 0u)
		return (AIDecideGustOfWindResult){attack.a, attack.f, d, e};
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
	d = ko.d;
	e = ko.e;
	if (ko.f & 0x10u) {
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(ko.a, ko.f, 0u, 0u, d, e, 0u);
		d = unusable.d;
		e = unusable.e;
		if ((unusable.f & 0x10u) == 0u)
			return (AIDecideGustOfWindResult){unusable.a, or_a_flags(unusable.a), d, e};
		/* LookForEnergyNeededForAttackInHand's exit e is not modeled: this
		 * refusal leaves the attack check's e. */
		LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
		d = energy.d;
		if (energy.f & 0x10u)
			return (AIDecideGustOfWindResult){energy.a, or_a_flags(energy.a), d, e};
	}
	/* .check_id */
	CardId arena_id = GetCardIDFromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
	d = 0u;
	e = (uint8_t)arena_id;
	if (arena_id == MEW_LV23 || arena_id == MEWTWO_LV53)
		return (AIDecideGustOfWindResult){(uint8_t)arena_id, 0x00u, d, e};
	uint8_t location;
	uint8_t z;
	if (gust_find_bench_card_to_knock_out(&location))
		return (AIDecideGustOfWindResult){location, (uint8_t)(0x10u | non_turn_z()), d, location};
	/* .loop_4 ran off the bench: `inc e` once per bench card from PLAY_AREA_BENCH_1. */
	e = (uint8_t)(bench_count + 1u);
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	if (!gust_no_attack_deals_damage(&d, &e)) {
		uint8_t color = TranslateColorToWR(GetArenaCardColor());
		SwapTurn();
		uint8_t weak = (uint8_t)(GetArenaCardWeakness() & color);
		SwapTurn();
		if (weak != 0u)
			return (AIDecideGustOfWindResult){weak, 0x00u, d, e};
		if (gust_find_bench_card_with_weakness(color, &location, &z, &d, &e))
			return (AIDecideGustOfWindResult){location, (uint8_t)(0x10u | z), d, e};
		return (AIDecideGustOfWindResult){0xFFu, 0x00u, d, e};
	}
	/* .check_bench_energy: the arena card cannot damage the defending card.
	 * The asm never loads b here: it is whatever the last damage estimate
	 * left, and every estimate that reaches its weakness/resistance tail
	 * leaves `ld b, CARD_LOCATION_ARENA` (ApplyAttachedDefender's input,
	 * damage_calculation.asm:166). That value doubles as a WATER weakness
	 * mask. A ROM bug, modeled as the register it is. */
	if (gust_find_bench_card_with_weakness(CARD_LOCATION_ARENA, &location, &z, &d, &e))
		return (AIDecideGustOfWindResult){location, (uint8_t)(0x10u | z), d, e};
	d = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	for (location = PLAY_AREA_BENCH_1; --d != 0u; location++) {
		SwapTurn();
		(void)GetPlayAreaCardAttachedEnergies(location);
		SwapTurn();
		if (wTotalAttachedEnergies != 0u)
			continue;
		if (gust_with_bench_card_in_arena(location, gust_can_damage_arena))
			return (AIDecideGustOfWindResult){location, (uint8_t)(0x10u | non_turn_z()), d, location};
	}
	/* .check_bench_hp: the damageable bench card with the least HP left. */
	wce06 = 0xFFu;
	wce08 = 0u;
	d = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	for (location = PLAY_AREA_BENCH_1; --d != 0u; location++) {
		uint8_t hp = GetNonTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD_HP)).a;
		if (wce06 < (uint8_t)(hp + 1u))
			continue;
		if (!gust_with_bench_card_in_arena(location, gust_can_damage_arena))
			continue;
		wce06 = hp;
		wce08 = location;
	}
	/* Both loops end with `dec d` reaching zero after `inc e` counted every
	 * play area slot: e is the non-turn duelist's play area count. */
	e = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t found = wce08;
	if (found == 0u)
		return (AIDecideGustOfWindResult){0u, 0x80u, d, e};
	return (AIDecideGustOfWindResult){found, 0x10u, d, e};
}
/* <<< factory AIDecide_GustOfWind */
/* --- factory AIDecide_Defender_Phase13 */
/* >>> factory AIDecide_ScoopUp */
AIDecide_ScoopUpResult AIDecide_ScoopUp(uint8_t d)
{
	/* trainer_cards.asm AIDecide_ScoopUp. d follows the callees;
	 * GetCardIDFromDeckIndex's `ld d, $0` clears it, `ld d, a` takes the
	 * arena card's HP in damage counters, and the switch decision reports
	 * the chosen bench slot. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	if (count.a < 2u)
		return (AIDecide_ScoopUpResult){count.a, or_a_flags(count.a), d};
	uint8_t deck_id = wOpponentDeckID;
	uint8_t slot;
	if (deck_id == LEGENDARY_ARTICUNO_DECK_ID) {
		/* .HandleLegendaryArticuno */
		count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
		if (count.a < 3u)
			return (AIDecide_ScoopUpResult){count.a, or_a_flags(count.a), d};
		LookForCardIDInPlayAreaResult bench = LookForCardIDInPlayArea_Bank8(ARTICUNO_LV37, PLAY_AREA_BENCH_1);
		if (bench.f & 0x10u) {
			slot = bench.a;
			goto articuno_bench;
		}
		CardId arena_id = GetCardIDFromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
		d = 0u;
		if (arena_id != ARTICUNO_LV37 && arena_id != CHANSEY)
			return (AIDecide_ScoopUpResult){(uint8_t)arena_id, or_a_flags((uint8_t)arena_id), d};
		/* .articuno_or_chansey */
		CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
		d = ko.d;
		if (ko.f & 0x10u) {
			CheckIfSelectedAttackIsUnusableResult unusable =
				CheckIfSelectedAttackIsUnusable(ko.a, ko.f, 0u, 0u, d, 0u, 0u);
			d = unusable.d;
			if ((unusable.f & 0x10u) == 0u)
				return (AIDecide_ScoopUpResult){unusable.a, or_a_flags(unusable.a), d};
			LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
			d = energy.d;
			if (energy.f & 0x10u)
				return (AIDecide_ScoopUpResult){energy.a, or_a_flags(energy.a), d};
		}
		/* .check_ko */
		CheckIfDefendingPokemonCanKnockOutResult defending =
			CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, d, 0u, 0u);
		d = defending.d;
		if ((defending.f & 0x10u) == 0u)
			return (AIDecide_ScoopUpResult){defending.a, or_a_flags(defending.a), d};
		goto decide_switch;
	}
	if (deck_id == LEGENDARY_RONALD_DECK_ID) {
		/* .HandleLegendaryRonald */
		count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
		if (count.a < 3u)
			return (AIDecide_ScoopUpResult){count.a, or_a_flags(count.a), d};
		LookForCardIDInPlayAreaResult bench = LookForCardIDInPlayArea_Bank8(ARTICUNO_LV37, PLAY_AREA_BENCH_1);
		if (bench.f & 0x10u) {
			slot = bench.a;
			goto articuno_bench;
		}
		bench = LookForCardIDInPlayArea_Bank8(ZAPDOS_LV68, PLAY_AREA_BENCH_1);
		if (bench.f & 0x10u) {
			slot = bench.a;
			goto check_attached_energy;
		}
		bench = LookForCardIDInPlayArea_Bank8(MOLTRES_LV37, PLAY_AREA_BENCH_1);
		if (bench.f & 0x10u) {
			slot = bench.a;
			goto check_attached_energy;
		}
		return (AIDecide_ScoopUpResult){bench.a, or_a_flags(bench.a), d};
	}

	{
		CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
		d = ko.d;
		if (ko.f & 0x10u) {
			CheckIfSelectedAttackIsUnusableResult unusable =
				CheckIfSelectedAttackIsUnusable(ko.a, ko.f, 0u, 0u, d, 0u, 0u);
			d = unusable.d;
			if ((unusable.f & 0x10u) == 0u)
				return (AIDecide_ScoopUpResult){unusable.a, or_a_flags(unusable.a), d};
			LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
			d = energy.d;
			if (energy.f & 0x10u)
				return (AIDecide_ScoopUpResult){energy.a, or_a_flags(energy.a), d};
		}
	}
	/* .cannot_ko */
	{
		uint8_t status = (uint8_t)(GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a & CNF_SLP_PRZ);
		if (status != PARALYZED && status != ASLEEP) {
			hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
			uint8_t cost = GetPlayAreaCardRetreatCost();
			/* GetLoadedCard1RetreatCost walks the bench (non-empty here) through
			 * GetCardIDFromDeckIndex. */
			d = 0u;
			uint8_t attached = CountNumberOfEnergyCardsAttached(PLAY_AREA_ARENA).a;
			if (attached >= cost)
				return (AIDecide_ScoopUpResult){attached, or_a_flags(attached), d};
		}
	}
	/* .cannot_retreat */
	{
		DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
		(void)LoadCardDataToBuffer1_FromDeckIndex(arena.a);
		uint8_t counters = ConvertHPToDamageCounters_Bank8(wLoadedCard1HP);
		d = counters;
		CardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
		if (damage.a == 0u)
			return (AIDecide_ScoopUpResult){0u, 0x80u, d};
		uint8_t ratio = CalculateBDividedByA_Bank8(counters, damage.a).a;
		if (ratio < 7u)
			return (AIDecide_ScoopUpResult){ratio, or_a_flags(ratio), d};
	}
decide_switch:
	{
		AIDecideBenchPokemonToSwitchToResult choice = AIDecideBenchPokemonToSwitchTo(d);
		d = choice.d;
		if (choice.f & 0x10u)
			return (AIDecide_ScoopUpResult){choice.a, or_a_flags(choice.a), d};
		wce1a = choice.a;
		/* `xor a; scf` */
		return (AIDecide_ScoopUpResult){0u, 0x90u, d};
	}
articuno_bench:
	{
		/* `push af` keeps the bench slot around the defender's id lookup. */
		CardId defender_id = GetCardIDFromDeckIndex(GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
		d = 0u;
		if (defender_id == SNORLAX)
			return (AIDecide_ScoopUpResult){(uint8_t)defender_id, or_a_flags((uint8_t)defender_id), d};
	}
check_attached_energy:
	{
		/* `push af` / `pop bc` keep the slot; the Z flag is the energy count's. */
		uint8_t attached = CountNumberOfEnergyCardsAttached(slot).a;
		if (attached != 0u)
			return (AIDecide_ScoopUpResult){slot, or_a_flags(slot), d};
		/* .no_energy */
		wce1a = 0xffu;
		return (AIDecide_ScoopUpResult){slot, 0x90u, d};
	}
}
/* <<< factory AIDecide_ScoopUp */
/* >>> factory AIDecide_FullHeal */
AIDecideFullHealResult AIDecide_FullHeal(uint8_t d)
{
	uint8_t status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
	if (status == 0u)
		return (AIDecideFullHealResult){0u, 0x80u, d};
	status &= CNF_SLP_PRZ;
	if (status != PARALYZED && status != ASLEEP && status != CONFUSED)
		return (AIDecideFullHealResult){status, 0x10u, d};
	if (status == ASLEEP) {
		LookForCardIDInPlayAreaResult ghost;
		SwapTurn();
		ghost = LookForCardIDInPlayArea_Bank8(GASTLY_LV8, PLAY_AREA_ARENA);
		SwapTurn();
		if (ghost.f & 0x10u)
			return (AIDecideFullHealResult){ghost.a, (uint8_t)((ghost.f & 0x80u) | 0x10u), d};
		SwapTurn();
		ghost = LookForCardIDInPlayArea_Bank8(GASTLY_LV17, PLAY_AREA_ARENA);
		SwapTurn();
		if (ghost.f & 0x10u)
			return (AIDecideFullHealResult){ghost.a, (uint8_t)((ghost.f & 0x80u) | 0x10u), d};
		SwapTurn();
		ghost = LookForCardIDInPlayArea_Bank8(HAUNTER_LV22, PLAY_AREA_ARENA);
		SwapTurn();
		if (ghost.f & 0x10u)
			return (AIDecideFullHealResult){ghost.a, (uint8_t)((ghost.f & 0x80u) | 0x10u), d};
	}
	LookForCardIDInHandListResult hand = LookForCardIDInHandList_Bank8(SCOOP_UP);
	d = hand.d;
	if (hand.f & 0x10u) {
		AIDecide_ScoopUpResult scoop = AIDecide_ScoopUp(d);
		d = scoop.d;
		if (scoop.f & 0x10u)
			return (AIDecideFullHealResult){scoop.a, or_a_flags(scoop.a), d};
	}
	uint8_t saved_status = 0u;
	DuelistVarResult status_var = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
	if (status == PARALYZED || status == ASLEEP) {
		saved_status = status_var.a;
		gb_write8(status_var.hl, NO_STATUS);
	}
	CheckIfCanDamageDefendingPokemonResult damage =
		CheckIfCanDamageDefendingPokemon(PLAY_AREA_ARENA, 0x80u, 0u, 0u, d, 0u, 0u);
	d = damage.d;
	if (status == PARALYZED || status == ASLEEP)
		gb_write8(status_var.hl, saved_status);
	if (status == CONFUSED) {
		if ((damage.f & 0x10u) == 0u)
			return (AIDecideFullHealResult){damage.a, or_a_flags(damage.a), d};
		if (wAIPlayEnergyCardForRetreat != 0u)
			return (AIDecideFullHealResult){wAIPlayEnergyCardForRetreat, 0x10u, d};
		return (AIDecideFullHealResult){0u, 0x80u, d};
	}
	if (damage.f & 0x10u)
		return (AIDecideFullHealResult){damage.a, (uint8_t)((damage.f & 0x80u) | 0x10u), d};
	uint8_t energy_for_retreat = wAIPlayEnergyCardForRetreat;
	if (energy_for_retreat != 0u)
		return (AIDecideFullHealResult){energy_for_retreat, 0x10u, d};
	AIDecideWhetherToRetreatResult retreat = AIDecideWhetherToRetreat(d);
	d = retreat.d;
	if ((retreat.f & 0x10u) == 0u)
		return (AIDecideFullHealResult){retreat.a, (uint8_t)((retreat.f & 0x80u) | 0x10u), d};
	return (AIDecideFullHealResult){retreat.a, or_a_flags(retreat.a), d};
}
/* <<< factory AIDecide_FullHeal */
/* --- factory AIDecide_PlusPower_Phase13 */
/* === factory AIDecide_PokemonCenter */
/* >>> part AIDecide_PlusPower1 */
AIDecideParameterResult AIDecide_PlusPower1(uint8_t d)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
	d = ko.d;
	if ((ko.f & 0x10u) != 0u) {
		CheckIfSelectedAttackIsUnusableResult ko_attack =
			CheckIfSelectedAttackIsUnusable(ko.a, ko.f, 0u, 0u, d, 0u, 0u);
		d = ko_attack.d;
		if ((ko_attack.f & 0x10u) == 0u)
			return (AIDecideParameterResult){ko_attack.a, or_a_flags(ko_attack.a), d};
		LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
		d = energy.d;
		if ((energy.f & 0x10u) != 0u)
			return (AIDecideParameterResult){energy.a, or_a_flags(energy.a), d};
	}
	DuelistVarResult attacker = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	CardId attacking_id = GetCardIDFromDeckIndex(attacker.a);
	uint16_t temp_card_id = wTempTurnDuelistCardID_ADDR;
	card_id_write(&temp_card_id, attacking_id);
	SwapTurn();
	DuelistVarResult defender = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	CardId defending_id = GetCardIDFromDeckIndex(defender.a);
	d = 0u;
	temp_card_id = wTempNonTurnDuelistCardID_ADDR;
	card_id_write(&temp_card_id, defending_id);
	NoDamageOrEffectResult prevented =
		HandleNoDamageOrEffectSubstatus(d, (uint8_t)defending_id, defender.hl);
	d = prevented.d;
	SwapTurn();
	if ((prevented.f & 0x10u) != 0u)
		return (AIDecideParameterResult){prevented.e, or_a_flags(prevented.e), d};
	uint8_t attack = FIRST_ATTACK_OR_PKMN_POWER;
	for (;;) {
		wSelectedAttack = attack;
		uint8_t exit_a;
		uint8_t kos_with_pluspower = 0u;
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(attack, 0u, 0u, 0u, d, 0u, 0u);
		d = unusable.d;
		if ((unusable.f & 0x10u) != 0u) {
			exit_a = unusable.a;
		} else {
			d = EstimateDamage_VersusDefendingCard(wSelectedAttack).d;
			uint8_t hp = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
			uint8_t damage = wDamage;
			exit_a = (uint8_t)(hp - damage);
			if (hp >= damage && exit_a != 0u) {
				uint8_t boosted = (uint8_t)(damage + 10u);
				exit_a = (uint8_t)(hp - boosted);
				kos_with_pluspower = (uint8_t)(hp <= boosted);
			}
		}
		if (kos_with_pluspower != 0u) {
			if ((uint8_t)(wDamage + 10u) >= 30u) {
				SwapTurn();
				DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
				CardId defending = GetCardIDFromDeckIndex(arena.a);
				d = 0u;
				SwapTurn();
				if (defending == MR_MIME)
					return (AIDecideParameterResult){(uint8_t)defending, 0x00u, d};
			}
			if (attack == FIRST_ATTACK_OR_PKMN_POWER)
				return (AIDecideParameterResult){FIRST_ATTACK_OR_PKMN_POWER, 0x90u, d};
			return (AIDecideParameterResult){SECOND_ATTACK, 0x10u, d};
		}
		if (attack == SECOND_ATTACK)
			return (AIDecideParameterResult){exit_a, or_a_flags(exit_a), d};
		attack = SECOND_ATTACK;
	}
}
/* <<< part AIDecide_PlusPower1 */
/* >>> part AIDecide_PlusPower2 */
AIDecideParameterResult AIDecide_PlusPower2(uint8_t d)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfSelectedAttackIsUnusableResult unusable =
		CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, d, 0u, 0u);
	d = unusable.d;
	if ((unusable.f & 0x10u) != 0u)
		return (AIDecideParameterResult){unusable.a, or_a_flags(unusable.a), d};
	d = EstimateDamage_VersusDefendingCard(wSelectedAttack).d;
	uint8_t hp = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t left = (uint8_t)(hp - wDamage);
	if (hp <= wDamage)
		return (AIDecideParameterResult){left, or_a_flags(left), d};
	unusable = CheckIfSelectedAttackIsUnusable(left, 0x10u, 0u, 0u, d, 0u, 0u);
	d = unusable.d;
	if ((unusable.f & 0x10u) != 0u)
		return (AIDecideParameterResult){unusable.a, or_a_flags(unusable.a), d};
	d = EstimateDamage_VersusDefendingCard(wSelectedAttack).d;
	uint8_t minimum = wAIMinDamage;
	if (minimum < 10u)
		return (AIDecideParameterResult){minimum, or_a_flags(minimum), d};
	uint8_t roll = Random(10u);
	if (roll >= 3u)
		return (AIDecideParameterResult){roll, or_a_flags(roll), d};
	uint8_t boosted = (uint8_t)(wDamage + 10u);
	if (boosted < 30u)
		return (AIDecideParameterResult){boosted, 0x10u, d};
	SwapTurn();
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	CardId defender = GetCardIDFromDeckIndex(arena.a);
	d = 0u;
	SwapTurn();
	if (defender == MR_MIME)
		return (AIDecideParameterResult){(uint8_t)defender, 0x00u, d};
	return (AIDecideParameterResult){(uint8_t)defender, 0x10u, d};
}
/* <<< part AIDecide_PlusPower2 */
/* >>> factory AIPlay_GustOfWind */
AIDecideResult AIPlay_GustOfWind(uint8_t d, uint8_t e)
{
	uint8_t flags = wCurrentAIFlags;
	flags |= 0x10u;
	wCurrentAIFlags = flags;
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_GustOfWind */
/* --- factory AIDecide_SuperPotion_Phase11 */
/* >>> factory AIDecide_ProfessorOak */
/* .LookForEvolution: carry when a card in hand evolves the card in play area
 * location e; wce08 is set when any card of the deck could. */
static uint8_t oak_evolution_in_hand(uint8_t location)
{
	wce08 = 0u;
	for (uint8_t candidate = 0u; candidate < DECK_SIZE; candidate++) {
		if (CheckIfCanEvolveInto(candidate, location).f & 0x10u)
			continue;
		wce08 = TRUE;
		if (GetTurnDuelistVariable((uint8_t)(DUELVARS_CARD_LOCATIONS + candidate)).a == CARD_LOCATION_HAND)
			return 1u;
	}
	return 0u;
}

AIDecideParameterResult AIDecide_ProfessorOak(uint8_t d)
{
	uint8_t remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	if (remaining >= DECK_SIZE - 6u)
		return (AIDecideParameterResult){remaining, cp_flags(remaining, DECK_SIZE - 6u), d};

	uint8_t deck_id = wOpponentDeckID;
	if (deck_id == LEGENDARY_ARTICUNO_DECK_ID) {
		uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		if (count < 3u) {
			d = count;
			(void)CreateHandCardList(0u);
			uint8_t evolves = 0u;
			for (uint8_t location = PLAY_AREA_ARENA; location != count; location++) {
				uint8_t card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + location)).a;
				if (CheckForEvolutionInList(card, 0u, 0u, 0u).f & 0x10u) {
					evolves = 1u;
					break;
				}
			}
			if (!evolves)
				return (AIDecideParameterResult){count, 0x90u, count};
		}
		CountOppEnergyResult energy = CountOppEnergyCardsInHand(0u, 0u);
		if (energy.a >= 4u)
			return (AIDecideParameterResult){energy.a, or_a_flags(energy.a), d};
		(void)CreateHandCardList(0u);
		d = 0xC5u;
		uint16_t list = wDuelTempList_ADDR;
		(void)RemoveCardIDInList(&list, PROFESSOR_OAK);
		(void)RemoveCardIDInList(&list, PROFESSOR_OAK);
		for (;;) {
			uint8_t index = gb_read8(list++);
			if (index == 0xFFu)
				return (AIDecideParameterResult){0xFFu, 0x90u, d};
			CheckIfCardCanBePlayedResult playable = CheckIfCardCanBePlayed(index, d);
			d = playable.d;
			if ((playable.f & 0x10u) == 0u)
				return (AIDecideParameterResult){playable.a, or_a_flags(playable.a), d};
		}
	}

	if (deck_id == EXCAVATION_DECK_ID) {
		if (remaining >= 46u)
			return (AIDecideParameterResult){remaining, cp_flags(remaining, 46u), d};
		LookForCardIDInHandAndPlayAreaResult fossil = LookForCardIDInHandAndPlayArea(MYSTERIOUS_FOSSIL);
		d = 0xC5u;
		wce06 = (fossil.f & 0x10u) ? 0x1Eu : 0x50u;
	} else {
		if (deck_id == WONDERS_OF_SCIENCE_DECK_ID) {
			LookForCardIDInHandListResult found = LookForCardIDInHandList_Bank8(GRIMER);
			d = 0xC5u;
			if ((found.f & 0x10u) == 0u)
				found = LookForCardIDInHandList_Bank8(MUK);
			d = 0xC5u;
			if (found.f & 0x10u)
				return (AIDecideParameterResult){found.a, or_a_flags(found.a), d};
		}
		if (remaining >= DECK_SIZE - 14u)
			return (AIDecideParameterResult){remaining, cp_flags(remaining, DECK_SIZE - 14u), d};
		wce06 = 30u;
	}
	uint8_t hand = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	if (hand < 4u)
		wce06 = (uint8_t)(wce06 + 50u);
	else if (hand >= 9u)
		wce06 = (uint8_t)(wce06 - 30u);
	if (CreateEnergyCardListFromHand(0u).f & 0x10u)
		wce06 = (uint8_t)(wce06 + 40u);
	if ((CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK).f & 0x10u) == 0u
	    && (CountTurnDuelistPokemonWithActivePkmnPower(BLASTOISE).f & 0x10u) != 0u
	    && (LookForCardIDInHand(WATER_ENERGY).f & 0x10u) != 0u)
		wce06 = (uint8_t)(wce06 + 10u);
	(void)CreateHandCardList(0u);
	uint16_t list = wDuelTempList_ADDR;
	for (;;) {
		uint8_t index = gb_read8(list++);
		if (index == 0xFFu)
			break;
		(void)LoadCardDataToBuffer1_FromDeckIndex(index);
		if (wLoadedCard1Type >= TYPE_ENERGY)
			continue;
		if (wLoadedCard1Stage == 0u) {
			wce06 = (uint8_t)(wce06 + 10u);
			break;
		}
	}
	wce0f = 0u;
	gb_write8((uint16_t)(wce0f_ADDR + 1u), 0u);
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	for (uint8_t location = PLAY_AREA_ARENA; count != 0u; location++, count--) {
		if (oak_evolution_in_hand(location))
			wce0f = TRUE;
		if (wce08 == TRUE)
			gb_write8((uint16_t)(wce0f_ADDR + 1u), TRUE);
	}
	if (gb_read8((uint16_t)(wce0f_ADDR + 1u)) != 0u && wce0f == 0u)
		wce06 = (uint8_t)(wce06 + 10u);
	uint8_t score = wce06;
	if (score >= 60u)
		return (AIDecideParameterResult){score, (uint8_t)((score == 60u ? 0x80u : 0u) | 0x10u), 0u};
	return (AIDecideParameterResult){score, or_a_flags(score), 0u};
}
/* <<< factory AIDecide_ProfessorOak */
/* === factory AIDecide_Potion_Phase10 */
/* >>> part AIDecide_SuperPotion1 */
AIDecideParameterResult AIDecide_SuperPotion1(uint8_t d)
{
	AIDecideWhetherToRetreatResult retreat = AIDecideWhetherToRetreat(d);
	d = retreat.d;
	if ((retreat.f & 0x10u) != 0u)
		return (AIDecideParameterResult){retreat.a, or_a_flags(retreat.a), d};
	AICheckIfAttackIsHighRecoilResult recoil = AICheckIfAttackIsHighRecoil();
	d = recoil.d;
	if ((recoil.f & 0x10u) != 0u)
		return (AIDecideParameterResult){0u, 0x80u, d};
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	uint8_t e = PLAY_AREA_ARENA;
	(void)GetPlayAreaCardAttachedEnergies(e);
	if (wTotalAttachedEnergies == 0u)
		return (AIDecideParameterResult){0u, 0x80u, d};
	CheckIfDefendingPokemonCanKnockOutResult ko =
		CheckIfDefendingPokemonCanKnockOut(wTotalAttachedEnergies, 0x10u, 0u, 0u, d, e, 0u);
	d = ko.d;
	if ((ko.f & 0x10u) == 0u)
		return (AIDecideParameterResult){ko.a, or_a_flags(ko.a), d};
	d = ko.a;
	uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t damage = GetCardDamageAndMaxHP(e).a;
	if (damage >= 41u)
		damage = 40u;
	uint8_t total = (uint8_t)(hp + damage);
	uint8_t remaining = (uint8_t)(total - d);
	if (total < d || remaining == 0u)
		return (AIDecideParameterResult){remaining, or_a_flags(remaining), d};
	return (AIDecideParameterResult){e, 0x10u, d};
}
/* <<< part AIDecide_SuperPotion1 */
/* >>> part AIDecide_SuperPotion2 */
AIDecideParameterResult AIDecide_SuperPotion2(uint8_t d)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfDefendingPokemonCanKnockOutResult ko =
		CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, d, 0u, 0u);
	d = ko.d;
	uint8_t e = PLAY_AREA_ARENA;
	uint8_t prizes;
	if ((ko.f & 0x10u) != 0u) {
		d = ko.a;
		uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
		uint8_t damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA).a;
		if (damage >= 41u)
			damage = 40u;
		uint8_t total = (uint8_t)(hp + damage);
		uint8_t remaining = (uint8_t)(total - d);
		if (total >= d && remaining != 0u)
			return (AIDecideParameterResult){remaining, 0u, d};
		SwapTurn();
		prizes = CountPrizes();
		SwapTurn();
		e = (uint8_t)(prizes - 1u) == 0u ? PLAY_AREA_ARENA : PLAY_AREA_BENCH_1;
	}
	for (;;) {
		uint8_t card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
		if (card == 0xffu)
			return (AIDecideParameterResult){0xffu, 0xC0u, d};
		d = card;
		(void)GetPlayAreaCardAttachedEnergies(e);
		if (wTotalAttachedEnergies == 0u) {
			e++;
			continue;
		}
		wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, d, e, 0u);
		if ((unusable.f & 0x10u) == 0u &&
		    (CheckLoadedAttackFlag(ATTACK_FLAG3_ADDRESS | BOOST_IF_TAKEN_DAMAGE_F).f & 0x10u) != 0u) {
			e++;
			continue;
		}
		wSelectedAttack = SECOND_ATTACK;
		unusable = CheckIfSelectedAttackIsUnusable(SECOND_ATTACK, 0u, 0u, 0u, d, e, 0u);
		if ((unusable.f & 0x10u) == 0u &&
		    (CheckLoadedAttackFlag(ATTACK_FLAG3_ADDRESS | BOOST_IF_TAKEN_DAMAGE_F).f & 0x10u) != 0u) {
			e++;
			continue;
		}
		wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
		hTempPlayAreaLocation_ff9d = e;
		CheckEnergyNeededForAttackResult need = CheckEnergyNeededForAttack();
		if ((need.f & 0x10u) == 0u &&
		    (CheckEnergyNeededForAttackAfterDiscard().f & 0x10u) != 0u) {
			e++;
			continue;
		}
		wSelectedAttack = SECOND_ATTACK;
		hTempPlayAreaLocation_ff9d = e;
		need = CheckEnergyNeededForAttack();
		if ((need.f & 0x10u) == 0u &&
		    (CheckEnergyNeededForAttackAfterDiscard().f & 0x10u) != 0u) {
			e++;
			continue;
		}
		CardDamageResult card_damage = GetCardDamageAndMaxHP(e);
		if (card_damage.a < 40u) {
			e++;
			continue;
		}
		if (e != PLAY_AREA_ARENA) {
			SwapTurn();
			prizes = CountPrizes();
			SwapTurn();
			if ((uint8_t)(prizes - 1u) != 0u) {
				uint8_t chance = Random(10u);
				if (chance < 3u)
					return (AIDecideParameterResult){chance, or_a_flags(chance), d};
			}
			return (AIDecideParameterResult){e, 0x10u, d};
		}
		AICheckIfAttackIsHighRecoilResult recoil = AICheckIfAttackIsHighRecoil();
		if ((recoil.f & 0x10u) != 0u)
			return (AIDecideParameterResult){0u, 0x80u, d};
		return (AIDecideParameterResult){e, 0x10u, d};
	}
}
/* <<< part AIDecide_SuperPotion2 */
/* --- factory AIDecide_SuperPotion_Phase08 */
/* === factory AIDecide_ComputerSearch_Anger */
/* === factory AIDecide_ComputerSearch_FireCharge */
/* === factory AIDecide_ComputerSearch_RockCrusher */
/* === factory AIDecide_ComputerSearch_WondersOfScience */
/* === factory AIDecide_Lass */
/* === factory AIDecide_PokemonTrader_BlisteringPokemon */
/* === factory AIDecide_PokemonTrader_Flamethrower */
/* === factory AIDecide_PokemonTrader_FlowerGarden */
/* === factory AIDecide_PokemonTrader_LegendaryDragonite */
/* === factory AIDecide_PokemonTrader_LegendaryMoltres */
/* === factory AIDecide_PokemonTrader_LegendaryRonald */
/* === factory AIDecide_PokemonTrader_SoundOfTheWaves */
/* === factory AIDecide_PokemonTrader_StrangePower */
/* === factory AIDecide_Recycle */
/* === factory AIDecide_SuperEnergyRemoval */
/* === factory AIPlay_EnergyRetrieval */
/* === factory AIPlay_Pokedex */
/* === factory AIPlay_SuperEnergyRetrieval */
