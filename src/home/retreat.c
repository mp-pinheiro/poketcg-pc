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

#include "home/card_color.h"
#define CONFUSED 0x01u
#define DOUBLE_POISONED 0xC0u
#define DUELVARS_BENCH 0xBCu
#define HITMONLEE 0x87u
#define PLAY_AREA_BENCH_1 0x01u
#define PORYGON 0xBDu
#define TRUE 0x01u
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
				(void)AIMakeDecision(OPPACTION_PLAY_ENERGY, 0u, 0u, 0u, 0u);
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
		(void)AIMakeDecision(OPPACTION_USE_PKMN_POWER, 0u, 0u, 0u, 0u);
		hAIPkmnPowerEffectParam = entry_a;
		(void)AIMakeDecision(OPPACTION_EXECUTE_PKMN_POWER_EFFECT, 0u, 0u, 0u, 0u);
		(void)AIMakeDecision(OPPACTION_DUEL_MAIN_SCENE, 0u, 0u, 0u, 0u);
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
	/* retreat.asm .retreat: `or a` on what AIMakeDecision leaves in a. */
	AIMakeDecisionResult retreated = AIMakeDecision(OPPACTION_ATTEMPT_RETREAT, 0u, 0u, 0u, 0u);
	return (AITryToRetreatResult){retreated.a, retreated.a == 0u ? 0x80u : 0x00u};
}
/* <<< factory AITryToRetreat */

/* >>> factory AIDecideBenchPokemonToSwitchTo */
/* retreat.asm AIDecideBenchPokemonToSwitchTo. Scores every bench card from
 * 50 and hands the scores to FindHighestBenchScore; the arena card keeps 50
 * unscored. */
AIDecideBenchPokemonToSwitchToResult AIDecideBenchPokemonToSwitchTo(uint8_t d)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	/* `cp 2; ret c` keeps the entry d; every other exit is FindHighestBenchScore's. */
	if (count < 2u)
		return (AIDecideBenchPokemonToSwitchToResult){count, 0x70u, d};
	(void)SetAIRetreatFlags();
	LoadDefendingPokemonColorWRAndPrizeCards();
	wAIScore = 50u;
	gb_write8(wPlayAreaAIScore_ADDR, wAIScore);
	for (uint8_t location = PLAY_AREA_BENCH_1; location < count; ++location) {
		hTempPlayAreaLocation_ff9d = location;
		wAIScore = 50u;
		uint8_t skip_to_weakness = 0u;
		if (CheckIfAnyAttackKnocksOutDefendingCard().f & 0x10u) {
			if ((CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) == 0u) {
				(void)AIEncourage(10u);
				wAIRetreatFlags |= 1u;
				/* With prizes left the knockout alone decides: the damage,
				 * energy and Mr. Mime checks below are skipped (jp nc). */
				if (CountPrizes() >= 2u)
					skip_to_weakness = 1u;
				else
					(void)AIEncourage(10u);
			}
		}
		if (!skip_to_weakness) {
			/* .check_can_use_atks: AI score += floor(damage / 10) + 1 per usable attack */
			for (uint8_t attack = FIRST_ATTACK_OR_PKMN_POWER; attack <= SECOND_ATTACK; ++attack) {
				wSelectedAttack = attack;
				if ((CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) == 0u) {
					(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
					(void)AIEncourage((uint8_t)(ConvertHPToDamageCounters_Bank5(wDamage).a + 1u));
				}
			}
			/* .check_energy_card */
			if ((LookForEnergyNeededInHand() & 0x10u) != 0u) {
				(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
				(void)AIEncourage((uint8_t)(ConvertHPToDamageCounters_Bank5(wDamage).a >> 1));
			}
			/* .check_attached_energy */
			(void)GetPlayAreaCardAttachedEnergies(hTempPlayAreaLocation_ff9d);
			if (wTotalAttachedEnergies == 0u)
				AIDiscourage(1u);
			/* .check_mr_mime: worth more if it can get through Invisible Wall */
			DuelistVarResult defending = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD);
			SwapTurn();
			uint8_t defending_id = LoadCardDataToBuffer2_FromDeckIndex(defending.a);
			SwapTurn();
			if (defending_id == MR_MIME) {
				(void)EstimateDamage_VersusDefendingCard(FIRST_ATTACK_OR_PKMN_POWER);
				uint8_t damages = wDamage != 0u;
				if (!damages) {
					(void)EstimateDamage_VersusDefendingCard(SECOND_ATTACK);
					damages = wDamage != 0u;
				}
				if (damages)
					(void)AIEncourage(5u);
			}
		}
		/* .check_defending_weak .. .check_weakness */
		uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + location)).a;
		(void)LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		uint8_t color = TranslateColorToWR(wLoadedCard1Type);
		if (color & wAIPlayerWeakness)
			(void)AIEncourage(3u);
		if (color & wAIPlayerResistance)
			AIDiscourage(2u);
		if (wAIPlayerColor & wLoadedCard1Resistance)
			(void)AIEncourage(2u);
		if (wAIPlayerColor & wLoadedCard1Weakness)
			AIDiscourage(3u);
		/* .check_retreat_cost */
		uint8_t cost = GetPlayAreaCardRetreatCost();
		if (cost < 2u)
			(void)AIEncourage(1u);
		else if (cost > 2u)
			AIDiscourage(1u);
		/* .check_player_prize_count */
		if (wAIRetreatFlags != 0x81u
		    && (CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) != 0u)
			AIDiscourage(wAIPlayerPrizeCount == 1u ? 10u : 3u);
		/* .check_hp */
		uint8_t hp = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + location)).a;
		if (hp == 0u) {
			wAIScore = 0u;
			gb_write8((uint16_t)(wPlayAreaAIScore_ADDR + location), wAIScore);
			continue;
		}
		/* .add_hp_score: AI score += floor(HP / 40) */
		(void)AIEncourage(ConvertHPToDamageCounters_Bank5(CalculateBDividedByA_Bank5(4u, hp).a).a);
		uint8_t card = LoadCardDataToBuffer1_FromDeckIndex(
			GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + location)).a);
		uint8_t raise = card == MR_MIME;
		if (card == MEW_LV8) {
			(void)LoadCardDataToBuffer2_FromDeckIndex(GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
			raise = wLoadedCard2Stage != 0u;
		}
		if (raise)
			(void)AIEncourage(5u);
		if (wLoadedCard1AIInfo == AI_INFO_BENCH_UTILITY)
			AIDiscourage(2u);
		/* .mysterious_fossil_or_clefairy_doll; b for the bonus list below is
		 * what a holds: the card ID, or AIDiscourage's exit a after -10. */
		uint8_t listed_id = wLoadedCard1ID;
		if (listed_id == MYSTERIOUS_FOSSIL || listed_id == CLEFAIRY_DOLL) {
			uint8_t before = wAIScore;
			AIDiscourage(10u);
			listed_id = before == 0u ? 0u : (uint8_t)(before - 10u);
		}
		/* .ai_score_bonus: the deck's (card ID, score) list */
		uint8_t hi = gb_read8((uint16_t)(wAICardListRetreatBonus_ADDR + 1u));
		if (hi != 0u) {
			uint16_t list = (uint16_t)(((uint16_t)hi << 8) | gb_read8(wAICardListRetreatBonus_ADDR));
			for (;;) {
				uint8_t entry = gb_read8(list++);
				if (entry == 0u)
					break;
				if (entry == listed_id) {
					uint8_t bonus = gb_read8(list);
					if (bonus >= 0x80u)
						(void)AIEncourage((uint8_t)(bonus - 0x80u));
					else
						AIDiscourage((uint8_t)(0x80u - bonus));
				}
				list++;
			}
		}
		gb_write8((uint16_t)(wPlayAreaAIScore_ADDR + location), wAIScore);
	}
	wAIRetreatScore = 0u;
	FindHighestBenchScoreResult best = FindHighestBenchScore();
	return (AIDecideBenchPokemonToSwitchToResult){best.a, best.f, best.d};
}
/* <<< factory AIDecideBenchPokemonToSwitchTo */

/* >>> factory AIDecideWhetherToRetreat */
AIDecideWhetherToRetreatResult AIDecideWhetherToRetreat(uint8_t d)
{
	uint8_t a = wConfusionRetreatCheckWasUnsuccessful;
	uint8_t f;
	uint8_t b = 0u;
	uint8_t c = 0u;
	uint8_t e = 0u;
	uint16_t hl = 0u;
	if (a != 0u) {
		/* .no_carry: the second `or a` clears carry and sets Z only for zero;
		 * the entry d survives. Every later exit passes GetCardIDFromDeckIndex
		 * at .check_active_id, whose `ld d, $0` clears it. */
		return (AIDecideWhetherToRetreatResult){a, 0u, d};
	}
	wAIPlayEnergyCardForRetreat = 0u;
	LoadDefendingPokemonColorWRAndPrizeCards();
	wAIScore = 0x80u;
	a = wAIRetreatScore;
	if (a != 0u) {
		a = (uint8_t)((a >> 2) << 1);
		AIEncourageResult r = AIEncourage(a);
		a = r.a;
		f = r.f;
	}
	DuelistVarResult v = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
	a = v.a;
	hl = v.hl;
	if (a != 0u) {
		a &= DOUBLE_POISONED;
		if (a != 0u) {
			AIEncourageResult r = AIEncourage(2u);
			a = r.a;
			f = r.f;
		}
		a = gb_read8(hl);
		a &= CNF_SLP_PRZ;
		if (a == CONFUSED) {
			AIEncourageResult r = AIEncourage(1u);
			a = r.a;
			f = r.f;
		}
	}
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfAnyAttackKnocksOutDefendingCardResult any = CheckIfAnyAttackKnocksOutDefendingCard();
	a = any.a;
	f = any.f;
	/* retreat.asm:39-49: an attack that knocks out and is usable, or
	 * unusable only for an energy the hand holds, argues against retreating. */
	if ((f & 0x10u) != 0u) {
		CheckIfSelectedAttackIsUnusableResult unusable = CheckIfSelectedAttackIsUnusable(a, f, b, c, d, e, hl);
		a = unusable.a; f = unusable.f; b = unusable.b; c = unusable.c; d = unusable.d; e = unusable.e; hl = unusable.hl;
		if ((f & 0x10u) == 0u)
			goto active_cant_use_atk;
		LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
		a = energy.a; f = energy.f;
		if ((f & 0x10u) != 0u)
			goto active_cant_use_atk;
	}
	goto active_cant_ko_1;

active_cant_use_atk:
	AIDiscourage(5u);
	if (wAIOpponentPrizeCount < 2u)
		AIDiscourage(35u);

active_cant_ko_1:
	{
		/* retreat.asm:52-79. A non-boss deck leaves for .check_resistance_1
		 * right after the defender's knockout check: only a boss deck weighs
		 * the prize counts, and it plays an energy for the retreat when the
		 * defender can knock out and the player is on its last prize. */
		CheckIfDefendingPokemonCanKnockOutResult ko = CheckIfDefendingPokemonCanKnockOut(a, f, b, c, d, e, hl);
		a = ko.a; f = ko.f;
		uint8_t defender_can_ko = (f & 0x10u) != 0u;
		if (defender_can_ko) {
			AIEncourageResult r = AIEncourage(2u);
			a = r.a; f = r.f;
		}
		CheckIfNotABossDeckIDResult boss = CheckIfNotABossDeckID();
		a = boss.a; f = boss.carry ? 0x10u : 0u;
		if (!boss.carry) {
			if (wAIPlayerPrizeCount < 2u) {
				if (defender_can_ko)
					wAIPlayEnergyCardForRetreat = TRUE;
				AIEncourageResult r = AIEncourage(2u);
				a = r.a; f = r.f;
			}
			if (wAIOpponentPrizeCount < 2u)
				AIDiscourage(2u);
		}
	}

check_resistance_1:
	a = TranslateColorToWR(GetArenaCardColor());
	b = a;
	a = wAIPlayerResistance;
	if ((a & b) != 0u) {
		AIEncourageResult r = AIEncourage(1u);
		a = r.a; f = r.f;
		b = wAIPlayerResistance;
		v = GetTurnDuelistVariable(DUELVARS_BENCH);
		hl = v.hl;
		for (;;) {
			a = gb_read8(hl++);
			if (a == 0xFFu) {
				AIDiscourage(2u);
				break;
			}
			LoadCardDataToBuffer1_FromDeckIndex(a);
			if ((TranslateColorToWR(wLoadedCard1Type) & b) == 0u)
				break;
		}
	}

check_weakness_1:
	b = wAIPlayerColor;
	a = GetArenaCardWeakness();
	if ((a & b) != 0u) {
		AIEncourageResult r = AIEncourage(2u);
		a = r.a; f = r.f;
		b = wAIPlayerColor;
		v = GetTurnDuelistVariable(DUELVARS_BENCH);
		hl = v.hl;
		for (;;) {
			a = gb_read8(hl++);
			if (a == 0xFFu) {
				AIDiscourage(3u);
				break;
			}
			LoadCardDataToBuffer1_FromDeckIndex(a);
			if ((wLoadedCard1Weakness & b) == 0u)
				break;
		}
	}

check_resistance_2:
	b = wAIPlayerColor;
	a = GetArenaCardResistance();
	if ((a & b) != 0u)
		AIDiscourage(3u);

check_weakness_2:
	/* retreat.asm:137-167. The first bench card whose type is the player's
	 * weakness scores 2 and ends the scan: a Porygon arena that can damage
	 * adds 10 and skips .check_weakness_3, any other arena goes to it; a
	 * bench without such a card jumps straight to .check_resistance_3. */
	b = wAIPlayerWeakness;
	v = GetTurnDuelistVariable(DUELVARS_BENCH);
	hl = v.hl;
	e = PLAY_AREA_BENCH_1 - 1u;
	for (;;) {
		++e;
		a = gb_read8(hl++);
		if (a == 0xFFu)
			goto check_resistance_3;
		uint8_t saved_e = e;
		LoadCardDataToBuffer1_FromDeckIndex(a);
		a = TranslateColorToWR(wLoadedCard1Type);
		e = saved_e;
		if ((a & b) == 0u)
			continue;
		AIEncourageResult r = AIEncourage(2u);
		a = r.a; f = r.f;
		DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
		uint8_t arena_id = (uint8_t)GetCardIDFromDeckIndex(arena.a);
		if (arena_id != PORYGON)
			goto check_weakness_3;
		CheckIfCanDamageDefendingPokemonResult damage = CheckIfCanDamageDefendingPokemon(e, f, b, c, d, e, hl);
		a = damage.a; f = damage.f;
		if ((f & 0x10u) == 0u)
			goto check_weakness_3;
		r = AIEncourage(10u);
		a = r.a; f = r.f;
		goto check_resistance_3;
	}

check_weakness_3:
	b = TranslateColorToWR(GetArenaCardColor());
	a = wAIPlayerWeakness;
	if ((a & b) != 0u)
		AIDiscourage(3u);

check_resistance_3:
	b = wAIPlayerColor;
	v = GetTurnDuelistVariable(DUELVARS_BENCH);
	hl = v.hl;
	for (;;) {
		a = gb_read8(hl++);
		if (a == 0xFFu)
			break;
		LoadCardDataToBuffer1_FromDeckIndex(a);
		if ((wLoadedCard1Resistance & b) != 0u) {
			AIEncourageResult r = AIEncourage(1u);
			a = r.a; f = r.f;
			break;
		}
	}

check_ko_2:
	v = GetTurnDuelistVariable(DUELVARS_BENCH);
	hl = v.hl;
	c = 0u;
	for (;;) {
		++c;
		a = gb_read8(hl++);
		if (a == 0xFFu)
			break;
		hTempPlayAreaLocation_ff9d = c;
		/* retreat.asm .loop_ko_1 pushes hl and bc around the three checks:
		 * the bench pointer and slot counter survive whatever they leave. */
		CheckIfAnyAttackKnocksOutDefendingCardResult k = CheckIfAnyAttackKnocksOutDefendingCard();
		a = k.a; f = k.f;
		if ((f & 0x10u) == 0u)
			continue;
		CheckIfSelectedAttackIsUnusableResult u = CheckIfSelectedAttackIsUnusable(a, f, b, c, d, e, hl);
		a = u.a; f = u.f; d = u.d; e = u.e;
		if ((f & 0x10u) == 0u)
			goto bench_ko_success;
		LookForEnergyNeededForAttackInHandResult need = LookForEnergyNeededForAttackInHand();
		a = need.a; f = need.f;
		if ((f & 0x10u) != 0u)
			goto bench_ko_success;
	}
	goto check_defending_id;

bench_ko_success:
	{
		AIEncourageResult r = AIEncourage(2u);
		a = r.a; f = r.f;
	}
	if (wAIOpponentPrizeCount < 2u) {
		CheckIfNotABossDeckIDResult boss = CheckIfNotABossDeckID();
		a = boss.a; f = boss.carry ? 0x10u : 0u;
		if (!boss.carry) {
			hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
			CheckIfAnyAttackKnocksOutDefendingCardResult k = CheckIfAnyAttackKnocksOutDefendingCard();
			a = k.a; f = k.f;
			if ((f & 0x10u) == 0u)
				goto check_defending_id;
			CheckIfSelectedAttackIsUnusableResult u = CheckIfSelectedAttackIsUnusable(a, f, b, c, d, e, hl);
			a = u.a; f = u.f; b = u.b; c = u.c; d = u.d; e = u.e; hl = u.hl;
			if ((f & 0x10u) == 0u)
				goto check_defending_id;
			AIEncourageResult r = AIEncourage(40u);
			a = r.a; f = r.f;
			wAIPlayEnergyCardForRetreat = TRUE;
		}
	}

check_defending_id:
	v = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD);
	SwapTurn();
	uint8_t defending_id = (uint8_t)GetCardIDFromDeckIndex(v.a);
	SwapTurn();
	if (defending_id == MR_MIME || defending_id == HITMONLEE) {
		hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
		CheckIfCanDamageDefendingPokemonResult damage = CheckIfCanDamageDefendingPokemon(0u, f, b, c, d, e, hl);
		a = damage.a; f = damage.f;
		if ((f & 0x10u) == 0u) {
			v = GetTurnDuelistVariable(DUELVARS_BENCH);
			hl = v.hl; c = 0u;
			for (;;) {
				++c; a = gb_read8(hl++);
				if (a == 0xFFu)
					break;
				CheckIfCanDamageDefendingPokemonResult bd = CheckIfCanDamageDefendingPokemon(c, f, b, c, d, e, hl);
				a = bd.a; f = bd.f;
				if ((f & 0x10u) != 0u) {
					AIEncourageResult r = AIEncourage(5u);
					a = r.a; f = r.f;
					wAIPlayEnergyCardForRetreat = TRUE;
					break;
				}
			}
		}
	}

check_retreat_cost:
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	a = GetPlayAreaCardRetreatCost();
	if (a == 2u)
		AIDiscourage(1u);
	else if (a >= 3u)
		AIDiscourage(2u);
	CheckIfArenaCardIsFullyPoweredResult powered = CheckIfArenaCardIsFullyPowered();
	a = powered.a; f = powered.f;
	if ((f & 0x10u) == 0u) {
		CountNumberOfSetUpBenchPokemonResult count = CountNumberOfSetUpBenchPokemon(a, f, b, c, d, e, hl);
		a = count.a; f = count.f; b = count.b; c = count.c; d = count.d; e = count.e; hl = count.hl;
		if (a >= 2u)
			AIEncourage(1u);
	}
	v = GetTurnDuelistVariable(DUELVARS_BENCH);
	hl = v.hl; e = 0u;
	for (;;) {
		++e; a = gb_read8(hl++);
		if (a == 0xFFu) {
			AIDiscourage(20u);
			break;
		}
		uint8_t saved_e = e;
		LoadCardDataToBuffer2_FromDeckIndex(a);
		e = saved_e;
		if (wLoadedCard2ID == MYSTERIOUS_FOSSIL || wLoadedCard2ID == CLEFAIRY_DOLL)
			continue;
		hTempPlayAreaLocation_ff9d = e;
		CheckIfDefendingPokemonCanKnockOutResult ko = CheckIfDefendingPokemonCanKnockOut(a, f, b, c, d, e, hl);
		a = ko.a; f = ko.f;
		if ((f & 0x10u) == 0u)
			goto check_active_id;
	}

check_active_id:
	v = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint8_t active_id = (uint8_t)GetCardIDFromDeckIndex(v.a);
	d = 0u;
	if (active_id == MYSTERIOUS_FOSSIL || active_id == CLEFAIRY_DOLL) {
		e = 0u;
		for (;;) {
			++e;
			v = GetTurnDuelistVariable((uint8_t)(e + DUELVARS_ARENA_CARD));
			if (v.a == 0xFFu)
				return (AIDecideWhetherToRetreatResult){0xFFu, 0u, d};
			hTempPlayAreaLocation_ff9d = e;
			CheckIfDefendingPokemonCanKnockOutResult ko = CheckIfDefendingPokemonCanKnockOut(a, f, b, c, d, e, hl);
			a = ko.a; f = ko.f;
			if ((f & 0x10u) != 0u)
				continue;
			CheckIfCanDamageDefendingPokemonResult damage = CheckIfCanDamageDefendingPokemon(e, f, b, c, d, e, hl);
			a = damage.a; f = damage.f;
			if ((f & 0x10u) != 0u)
				return (AIDecideWhetherToRetreatResult){a, (uint8_t)((f & 0x80u) | 0x10u), d};
		}
	}
	a = wAIScore;
	if (a >= 131u)
		return (AIDecideWhetherToRetreatResult){a, (uint8_t)((a == 131u ? 0x80u : 0u) | 0x10u), d};
	return (AIDecideWhetherToRetreatResult){a, (uint8_t)(a == 0u ? 0x80u : 0u), d};
}
/* <<< factory AIDecideWhetherToRetreat */
