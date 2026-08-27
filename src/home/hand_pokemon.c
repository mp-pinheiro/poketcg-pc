#include "home/hand_pokemon.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/common.h"
#include "home/substatus.h"
#include "home/duel.h"

#define CHARMELEON 0x31u
#define DRAGONAIR 0xC0u
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xEFu
#define GRIMER 0x26u
#define INVINCIBLE_RONALD_DECK_ID 0x1Au
#define LEGENDARY_DRAGONITE_DECK_ID 0x0Fu
#define LEGENDARY_RONALD_DECK_ID 0x1Bu
#define MAGIKARP 0x57u
#define MUK 0x27u
#define PLAY_AREA_ARENA 0x00u

#include "home/retreat.h"

#define LEGENDARY_ARTICUNO_DECK_ID 0x0Eu
#define LEGENDARY_ZAPDOS_DECK_ID 0x0Du
#define ARTICUNO_LV37 0x5Fu
#define CNF_SLP_PRZ 0x0Fu
#define DUELVARS_ARENA_CARD 0xBBu
#define DUELVARS_ARENA_CARD_STATUS 0xF0u
#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK 0xBAu
#define FIRST_ATTACK_OR_PKMN_POWER 0x00u
#define MAX_BENCH_POKEMON 0x05u
#define MOLTRES_LV37 0x40u
#define POKEMON_POWER 0x04u
#define SNORLAX 0xBEu
#define ZAPDOS_LV68 0x76u
/* <<< factory statics */

/* >>> factory AIDecideSpecialEvolutions */
void AIDecideSpecialEvolutions(void)
{
	uint8_t deck = wOpponentDeckID;
	if (deck == LEGENDARY_DRAGONITE_DECK_ID) {
		uint8_t card = wLoadedCard2ID;
		if (card == CHARMELEON) {
			uint8_t location = hTempPlayAreaLocation_ff9d;
			CountNumberOfEnergyCardsAttachedResult attached =
				CountNumberOfEnergyCardsAttached(location);
			if (attached.a < 3u) {
				AIDiscourage(10u);
				return;
			}
			CountOppEnergyResult hand = CountOppEnergyCardsInHand(0u, 0u);
			if ((uint8_t)(attached.a + hand.a) < 6u)
				AIDiscourage(10u);
			else
				(void)AIEncourage(3u);
			return;
		}
		if (card == MAGIKARP) {
			uint8_t location = hTempPlayAreaLocation_ff9d;
			if (location == 0u)
				return;
			CountNumberOfEnergyCardsAttachedResult attached =
				CountNumberOfEnergyCardsAttached(location);
			if (attached.a >= 2u)
				(void)AIEncourage(3u);
			return;
		}
		if (card != DRAGONAIR)
			return;
	} else if (deck == INVINCIBLE_RONALD_DECK_ID) {
		if (wLoadedCard2ID != GRIMER)
			return;
		if (hTempPlayAreaLocation_ff9d == 0u)
			return;
		(void)AIEncourage(10u);
		return;
	} else if (deck != LEGENDARY_RONALD_DECK_ID || wLoadedCard2ID != DRAGONAIR) {
		return;
	}

	uint8_t location = hTempPlayAreaLocation_ff9d;
	if (location != 0u) {
		uint8_t count = GetTurnDuelistVariable(
			DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		uint8_t total = 0u;
		while (count != 0u) {
			--count;
			CardDamageResult damage = GetCardDamageAndMaxHP(count);
			total = (uint8_t)(total + damage.a);
		}
		if (total < 70u) {
			AIDiscourage(10u);
			return;
		}
		PkmnPowerCountResult muk =
			CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
		if ((muk.f & 0x10u) != 0u) {
			AIDiscourage(10u);
			return;
		}
		(void)AIEncourage(10u);
		return;
	}

	CardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	if (damage.a < 50u) {
		AIDiscourage(10u);
		return;
	}
	(void)GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	if (wTotalAttachedEnergies < 3u) {
		AIDiscourage(10u);
		return;
	}
	PkmnPowerCountResult muk =
		CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	if ((muk.f & 0x10u) != 0u)
		AIDiscourage(10u);
	else
		(void)AIEncourage(10u);
}
/* <<< factory AIDecideSpecialEvolutions */

/* >>> factory AIDecideEvolution */
uint8_t AIDecideEvolution(void)
{
	uint8_t result = 0xffu;
	return result;
}
/* <<< factory AIDecideEvolution */

/* >>> factory AIDecidePlayLegendaryBirds */
void AIDecidePlayLegendaryBirds(void)
{
	uint8_t deck = wOpponentDeckID;
	if (deck != LEGENDARY_ZAPDOS_DECK_ID &&
		deck != LEGENDARY_ARTICUNO_DECK_ID &&
		deck != LEGENDARY_RONALD_DECK_ID)
		return;

	uint8_t card = wLoadedCard1ID;
	if (card == ARTICUNO_LV37) {
		if (GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a < 2u)
			return;
		CheckIfActiveCardCanKnockOutResult knock =
			CheckIfActiveCardCanKnockOut(0u, 0u, 0u, 0u, 0u, 0u, 0u);
		if ((knock.f & 0x10u) != 0u) {
			AIDiscourage(100u);
			return;
		}
		CanArenaCardUseNonResidualAttackResult attack =
			CanArenaCardUseNonResidualAttack(knock.a, knock.f, knock.b, knock.c,
				knock.d, knock.e, knock.hl);
		if ((attack.f & 0x10u) == 0u) {
			AIDiscourage(100u);
			return;
		}
		AIDecideWhetherToRetreatResult retreat = AIDecideWhetherToRetreat();
		if ((retreat.f & 0x10u) != 0u) {
			AIDiscourage(100u);
			return;
		}
		if ((GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a & CNF_SLP_PRZ) != 0u) {
			AIDiscourage(100u);
			return;
		}
		SwapTurn();
		uint8_t arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
		(void)CopyAttackDataAndDamage_FromDeckIndex(arena, FIRST_ATTACK_OR_PKMN_POWER);
		SwapTurn();
		if (wLoadedAttackCategory == POKEMON_POWER)
			goto check_muk_and_snorlax;
		if (GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a >= MAX_BENCH_POKEMON)
			return;

	check_muk_and_snorlax:
		if ((CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK).f & 0x10u) != 0u) {
			AIDiscourage(100u);
			return;
		}
		uint8_t opponent_arena =
			GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
		SwapTurn();
		uint8_t opponent_card = (uint8_t)GetCardIDFromDeckIndex(opponent_arena);
		SwapTurn();
		if (opponent_card == SNORLAX) {
			AIDiscourage(100u);
			return;
		}
		(void)AIEncourage(70u);
		return;
	}
	if (card == MOLTRES_LV37) {
		if (GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a >= 56u)
			AIDiscourage(100u);
		return;
	}
	if (card == ZAPDOS_LV68 &&
		(CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK).f & 0x10u) != 0u)
		AIDiscourage(100u);
}
/* <<< factory AIDecidePlayLegendaryBirds */
