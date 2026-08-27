#include "home/energy.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/duel.h"

#define AI_ENERGY_FLAG_SKIP_ARENA_CARD 0x80u
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xefu
#define MAX_PLAY_AREA_POKEMON 0x06u
#define PLAY_AREA_ARENA 0x00u
#define PLAY_AREA_BENCH_1 0x01u

#include "home/duel.h"
#include "mem.h"

#include "home/duel.h"
#include "home/core.h"
#include "generated/wram.h"
#include "generated/hram.h"
#define CHARMANDER 0x30u
#define COLORLESS 0x06u
#define DOUBLE_COLORLESS_ENERGY 0x07u
#define DRATINI 0xbfu
#define DUELVARS_ARENA_CARD 0xbbu
#define GROWLITHE 0x36u
#define LEGENDARY_DRAGONITE_DECK_ID 0x0fu
#define FIRE_CHARGE_DECK_ID 0x17u
#define LEGENDARY_RONALD_DECK_ID 0x1bu

#include "home/energy.h"
#include "home/duel.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define CHARIZARD 0x32u
#define EXEGGUTOR 0x29u
#define FALSE 0x00u
#define TRUE 0x01u
#define FIGHTING_ENERGY 0x05u
#define FIRE_ENERGY 0x02u
#define GRASS_ENERGY 0x01u
#define LIGHTNING_ENERGY 0x04u
#define PSYCHIC_ENERGY 0x06u
#define WATER_ENERGY 0x03u
#define ZAPDOS_LV64 0x75u

#include "home/core.h"
#include "home/duel.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define DUELVARS_ARENA_CARD_510 0xBBu

#include "home/core.h"
#include "home/duel.h"
#include "home/energy.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define ATTACHED_ENERGY_BOOST_F_600 0x4u
#define ATTACK_FLAG2_ADDRESS_600 0x8u
#define DISCARD_ENERGY_F_600 0x3u
#define DOUBLE_COLORLESS_ENERGY_600 0x07u
#define FIRST_ATTACK_OR_PKMN_POWER_600 0x00u
#define SECOND_ATTACK_600 0x01u
#define OPPACTION_PLAY_ENERGY_600 0x03u

#define ATTACHED_ENERGY_BOOST_F 0x04u
#define ATTACK_FLAG2_ADDRESS 0x08u
#define DISCARD_ENERGY_F 0x03u
#define IGNORE_THIS_ATTACK_F 0x05u
#define MAX_ENERGY_BOOST_IS_LIMITED 0x02u

#include "home/core.h"
#include "home/duel.h"
#include "home/substatus.h"
#include "generated/wram.h"
#include "generated/hram.h"
#define AI_ENERGY_FLAG_SKIP_EVOLUTION 0x02u
#define AI_MEWTWO_MILL_F 0x07u
#define DOUBLE_POISONED 0xc0u
#define DUELVARS_ARENA_CARD_HP 0xc8u
#define DUELVARS_ARENA_CARD_STATUS 0xf0u
#define FIRST_ATTACK_OR_PKMN_POWER 0x00u
#define MUK 0x27u
#define POISONED 0x80u
#define SECOND_ATTACK 0x01u
#define VENUSAUR_LV67 0x0bu
/* <<< factory statics */

/* >>> factory RetrievePlayAreaAIScoreFromBackup1 */
/* energy.asm:71-84 */
Backup1Result RetrievePlayAreaAIScoreFromBackup1(void)
{
	uint16_t de = wPlayAreaAIScore_ADDR;
	uint16_t hl = wTempPlayAreaAIScore_ADDR;
	for (uint8_t b = MAX_PLAY_AREA_POKEMON; b != 0u; b--) {
		gb_write8(de, gb_read8(hl));
		hl = (uint16_t)(hl + 1u);
		de = (uint16_t)(de + 1u);
	}
	wAIScore = gb_read8(hl);
	return (Backup1Result){de, hl};
}
/* <<< factory RetrievePlayAreaAIScoreFromBackup1 */

/* >>> factory FindPlayAreaCardWithHighestAIScore */
/* energy.asm:596-675 */
AIScoreResult FindPlayAreaCardWithHighestAIScore(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	if (wAIEnergyAttachLogicFlags & AI_ENERGY_FLAG_SKIP_ARENA_CARD) {
		uint8_t cnt = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		uint8_t n = (uint8_t)(cnt - 1u);
		if (n == 0u) {
			AIScoreResult r = {0u, 0x80u, b, c, d, e, hl};
			return r;
		}
		e = 0u;
		c = PLAY_AREA_BENCH_1;
		d = c;
		hl = (uint16_t)(wPlayAreaAIScore_ADDR + 1u);
		for (uint8_t i = 0u; i < n; i++) {
			uint8_t v = gb_read8(hl);
			hl = (uint16_t)(hl + 1u);
			if (v > e) {
				e = v;
				d = c;
			}
			c = (uint8_t)(c + 1u);
		}
		hTempPlayAreaLocation_ff9d = d;
		AIScoreResult r = {d, 0x90u, 0u, c, d, e, hl};
		return r;
	}

	uint8_t cnt = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint32_t n = cnt ? (uint32_t)cnt : 0x100u;
	e = 0u;
	c = PLAY_AREA_ARENA;
	d = c;
	hl = wPlayAreaAIScore_ADDR;
	for (uint32_t i = 0u; i < n; i++) {
		uint8_t v = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (v > e) {
			e = v;
			d = c;
		}
		c = (uint8_t)(c + 1u);
	}
	if (e < 0x85u) {
		AIScoreResult r = {e, (uint8_t)(e == 0u ? 0x80u : 0x00u), 0u, c, d, e, hl};
		return r;
	}
	hTempPlayAreaLocation_ff9d = d;
	AIScoreResult r = {d, (uint8_t)(0x10u | (e == 0x85u ? 0x80u : 0x00u)), 0u, c, d, e, hl};
	return r;
}
/* <<< factory FindPlayAreaCardWithHighestAIScore */

/* >>> factory CheckSpecificDecksToAttachDoubleColorless */
static uint8_t CheckSpecificDecksToAttachDoubleColorless_GetID(void)
{
	uint8_t loc = hTempPlayAreaLocation_ff9d;
	DuelistVarResult v = GetTurnDuelistVariable((uint8_t)(loc + DUELVARS_ARENA_CARD));
	uint16_t id16 = GetCardIDFromDeckIndex(v.a);
	return (uint8_t)id16;
}

CheckSpecificDecksToAttachDoubleColorlessResult CheckSpecificDecksToAttachDoubleColorless(
	uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t deck_id = wOpponentDeckID;
	uint8_t a = deck_id;
	uint8_t check_colorless = 0u;

	if (deck_id == LEGENDARY_DRAGONITE_DECK_ID) {
		a = CheckSpecificDecksToAttachDoubleColorless_GetID();
		if (a == CHARMANDER || a == DRATINI)
			check_colorless = 1u;
	} else if (deck_id == FIRE_CHARGE_DECK_ID) {
		a = CheckSpecificDecksToAttachDoubleColorless_GetID();
		if (a == GROWLITHE)
			check_colorless = 1u;
	} else if (deck_id == LEGENDARY_RONALD_DECK_ID) {
		a = CheckSpecificDecksToAttachDoubleColorless_GetID();
		if (a == DRATINI)
			check_colorless = 1u;
	}

	if (check_colorless) {
		uint8_t loc = hTempPlayAreaLocation_ff9d;
		(void)GetPlayAreaCardAttachedEnergies(loc);
		a = gb_read8((uint16_t)(wAttachedEnergies_ADDR + COLORLESS));
		if (a == 0u) {
			CoreCardListResult r = LookForCardIDInHand(DOUBLE_COLORLESS_ENERGY);
			if (!(r.f & 0x10u)) {
				hTemp_ffa0 = r.a;
				return (CheckSpecificDecksToAttachDoubleColorlessResult){r.a, 0x10u, b, c, d, e, hl};
			}
			a = r.a;
		}
	}
	return (CheckSpecificDecksToAttachDoubleColorlessResult){a, (uint8_t)(a == 0u ? 0x80u : 0u), b, c, d, e, hl};
}
/* <<< factory CheckSpecificDecksToAttachDoubleColorless */

/* >>> factory GetEnergyCardForDiscardOrEnergyBoostAttack */
GetEnergyCardForDiscardOrEnergyBoostAttackResult GetEnergyCardForDiscardOrEnergyBoostAttack(uint8_t c_in)
{
	DuelistVarResult dv = GetTurnDuelistVariable((uint8_t)(hTempPlayAreaLocation_ff9d + DUELVARS_ARENA_CARD));
	uint8_t a = LoadCardDataToBuffer2_FromDeckIndex(dv.a);
	uint8_t b = a;
	uint16_t hl;
	a = wSelectedAttack;
	if (a == 0u) {
		hl = wLoadedCard2Atk1EnergyCost_ADDR;
	} else {
		a = b;
		if (a == ZAPDOS_LV64)
			return (GetEnergyCardForDiscardOrEnergyBoostAttackResult){a, b, c_in, 0u, 0x00u};
		if (a == CHARIZARD || a == EXEGGUTOR)
			return (GetEnergyCardForDiscardOrEnergyBoostAttackResult){a, FALSE, TRUE, 0u, 0x90u};
		hl = wLoadedCard2Atk2EnergyCost_ADDR;
	}

	uint8_t e;
	uint8_t f;
	a = gb_read8(hl); hl = (uint16_t)(hl + 1u);
	b = a;
	a = (uint8_t)(a & 0xF0u);
	if (a != 0u) {
		e = FIRE_ENERGY;
		f = 0x10u;
	} else {
		a = b;
		a = (uint8_t)(a & 0x0Fu);
		if (a != 0u) {
			e = GRASS_ENERGY;
			f = 0x10u;
		} else {
			a = gb_read8(hl); hl = (uint16_t)(hl + 1u);
			b = a;
			a = (uint8_t)(a & 0xF0u);
			if (a != 0u) {
				e = LIGHTNING_ENERGY;
				f = 0x10u;
			} else {
				a = b;
				a = (uint8_t)(a & 0x0Fu);
				if (a != 0u) {
					e = WATER_ENERGY;
					f = 0x10u;
				} else {
					a = gb_read8(hl); hl = (uint16_t)(hl + 1u);
					b = a;
					a = (uint8_t)(a & 0xF0u);
					if (a != 0u) {
						e = FIGHTING_ENERGY;
						f = 0x10u;
					} else {
						e = PSYCHIC_ENERGY;
						f = 0x90u;
					}
				}
			}
		}
	}
	return (GetEnergyCardForDiscardOrEnergyBoostAttackResult){a, TRUE, FALSE, e, f};
}
/* <<< factory GetEnergyCardForDiscardOrEnergyBoostAttack */

/* >>> factory CheckIfEvolutionNeedsEnergyForAttack */
CheckIfEvolutionNeedsEnergyForAttackResult CheckIfEvolutionNeedsEnergyForAttack(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)CreateHandCardList(c);
	uint8_t loc1 = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
	DuelistVarResult var1 = GetTurnDuelistVariable((uint8_t)(loc1 + DUELVARS_ARENA_CARD_510));
	CheckCardEvolutionInHandOrDeckResult evo = CheckCardEvolutionInHandOrDeck(var1.a);
	if ((evo.f & 0x10u) == 0u) {
		uint8_t f_out = (evo.a == 0u) ? 0x80u : 0x00u;
		return (CheckIfEvolutionNeedsEnergyForAttackResult){evo.a, f_out, b, c, d, e, var1.hl};
	}

	uint8_t new_b = evo.a;
	uint8_t loc2 = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
	DuelistVarResult var2 = GetTurnDuelistVariable((uint8_t)(loc2 + DUELVARS_ARENA_CARD_510));
	uint8_t saved_a = var2.a;
	gb_write8(var2.hl, new_b);
	CheckEnergyNeededForAttackResult energy = CheckEnergyNeededForAttack();
	if (energy.f & 0x10u) {
		uint8_t loc3 = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
		DuelistVarResult var3 = GetTurnDuelistVariable((uint8_t)(loc3 + DUELVARS_ARENA_CARD_510));
		gb_write8(var3.hl, saved_a);
		uint8_t f_out2 = (uint8_t)((evo.f & 0x80u) | 0x10u);
		return (CheckIfEvolutionNeedsEnergyForAttackResult){saved_a, f_out2, new_b, c, d, e, var3.hl};
	}

	uint8_t loc4 = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
	DuelistVarResult var4 = GetTurnDuelistVariable((uint8_t)(loc4 + DUELVARS_ARENA_CARD_510));
	gb_write8(var4.hl, saved_a);
	uint8_t f_out3 = (saved_a == 0u) ? 0x80u : 0x00u;
	return (CheckIfEvolutionNeedsEnergyForAttackResult){saved_a, f_out3, new_b, c, d, e, var4.hl};
}
/* <<< factory CheckIfEvolutionNeedsEnergyForAttack */

/* >>> factory AITryToPlayEnergyCard */
uint8_t AITryToPlayEnergyCard(void)
{
	gb_write8(wTempAI_ADDR, 0u);
	gb_write8(wSelectedAttack_ADDR, FIRST_ATTACK_OR_PKMN_POWER_600);
	CheckEnergyNeededForAttackResult r1 = CheckEnergyNeededForAttack();
	if (r1.f & 0x10u) {
		if (r1.b != 0u || r1.c != 0u)
			goto check_deck;
	}

second_attack:
	gb_write8(wSelectedAttack_ADDR, SECOND_ATTACK_600);
	CheckEnergyNeededForAttackResult r2 = CheckEnergyNeededForAttack();
	if (r2.f & 0x10u) {
		if (r2.b != 0u || r2.c != 0u)
			goto check_deck;
	}

	{
		gb_write8(wTempAI_ADDR, 1u);
		gb_write8(wSelectedAttack_ADDR, FIRST_ATTACK_OR_PKMN_POWER_600);
		(void)CheckEnergyNeededForAttack();
		AttackFlagResult f1a = CheckLoadedAttackFlag((uint8_t)(ATTACK_FLAG2_ADDRESS_600 | ATTACHED_ENERGY_BOOST_F_600));
		if (f1a.f & 0x10u)
			goto energy_boost_or_discard_energy;
		AttackFlagResult f1b = CheckLoadedAttackFlag((uint8_t)(ATTACK_FLAG2_ADDRESS_600 | DISCARD_ENERGY_F_600));
		if (f1b.f & 0x10u)
			goto energy_boost_or_discard_energy;

		gb_write8(wSelectedAttack_ADDR, SECOND_ATTACK_600);
		(void)CheckEnergyNeededForAttack();
		AttackFlagResult f2a = CheckLoadedAttackFlag((uint8_t)(ATTACK_FLAG2_ADDRESS_600 | ATTACHED_ENERGY_BOOST_F_600));
		if (f2a.f & 0x10u)
			goto energy_boost_or_discard_energy;
		AttackFlagResult f2b = CheckLoadedAttackFlag((uint8_t)(ATTACK_FLAG2_ADDRESS_600 | DISCARD_ENERGY_F_600));
		if (f2b.f & 0x10u)
			goto energy_boost_or_discard_energy;

		CheckIfEvolutionNeedsEnergyForAttackResult evo =
			CheckIfEvolutionNeedsEnergyForAttack(0u, 0u, 0u, 0u, 0u);
		if ((evo.f & 0x10u) == 0u)
			return 0u;
		(void)CreateEnergyCardListFromHand(evo.a);
		goto check_deck;
	}

energy_boost_or_discard_energy:
	{
		GetEnergyCardForDiscardOrEnergyBoostAttackResult g =
			GetEnergyCardForDiscardOrEnergyBoostAttack(0u);
		if ((g.f & 0x10u) == 0u)
			return 0u;
	}

check_deck:
	{
		CheckSpecificDecksToAttachDoubleColorlessResult sd =
			CheckSpecificDecksToAttachDoubleColorless(0u, 0u, 0u, 0u, 0u);
		if (sd.f & 0x10u)
			goto play_energy_card;

		if (sd.b != 0u) {
			CoreCardListResult look = LookForCardIDInHand(sd.e);
			gb_write8(hTemp_ffa0_ADDR, look.a);
			if ((look.f & 0x10u) == 0u)
				goto play_energy_card;
			goto colorless_energy_fallthrough_look_for_any;
		}

	colorless_energy:
		if (gb_read8(hTempPlayAreaLocation_ff9d_ADDR) != 0u)
			goto look_for_any_energy;
		if (sd.c == 0u)
			goto check_if_done;
		if (sd.c != 2u)
			goto look_for_any_energy;

		{
			uint16_t hl = wDuelTempList_ADDR;
			for (;;) {
				uint8_t v = gb_read8(hl);
				hl = (uint16_t)(hl + 1u);
				if (v == 0xFFu)
					goto look_for_any_energy;
				gb_write8(hTemp_ffa0_ADDR, v);
				uint16_t id16 = GetCardIDFromDeckIndex(v);
				uint8_t id_e = (uint8_t)id16;
				if (id_e == DOUBLE_COLORLESS_ENERGY_600)
					goto play_energy_card;
			}
		}

	colorless_energy_fallthrough_look_for_any:
		goto colorless_energy;

	look_for_any_energy:
		{
			uint16_t hl = wDuelTempList_ADDR;
			(void)CountCardsInDuelTempList();
			(void)ShuffleCards(0u, hl);
			for (;;) {
				uint8_t v = gb_read8(hl);
				hl = (uint16_t)(hl + 1u);
				if (v == 0xFFu)
					goto check_if_done;
				CheckIfOpponentHasBossDeckIDResult boss = CheckIfOpponentHasBossDeckID(v);
				uint8_t load;
				if (boss.carry == 0u) {
					load = v;
				} else {
					uint16_t id16b = GetCardIDFromDeckIndex(v);
					uint8_t id_e2 = (uint8_t)id16b;
					if (id_e2 == DOUBLE_COLORLESS_ENERGY_600)
						continue;
					load = boss.a;
				}
				gb_write8(hTemp_ffa0_ADDR, load);
				break;
			}
		}
	}

play_energy_card:
	{
		uint8_t loc = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
		gb_write8(hTempPlayAreaLocation_ffa1_ADDR, loc);
		(void)AIMakeDecision(OPPACTION_PLAY_ENERGY_600);
		return 1u;
	}

check_if_done:
	if (gb_read8(wTempAI_ADDR) != 0u)
		return 0u;
	if (gb_read8(wSelectedAttack_ADDR) == 0u)
		goto second_attack;
	return 0u;
}
/* <<< factory AITryToPlayEnergyCard */

/* >>> factory DetermineAIScoreOfAttackEnergyRequirement */
void DetermineAIScoreOfAttackEnergyRequirement(uint8_t a)
{
	wSelectedAttack = a;
	CheckEnergyNeededForAttackResult energy = CheckEnergyNeededForAttack();
	if (energy.f & 0x10u) {
		uint8_t flag = ATTACK_FLAG2_ADDRESS | IGNORE_THIS_ATTACK_F;
		if (CheckLoadedAttackFlag(flag).f & 0x10u)
			AIDiscourage(5u);
		if (energy.b != 0u) {
			CoreCardListResult hand = LookForCardIDInHand(energy.e);
			if ((hand.f & 0x10u) == 0u)
				AIEncourage(4u);
		}
		if (energy.c != 0u)
			AIEncourage(3u);
		if ((uint8_t)(energy.b + energy.c - 1u) == 0u)
			AIEncourage(3u);
	} else {
		uint8_t flag = ATTACK_FLAG2_ADDRESS | ATTACHED_ENERGY_BOOST_F;
		if (CheckLoadedAttackFlag(flag).f & 0x10u) {
			if (wLoadedAttackEffectParam == MAX_ENERGY_BOOST_IS_LIMITED) {
				CheckIfNoSurplusEnergyResult surplus = CheckIfNoSurplusEnergyForAttack();
				if ((surplus.f & 0x10u) != 0u || surplus.a < 3u)
					AIEncourage(2u);
				else
					AIDiscourage(5u);
			} else {
				AIEncourage(0u);
			}
		}
		flag = ATTACK_FLAG2_ADDRESS | DISCARD_ENERGY_F;
		if (CheckLoadedAttackFlag(flag).f & 0x10u && wLoadedCard1ID != ZAPDOS_LV64) {
			CheckIfNoSurplusEnergyResult surplus = CheckIfNoSurplusEnergyForAttack();
			if ((surplus.f & 0x10u) != 0u)
				AIEncourage(2u);
			else
				AIDiscourage(5u);
		}
	}

	uint8_t evolution = wTempAI;
	if (evolution == 0xFFu)
		return;
	uint8_t location = hTempPlayAreaLocation_ff9d;
	DuelistVarResult slot = GetTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD));
	uint8_t original = slot.a;
	gb_write8(slot.hl, evolution);
	CheckEnergyNeededForAttackResult evo_energy = CheckEnergyNeededForAttack();
	if ((evo_energy.f & 0x10u) != 0u) {
		uint8_t flag = ATTACK_FLAG2_ADDRESS | IGNORE_THIS_ATTACK_F;
		if ((CheckLoadedAttackFlag(flag).f & 0x10u) == 0u) {
			if (evo_energy.b != 0u) {
				CoreCardListResult hand = LookForCardIDInHand(evo_energy.e);
				if ((hand.f & 0x10u) == 0u)
					AIEncourage(2u);
			}
			if (evo_energy.c != 0u)
				AIEncourage(1u);
		}
	}
	gb_write8(slot.hl, original);
}
/* <<< factory DetermineAIScoreOfAttackEnergyRequirement */

/* >>> factory AIProcessEnergyCards */
void AIProcessEnergyCards(void)
{
	for (uint8_t i=0; i<MAX_PLAY_AREA_POKEMON; ++i) gb_write8((uint16_t)(wPlayAreaEnergyAIScore_ADDR+i),0x80u);
	HandleLegendaryArticunoEnergyScoring();
	uint8_t count=GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	for(uint8_t loc=0; count; ++loc,--count){
		hTempPlayAreaLocation_ff9d=loc; wAIScore=0x80u; wTempAI=0xffu;
		if(!(wAIEnergyAttachLogicFlags&AI_ENERGY_FLAG_SKIP_EVOLUTION)){
			(void)CreateHandCardList(count); wCurCardCanAttack=GetTurnDuelistVariable((uint8_t)(loc+DUELVARS_ARENA_CARD)).a;
			EnergyFlagsResult need=CheckEnergyFlagsNeededInList(GetAttacksEnergyCostBits(wCurCardCanAttack).a);
			if(need.carry){ CheckForEvolutionInListResult x=CheckForEvolutionInList(wCurCardCanAttack,0); if(x.f&0x10u){wTempAI=x.a;(void)AIEncourage(2);} else if(CheckForEvolutionInDeck(wCurCardCanAttack,0).f&0x10u)(void)AIEncourage(1); }
		}
		if(!(CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK).f&0x10u) && (CountTurnDuelistPokemonWithActivePkmnPower(VENUSAUR_LV67).f&0x10u))(void)AIEncourage(1);
		if(!loc){if(wAIBarrierFlagCounter&(1u<<AI_MEWTWO_MILL_F))AIDiscourage(5);else(void)AIEncourage(4);uint8_t hp=ConvertHPToDamageCounters_Bank5(GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a).a;if(hp<3){uint8_t st=GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;if(st&(hp==2?DOUBLE_POISONED:POISONED))AIDiscourage(10);}}else{uint8_t hp=ConvertHPToDamageCounters_Bank5(GetTurnDuelistVariable((uint8_t)(loc+DUELVARS_ARENA_CARD_HP)).a).a;if(hp<3)AIDiscourage((uint8_t)(3-hp));}
		if(CheckIfNotABossDeckID().carry==0){(void)HandleAIEnergyScoringForRepeatedBenchPokemon();uint8_t v=gb_read8((uint16_t)(wPlayAreaEnergyAIScore_ADDR+loc));if(v>=0x80)(void)AIEncourage((uint8_t)(v-0x80));else AIDiscourage((uint8_t)(0x80-v));}
		(void)AIEncourage(1);DetermineAIScoreOfAttackEnergyRequirement(0);DetermineAIScoreOfAttackEnergyRequirement(1);gb_write8((uint16_t)(wPlayAreaAIScore_ADDR+loc),wAIScore);
	}
	AIScoreResult best=FindPlayAreaCardWithHighestAIScore(0,0,0,0,0);if(best.f&0x10){if(wAIEnergyAttachLogicFlags)(void)RetrievePlayAreaAIScoreFromBackup1();else{(void)CreateEnergyCardListFromHand(best.a);(void)AITryToPlayEnergyCard();}}else if(wAIEnergyAttachLogicFlags)(void)RetrievePlayAreaAIScoreFromBackup1();
}
/* <<< factory AIProcessEnergyCards */
