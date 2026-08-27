#include "home/retreat.h"

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/card_data.h"
#include "home/core.h"
#include "home/duel.h"
#include "generated/hram.h"

#define ASLEEP 0x02u
#define CLEFAIRY_DOLL 0xCBu
#define CNF_SLP_PRZ 0x0Fu
#define DOUBLE_COLORLESS_ENERGY 0x07u
#define DUELVARS_ARENA_CARD 0xBBu
#define DUELVARS_ARENA_CARD_STATUS 0xF0u
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xEFu
#define FLAG_C 0x10u
#define FLAG_Z 0x80u
#define MYSTERIOUS_FOSSIL 0xCCu
#define OPPACTION_ATTEMPT_RETREAT 0x04u
#define OPPACTION_DUEL_MAIN_SCENE 0x16u
#define OPPACTION_EXECUTE_PKMN_POWER_EFFECT 0x0Du
#define OPPACTION_PLAY_ENERGY 0x03u
#define OPPACTION_USE_PKMN_POWER 0x0Cu
#define PARALYZED 0x03u
#define PLAY_AREA_ARENA 0x00u
#define TYPE_ENERGY 0x08u

#include "home/core.h"
#include "home/duel.h"
#include "generated/hram.h"
#define FIRST_ATTACK_OR_PKMN_POWER 0x00u
#define SECOND_ATTACK 0x01u
#define MR_MIME 0x9Bu
#define MEW_LV8 0xA0u
#define DUELVARS_ARENA_CARD_HP 0xC8u
#define AI_INFO_BENCH_UTILITY 0x01u
/* <<< factory statics */

#define POKEMON_POWER 0x04u
#define OPPONENT_TURN ((uint8_t)(wOpponentDuelVariables_ADDR >> 8))

static uint8_t flag_cp(uint8_t a, uint8_t value)
{
	uint8_t f = 0x40u;
	if (a == value)
		f |= 0x80u;
	if ((a & 0x0fu) < (value & 0x0fu))
		f |= 0x20u;
	if (a < value)
		f |= 0x10u;
	return f;
}

SetAIRetreatFlagsResult SetAIRetreatFlags(void)
{
	gb_write8(wAIRetreatFlags_ADDR, 0);
	uint8_t turn = gb_read8(wWhoseTurn_ADDR);
	if (turn == OPPONENT_TURN) {
		uint8_t tried = gb_read8(wAITriedAttack_ADDR);
		uint8_t f = tried ? 0x00u : 0x80u;
		if (tried)
			return (SetAIRetreatFlagsResult){tried, f};
		gb_write8(wAIRetreatFlags_ADDR, 0x80u);
		return (SetAIRetreatFlagsResult){0x80u, f};
	}

	uint8_t category = gb_read8(wLoadedAttackCategory_ADDR);
	uint8_t f = flag_cp(category, POKEMON_POWER);
	if (category == POKEMON_POWER)
		return (SetAIRetreatFlagsResult){category, f};
	gb_write8(wAIRetreatFlags_ADDR, 0x80u);
	return (SetAIRetreatFlagsResult){0x80u, f};
}

/* >>> factory AITryToRetreat */
/* engine/duel/ai/retreat.asm:775-1012. The entry `push af` is popped exactly
 * once on every path, so the frame balances and the caller's a/f -- the Play
 * Area location to retreat to -- arrive as parameters instead of on the stack. */
AITryToRetreatResult AITryToRetreat(uint8_t entry_a, uint8_t entry_f)
{
	if (wAIPlayEnergyCardForRetreat != 0u) {
		uint8_t gate = (uint8_t)(GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a & CNF_SLP_PRZ);
		if (gate != ASLEEP && gate != PARALYZED && wAlreadyPlayedEnergy == 0u) {
			uint8_t attached = CountNumberOfEnergyCardsAttached(PLAY_AREA_ARENA).a;
			hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
			uint8_t retreat_cost = GetPlayAreaCardRetreatCost();
			/* `pop bc` puts the attached count in b; `cp b` / `jr c` / `jr z`
			 * keep only a cost strictly above it, and `sub b` / `cp 1` only a
			 * gap of exactly one energy. `a` is that 1 at the call below. */
			if (retreat_cost > attached &&
			    (uint8_t)(retreat_cost - attached) == 1u &&
			    (CreateEnergyCardListFromHand(1u).f & FLAG_C) == 0u) {
				hTemp_ffa0 = wDuelTempList;
				hTempPlayAreaLocation_ffa1 = PLAY_AREA_ARENA;
				(void)AIMakeDecision(OPPACTION_PLAY_ENERGY);
			}
		}
	}

	/* .check_id */
	uint8_t arena_id = (uint8_t)GetCardIDFromDeckIndex(
		GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
	if (arena_id == MYSTERIOUS_FOSSIL || arena_id == CLEFAIRY_DOLL) {
		if (GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a < 2u) {
			/* No bench: `pop af` then `scf` hands the caller's own a back
			 * with its Z untouched and carry set. */
			return (AITryToRetreatResult){entry_a,
				(uint8_t)((entry_f & FLAG_Z) | FLAG_C)};
		}
		hTempCardIndex_ff9f = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
		hTemp_ffa0 = PLAY_AREA_ARENA;
		(void)AIMakeDecision(OPPACTION_USE_PKMN_POWER);
		hAIPkmnPowerEffectParam = entry_a;
		(void)AIMakeDecision(OPPACTION_EXECUTE_PKMN_POWER_EFFECT);
		(void)AIMakeDecision(OPPACTION_DUEL_MAIN_SCENE);
		/* `or a` over AIMakeDecision's exit a, which AIMakeDecisionResult does
		 * not carry; the landed convention (HandleAIShift, HandleAIPeek,
		 * AIAttachEnergyInHandToCardInPlayArea) passes the oppaction byte
		 * through, and it is non-zero, so every flag clears. */
		return (AITryToRetreatResult){OPPACTION_DUEL_MAIN_SCENE, 0x00u};
	}

	hTempPlayAreaLocation_ffa1 = entry_a;
	uint8_t status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
	uint8_t cnf_slp_prz = (uint8_t)(status & CNF_SLP_PRZ);
	if (cnf_slp_prz == ASLEEP || cnf_slp_prz == PARALYZED) {
		/* .set_carry: the `cp` that matched left Z set and `scf` keeps it. */
		return (AITryToRetreatResult){cnf_slp_prz, (uint8_t)(FLAG_Z | FLAG_C)};
	}
	hTemp_ffa0 = status;
	hTempRetreatCostCards = 0xffu;
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	uint8_t cost = GetPlayAreaCardRetreatCost();
	wTempCardRetreatCost = cost;
	if (cost != 0u) {
		uint16_t de = hTempRetreatCostCards_ADDR;
		(void)CreateArenaOrBenchEnergyCardList(PLAY_AREA_ARENA);
		(void)GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
		if (cost == wTotalAttachedEnergies) {
			/* .loop_1: exactly enough energy attached, so the whole list --
			 * its $ff terminator included -- becomes the payment. */
			uint16_t src = wDuelTempList_ADDR;
			uint8_t index;
			do {
				index = gb_read8(src++);
				gb_write8(de++, index);
			} while (index != 0xffu);
		} else {
			/* .choose_energy_discard */
			uint16_t hl = wDuelTempList_ADDR;
			uint8_t deck_index = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
			uint8_t id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
			uint8_t c;
			wTempCardID = id;
			LoadCardDataToBuffer1_FromCardID(id);
			wTempCardType = (uint8_t)(wLoadedCard1Type | TYPE_ENERGY);
			c = wTempCardRetreatCost;
			/* .loop_2: each Double Colorless Energy pays two of the cost. */
			while (c >= 2u) {
				uint8_t index = gb_read8(hl++);
				if (index == 0xffu)
					break;
				gb_write8(de, index);
				if ((uint8_t)GetCardIDFromDeckIndex(index) != DOUBLE_COLORLESS_ENERGY)
					continue;
				(void)RemoveCardFromDuelTempList(gb_read8(de));
				hl--;
				de++;
				c = (uint8_t)(c - 2u);
				if (c == 0u)
					goto end_retreat_list;
			}
			/* .loop_3: shuffle what is left and spend the energies this
			 * Pokemon has no use for. */
			hl = wDuelTempList_ADDR;
			(void)ShuffleCards(CountCardsInDuelTempList().a, hl);
			for (;;) {
				uint8_t index = gb_read8(hl++);
				if (index == 0xffu)
					break;
				gb_write8(de, index);
				if ((CheckIfEnergyIsUseful(index).f & FLAG_C) != 0u)
					continue;
				(void)RemoveCardFromDuelTempList(gb_read8(de));
				hl--;
				de++;
				c = (uint8_t)(c - 1u);
				if (c == 0u)
					goto end_retreat_list;
			}
			/* .any_energy: anything at all, until the cost is covered. */
			hl = wDuelTempList_ADDR;
			for (;;) {
				uint8_t index = gb_read8(hl++);
				if (index == 0xffu) {
					/* .set_carry: the list ran out first. */
					return (AITryToRetreatResult){0xffu,
						(uint8_t)(FLAG_Z | FLAG_C)};
				}
				gb_write8(de++, index);
				if ((uint8_t)GetCardIDFromDeckIndex(index) == DOUBLE_COLORLESS_ENERGY) {
					c = (uint8_t)(c - 1u);
					if (c == 0u)
						break;
				}
				c = (uint8_t)(c - 1u);
				if (c == 0u)
					break;
			}
end_retreat_list:
			gb_write8(de, 0xffu);
		}
	}
	(void)AIMakeDecision(OPPACTION_ATTEMPT_RETREAT);
	return (AITryToRetreatResult){OPPACTION_ATTEMPT_RETREAT, 0x00u};
}
/* <<< factory AITryToRetreat */

/* >>> factory AIDecideBenchPokemonToSwitchTo */
AIDecideBenchPokemonToSwitchToResult AIDecideBenchPokemonToSwitchTo(void)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	if (count < 2u)
		return (AIDecideBenchPokemonToSwitchToResult){count, 0x70u};
	(void)SetAIRetreatFlags();
	LoadDefendingPokemonColorWRAndPrizeCards();
	for (uint8_t location = 0u; location < count; ++location) {
		hTempPlayAreaLocation_ff9d = location;
		wAIScore = 50u;
		CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
		if ((ko.f & 0x10u) != 0u) {
			CheckIfSelectedAttackIsUnusableResult u = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
			if ((u.f & 0x10u) == 0u) {
				(void)AIEncourage(10u);
				wAIRetreatFlags |= 1u;
				if (CountPrizes() < 2u) (void)AIEncourage(10u);
			}
		}
		for (uint8_t attack = FIRST_ATTACK_OR_PKMN_POWER; attack <= SECOND_ATTACK; ++attack) {
			wSelectedAttack = attack;
			CheckIfSelectedAttackIsUnusableResult u = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
			if ((u.f & 0x10u) == 0u) {
				(void)EstimateDamage_VersusDefendingCard(attack);
				(void)AIEncourage((uint8_t)(ConvertHPToDamageCounters_Bank5(wDamage).a + 1u));
			}
		}
		if ((LookForEnergyNeededInHand() & 0x10u) != 0u) {
			(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
			(void)AIEncourage((uint8_t)(ConvertHPToDamageCounters_Bank5(wDamage).a >> 1));
		}
		(void)GetPlayAreaCardAttachedEnergies(hTempPlayAreaLocation_ff9d);
		if (wTotalAttachedEnergies == 0u) AIDiscourage(1u);
		DuelistVarResult nonturn = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD);
		SwapTurn();
		uint8_t opposing = LoadCardDataToBuffer2_FromDeckIndex(nonturn.a);
		SwapTurn();
		if (opposing == MR_MIME) (void)AIEncourage(5u);
		DuelistVarResult cardvar = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + location));
		uint8_t card = LoadCardDataToBuffer1_FromDeckIndex(cardvar.a);
		uint8_t mask = TranslateColorToWR(wLoadedCard1Type);
		if (mask & wAIPlayerWeakness) (void)AIEncourage(3u);
		if (mask & wAIPlayerResistance) AIDiscourage(2u);
		uint8_t cost = GetPlayAreaCardRetreatCost();
		if (cost < 2u) (void)AIEncourage(1u);
		else if (cost > 2u) AIDiscourage(1u);
		uint8_t hp = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + location)).a;
		if (hp == 0u) wAIScore = 0u;
		else { CalculateBDividedByAResult q = CalculateBDividedByA_Bank5(4u, hp); (void)AIEncourage(ConvertHPToDamageCounters_Bank5(q.a).a); }
		if (card == MR_MIME || card == MEW_LV8) (void)AIEncourage(5u);
		if (wLoadedCard1AIInfo == AI_INFO_BENCH_UTILITY) AIDiscourage(2u);
		if (wLoadedCard1ID == MYSTERIOUS_FOSSIL || wLoadedCard1ID == CLEFAIRY_DOLL) AIDiscourage(10u);
		uint8_t hi = gb_read8((uint16_t)(wAICardListRetreatBonus_ADDR + 1u));
		if (hi != 0u) {
			uint16_t p = (uint16_t)(((uint16_t)hi << 8) | gb_read8(wAICardListRetreatBonus_ADDR));
			for (;;) { uint8_t listed = gb_read8(p++); if (listed == 0u) break; if (listed == card) { uint8_t bonus = gb_read8(p); if (bonus >= 0x80u) (void)AIEncourage((uint8_t)(bonus - 0x80u)); else AIDiscourage((uint8_t)(0x80u - bonus)); } }
		}
		gb_write8((uint16_t)(wPlayAreaAIScore_ADDR + location), wAIScore);
	}
	wAIRetreatScore = 0u;
	FindHighestBenchScoreResult best = FindHighestBenchScore();
	return (AIDecideBenchPokemonToSwitchToResult){best.a, best.f};
}
/* <<< factory AIDecideBenchPokemonToSwitchTo */
