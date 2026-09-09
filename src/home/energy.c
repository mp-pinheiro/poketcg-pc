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

#include "home/energy.h"
#include "generated/wram.h"
#include "generated/hram.h"
#define AI_ENERGY_FLAG_DONT_PLAY 0x01u

#include "home/energy.h"
#include "generated/wram.h"
#include "mem.h"
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
	/* bc and de leave as CheckEnergyNeededForAttack set them (energy.asm
	 * :783-801): GetTurnDuelistVariable and `pop af` touch neither. */
	if (energy.f & 0x10u) {
		uint8_t loc3 = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
		DuelistVarResult var3 = GetTurnDuelistVariable((uint8_t)(loc3 + DUELVARS_ARENA_CARD_510));
		gb_write8(var3.hl, saved_a);
		uint8_t f_out2 = (uint8_t)((evo.f & 0x80u) | 0x10u);
		return (CheckIfEvolutionNeedsEnergyForAttackResult){saved_a, f_out2, energy.b, energy.c, energy.d, energy.e, var3.hl};
	}

	uint8_t loc4 = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
	DuelistVarResult var4 = GetTurnDuelistVariable((uint8_t)(loc4 + DUELVARS_ARENA_CARD_510));
	gb_write8(var4.hl, saved_a);
	uint8_t f_out3 = (saved_a == 0u) ? 0x80u : 0x00u;
	return (CheckIfEvolutionNeedsEnergyForAttackResult){saved_a, f_out3, energy.b, energy.c, energy.d, energy.e, var4.hl};
}
/* <<< factory CheckIfEvolutionNeedsEnergyForAttack */

/* >>> factory AITryToPlayEnergyCard */
AITryToPlayEnergyCardResult AITryToPlayEnergyCard(void)
{
	uint8_t pending;
	uint8_t attack;
	/* b = basic energy still needed, c = colorless still needed, e = the
	 * basic energy's card ID: CheckEnergyNeededForAttack's registers, which
	 * every path into .check_deck carries there (energy.asm:849-910). */
	uint8_t need_b;
	uint8_t need_c;
	uint8_t need_e;

	gb_write8(wTempAI_ADDR, 0u);
	gb_write8(wSelectedAttack_ADDR, FIRST_ATTACK_OR_PKMN_POWER_600);
	CheckEnergyNeededForAttackResult r1 = CheckEnergyNeededForAttack();
	if (r1.f & 0x10u) {
		if (r1.b != 0u || r1.c != 0u) {
			need_b = r1.b;
			need_c = r1.c;
			need_e = r1.e;
			goto check_deck;
		}
	}

second_attack:
	gb_write8(wSelectedAttack_ADDR, SECOND_ATTACK_600);
	CheckEnergyNeededForAttackResult r2 = CheckEnergyNeededForAttack();
	if (r2.f & 0x10u) {
		if (r2.b != 0u || r2.c != 0u) {
			need_b = r2.b;
			need_c = r2.c;
			need_e = r2.e;
			goto check_deck;
		}
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
			return (AITryToPlayEnergyCardResult){evo.a, evo.f};
		/* CreateEnergyCardListFromHand preserves bc and de (core.asm:622-654). */
		(void)CreateEnergyCardListFromHand(evo.a);
		need_b = evo.b;
		need_c = evo.c;
		need_e = evo.e;
		goto check_deck;
	}

energy_boost_or_discard_energy:
	{
		GetEnergyCardForDiscardOrEnergyBoostAttackResult g =
			GetEnergyCardForDiscardOrEnergyBoostAttack(0u);
		if ((g.f & 0x10u) == 0u)
			return (AITryToPlayEnergyCardResult){g.a, g.f};
		need_b = g.b;
		need_c = g.c;
		need_e = g.e;
	}

check_deck:
	{
		CheckSpecificDecksToAttachDoubleColorlessResult sd =
			CheckSpecificDecksToAttachDoubleColorless(need_b, need_c, 0u, need_e, 0u);
		if (sd.f & 0x10u)
			goto play_energy_card;

		if (need_b != 0u) {
			CoreCardListResult look = LookForCardIDInHand(need_e);
			gb_write8(hTemp_ffa0_ADDR, look.a);
			if ((look.f & 0x10u) == 0u)
				goto play_energy_card;
		}

		/* .colorless_energy */
		if (gb_read8(hTempPlayAreaLocation_ff9d_ADDR) != 0u)
			goto look_for_any_energy;
		if (need_c == 0u)
			goto check_if_done;
		if (need_c != 2u)
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

	look_for_any_energy:
		{
			uint16_t hl = wDuelTempList_ADDR;
			(void)ShuffleCards(CountCardsInDuelTempList().a, hl);
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
		AIMakeDecisionResult played =
			AIMakeDecision(OPPACTION_PLAY_ENERGY_600, 0u, 0u, 0u, 0u);

		return (AITryToPlayEnergyCardResult){played.a, 0x10u};
	}

check_if_done:
	pending = gb_read8(wTempAI_ADDR);
	if (pending != 0u)
		return (AITryToPlayEnergyCardResult){pending, 0x00u};
	attack = gb_read8(wSelectedAttack_ADDR);
	if (attack == 0u)
		goto second_attack;
	return (AITryToPlayEnergyCardResult){attack, 0x00u};
}
/* <<< factory AITryToPlayEnergyCard */

/* >>> factory DetermineAIScoreOfAttackEnergyRequirement */
/* energy.asm .asm_166cd: the surplus-energy verdict came back "play more",
 * and an ATTACHED_ENERGY_BOOST attack that one more energy would turn into a
 * knockout is worth a lot more. */
static void encourage_energy_boost_knockout(void)
{
	(void)AIEncourage(2u);
	if ((CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | ATTACHED_ENERGY_BOOST_F).f & 0x10u) == 0u)
		return;
	(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
	uint8_t hp = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t damage = gb_read8(wDamage_ADDR);
	if (hp <= damage)
		return;
	uint8_t boosted = (uint8_t)(damage + 10u);
	if (hp > boosted)
		return;
	(void)AIEncourage(20u);
	if (hTempPlayAreaLocation_ff9d == 0u)
		(void)AIEncourage(10u);
}

void DetermineAIScoreOfAttackEnergyRequirement(uint8_t a)
{
	wSelectedAttack = a;
	CheckEnergyNeededForAttackResult energy = CheckEnergyNeededForAttack();
	if (energy.f & 0x10u) {
		/* .not_enough_energy */
		if (CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | IGNORE_THIS_ATTACK_F).f & 0x10u)
			AIDiscourage(5u);
		uint8_t color_in_hand = energy.b != 0u
			&& (LookForCardIDInHand(energy.e).f & 0x10u) == 0u;
		if (color_in_hand) {
			(void)AIEncourage(4u);
		} else {
			if (energy.c == 0u)
				goto check_evolution;
			(void)AIEncourage(3u);
		}
		/* .check_total_needed */
		if ((uint8_t)(energy.b + energy.c - 1u) != 0u)
			goto check_evolution;
		(void)AIEncourage(3u);
		if (hTempPlayAreaLocation_ff9d != 0u)
			goto check_evolution;
		(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
		if (GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a > gb_read8(wDamage_ADDR))
			goto check_evolution;
		(void)AIEncourage(20u);
		/* The asm re-tests the location it just tested; it is the arena. */
		(void)AIEncourage(10u);
	} else if (CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | ATTACHED_ENERGY_BOOST_F).f & 0x10u) {
		/* .attached_energy_boost: a holds the effect parameter. */
		uint8_t param = wLoadedAttackEffectParam;
		if (param != MAX_ENERGY_BOOST_IS_LIMITED) {
			(void)AIEncourage(param);
		} else {
			CheckIfNoSurplusEnergyResult surplus = CheckIfNoSurplusEnergyForAttack();
			if ((surplus.f & 0x10u) != 0u || surplus.a < 3u)
				encourage_energy_boost_knockout();
			else
				AIDiscourage(5u);
		}
	} else if (CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | DISCARD_ENERGY_F).f & 0x10u) {
		/* .discard_energy */
		if (wLoadedCard1ID != ZAPDOS_LV64) {
			if (CheckIfNoSurplusEnergyForAttack().f & 0x10u)
				encourage_energy_boost_knockout();
			else
				AIDiscourage(5u);
		}
	}

check_evolution:
	{
		uint8_t evolution = wTempAI;
		if (evolution == 0xFFu)
			return;
		uint8_t location = hTempPlayAreaLocation_ff9d;
		DuelistVarResult slot = GetTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD));
		uint8_t original = slot.a;
		gb_write8(slot.hl, evolution);
		CheckEnergyNeededForAttackResult evo_energy = CheckEnergyNeededForAttack();
		if ((evo_energy.f & 0x10u) != 0u
		    && (CheckLoadedAttackFlag(ATTACK_FLAG2_ADDRESS | IGNORE_THIS_ATTACK_F).f & 0x10u) == 0u) {
			if (evo_energy.b != 0u && (LookForCardIDInHand(evo_energy.e).f & 0x10u) == 0u)
				(void)AIEncourage(2u);
			else if (evo_energy.c != 0u)
				(void)AIEncourage(1u);
		}
		gb_write8(slot.hl, original);
	}
}
/* <<< factory DetermineAIScoreOfAttackEnergyRequirement */

/* >>> factory AIProcessEnergyCards */
AIEnergyResult AIProcessEnergyCards(void)
{
	for (uint8_t i = 0; i < MAX_PLAY_AREA_POKEMON; ++i)
		gb_write8((uint16_t)(wPlayAreaEnergyAIScore_ADDR + i), 0x80u);
	HandleLegendaryArticunoEnergyScoring();
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	for (uint8_t loc = 0; count != 0u; ++loc, --count) {
		hTempPlayAreaLocation_ff9d = loc;
		wAIScore = 0x80u;
		wTempAI = 0xFFu;
		if ((wAIEnergyAttachLogicFlags & AI_ENERGY_FLAG_SKIP_EVOLUTION) == 0u) {
			(void)CreateHandCardList(0u);
			wCurCardCanAttack = GetTurnDuelistVariable((uint8_t)(loc + DUELVARS_ARENA_CARD)).a;
			EnergyFlagsResult need =
				CheckEnergyFlagsNeededInList(GetAttacksEnergyCostBits(wCurCardCanAttack).a);
			/* energy.asm:149: a card whose energy is not in hand keeps the
			 * neutral score; nothing below is evaluated for it. */
			if (!need.carry)
				goto store_score;
			CheckForEvolutionInListResult in_hand = CheckForEvolutionInList(wCurCardCanAttack, 0u, 0u, 0u);
			if (in_hand.f & 0x10u) {
				wTempAI = in_hand.a;
				(void)AIEncourage(2u);
			} else if (CheckForEvolutionInDeck(wCurCardCanAttack, 0u).f & 0x10u) {
				(void)AIEncourage(1u);
			}
		}
		/* .check_venusaur */
		if ((CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK).f & 0x10u) == 0u
		    && (CountTurnDuelistPokemonWithActivePkmnPower(VENUSAUR_LV67).f & 0x10u) != 0u)
			(void)AIEncourage(1u);
		if (loc == 0u) {
			/* .check_bench is reached when poison will KO the arena card
			 * or the defending Pokemon can. */
			uint8_t threatened;
			if (wAIBarrierFlagCounter & (1u << AI_MEWTWO_MILL_F)) {
				AIDiscourage(5u);
				threatened = 0u;
			} else {
				(void)AIEncourage(4u);
				uint8_t hp = ConvertHPToDamageCounters_Bank5(
					GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a).a;
				threatened = hp < 3u
					&& (GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a
					    & (hp == 2u ? DOUBLE_POISONED : POISONED)) != 0u;
			}
			if (!threatened)
				threatened = (CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) != 0u;
			if (threatened) {
				AIDiscourage(10u);
				if (GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a == 1u)
					(void)AIEncourage(6u);
			}
		} else {
			uint8_t hp = ConvertHPToDamageCounters_Bank5(
				GetTurnDuelistVariable((uint8_t)(loc + DUELVARS_ARENA_CARD_HP)).a).a;
			if (hp < 3u)
				AIDiscourage((uint8_t)(3u - hp));
		}
		/* .ai_score_bonus: the deck's (card ID, energy target, score) list. */
		if (gb_read8(wAICardListEnergyBonus_ADDR + 1u) != 0u) {
			uint16_t list = (uint16_t)(gb_read8(wAICardListEnergyBonus_ADDR)
					| (gb_read8(wAICardListEnergyBonus_ADDR + 1u) << 8));
			uint8_t id = (uint8_t)GetCardIDFromDeckIndex(
				GetTurnDuelistVariable((uint8_t)(loc + DUELVARS_ARENA_CARD)).a);
			for (;;) {
				uint8_t entry = gb_read8(list++);
				if (entry == 0u)
					break;
				if (entry != id) {
					list = (uint16_t)(list + 2u);
					continue;
				}
				uint8_t target = gb_read8(list++);
				(void)GetPlayAreaCardAttachedEnergies(loc);
				if (wTotalAttachedEnergies >= target) {
					/* energy.asm:242: `jr .store_score`, skipping the
					 * rest of the scoring (the asm's own noted bug). */
					AIDiscourage(10u);
					goto store_score;
				}
				uint8_t score = gb_read8(list);
				if (score >= 0x80u)
					(void)AIEncourage((uint8_t)(score - 0x80u));
				else
					AIDiscourage((uint8_t)(0x80u - score));
				break;
			}
		}
		/* .check_boss_deck */
		if (CheckIfNotABossDeckID().carry == 0u) {
			(void)HandleAIEnergyScoringForRepeatedBenchPokemon();
			uint8_t v = gb_read8((uint16_t)(wPlayAreaEnergyAIScore_ADDR + loc));
			if (v >= 0x80u)
				(void)AIEncourage((uint8_t)(v - 0x80u));
			else
				AIDiscourage((uint8_t)(0x80u - v));
		}
		(void)AIEncourage(1u);
		DetermineAIScoreOfAttackEnergyRequirement(FIRST_ATTACK_OR_PKMN_POWER_600);
		DetermineAIScoreOfAttackEnergyRequirement(SECOND_ATTACK_600);
	store_score:
		gb_write8((uint16_t)(wPlayAreaAIScore_ADDR + loc), wAIScore);
	}
	/* energy.asm:265-285. RetrievePlayAreaAIScoreFromBackup1 is push af ...
	 * pop af (:71-85), so the carry each tail jump carries is this routine's:
	 * `scf` when a card was found under logic flags, clear otherwise, and
	 * AITryToPlayEnergyCard's own carry on the no-flags path -- which its
	 * 1/0 return already is, set only on `.play_energy_card` (:138-145). */
	AIScoreResult best = FindPlayAreaCardWithHighestAIScore(0, 0, 0, 0, 0);

	uint8_t logic = wAIEnergyAttachLogicFlags;

	if ((best.f & 0x10u) != 0u) {
		if (logic != 0u) {
			(void)RetrievePlayAreaAIScoreFromBackup1();
			return (AIEnergyResult){logic, 0x10u};
		}
		(void)CreateEnergyCardListFromHand(best.a);
		AITryToPlayEnergyCardResult played = AITryToPlayEnergyCard();

		return (AIEnergyResult){played.a, played.f};
	}
	if (logic != 0u)
		(void)RetrievePlayAreaAIScoreFromBackup1();
	return (AIEnergyResult){logic, 0x00u};
}
/* <<< factory AIProcessEnergyCards */

/* >>> factory AIProcessAndTryToPlayEnergy */
void AIProcessAndTryToPlayEnergy(void)
{
	wAIEnergyAttachLogicFlags = 0u;
	CoreCardListResult list = CreateEnergyCardListFromHand(0u);
	if ((list.f & 0x10u) == 0u) {
		AIProcessEnergyCards();
		return;
	}
	if (wAIEnergyAttachLogicFlags != 0u)
		(void)RetrievePlayAreaAIScoreFromBackup1();
}
/* <<< factory AIProcessAndTryToPlayEnergy */

/* >>> factory AIProcessButDontPlayEnergy_SkipEvolution */
AIEnergyResult AIProcessButDontPlayEnergy_SkipEvolution(void)
{
	wAIEnergyAttachLogicFlags = AI_ENERGY_FLAG_DONT_PLAY | AI_ENERGY_FLAG_SKIP_EVOLUTION;
	uint16_t de = wTempPlayAreaAIScore_ADDR;
	uint16_t hl = wPlayAreaAIScore_ADDR;
	for (uint8_t b = MAX_PLAY_AREA_POKEMON; b != 0u; b--) {
		gb_write8(de, gb_read8(hl));
		hl = (uint16_t)(hl + 1u);
		de = (uint16_t)(de + 1u);
	}
	wAIScore = gb_read8(hl);
	return AIProcessEnergyCards();
}
/* <<< factory AIProcessButDontPlayEnergy_SkipEvolution */

/* >>> factory AIProcessButDontPlayEnergy_SkipEvolutionAndArena */
/* energy.asm:48-70 */
AIEnergyResult AIProcessButDontPlayEnergy_SkipEvolutionAndArena(void)
{
	wAIEnergyAttachLogicFlags = AI_ENERGY_FLAG_DONT_PLAY | AI_ENERGY_FLAG_SKIP_EVOLUTION | AI_ENERGY_FLAG_SKIP_ARENA_CARD;
	uint16_t de = wTempPlayAreaAIScore_ADDR;
	uint16_t hl = wPlayAreaAIScore_ADDR;
	for (uint8_t b = MAX_PLAY_AREA_POKEMON; b != 0u; b--) {
		gb_write8(de, gb_read8(hl));
		hl = (uint16_t)(hl + 1u);
		de = (uint16_t)(de + 1u);
	}
	gb_write8(de, wAIScore);
	return AIProcessEnergyCards();
}
/* <<< factory AIProcessButDontPlayEnergy_SkipEvolutionAndArena */

/* >>> factory Func_16488 */
void Func_16488(void)
{
	wAIEnergyAttachLogicFlags = AI_ENERGY_FLAG_DONT_PLAY;
	uint16_t de = wTempPlayAreaAIScore_ADDR;
	uint16_t hl = wPlayAreaAIScore_ADDR;
	for (uint8_t b = MAX_PLAY_AREA_POKEMON; b != 0u; b--) {
		gb_write8(de, gb_read8(hl));
		hl = (uint16_t)(hl + 1u);
		de = (uint16_t)(de + 1u);
	}
	gb_write8(de, wAIScore);
	CoreCardListResult list = CreateEnergyCardListFromHand(0u);
	if ((list.f & 0x10u) == 0u) {
		AIProcessEnergyCards();
		return;
	}
	if (wAIEnergyAttachLogicFlags != 0u)
		(void)RetrievePlayAreaAIScoreFromBackup1();
}
/* <<< factory Func_16488 */
