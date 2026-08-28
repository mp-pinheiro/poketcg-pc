#include "home/sams_practice.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "mem.h"
/* >>> factory statics */
#include "home/core.h"

#define RATICATE 0xA8u
#define RATTATA 0xA7u
#define PLAY_AREA_BENCH_1 1u

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/core.h"
#include "home/retreat.h"
#define DUELVARS_ARENA_CARD 0xBBu
#define FIGHTING_ENERGY 0x05u
#define FIRST_ATTACK_OR_PKMN_POWER 0x00u
#define LIGHTNING_ENERGY 0x04u
#define MACHOP 0x7Du
#define OPPACTION_EVOLVE_PKMN 0x02u
#define OPPACTION_FINISH_NO_ATTACK 0x05u
#define OPPACTION_PLAY_BASIC_PKMN 0x01u
#define PLAY_AREA_ARENA 0x00u
#define PLAY_AREA_BENCH_2 0x02u
/* <<< factory statics */

SamsPracticeResult IsAIPracticeScriptedTurn(uint8_t a, uint8_t f, uint8_t b,
						uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t shifted = (uint8_t)(gb_read8(wDuelTurns_ADDR) >> 1);
	uint8_t flags = (uint8_t)((shifted == 7 ? 0x80u : 0u) |
					 (shifted >= 7 ? 0x10u : 0u));
	return (SamsPracticeResult){shifted, flags, b, c, d, e, hl};
}

SamsPracticeResult SetSamsStartingPlayArea(uint8_t a, uint8_t f, uint8_t b,
						uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	HandListResult list = CreateHandCardList(c);
	uint16_t scan = wDuelTempList_ADDR;

	b = list.b;
	d = list.d;
	e = list.e;
	c = list.c;
	for (;;) {
		a = gb_read8(scan++);
		hTempCardIndex_ff98 = a;
		if (a == 0xffu)
			return (SamsPracticeResult){a, 0xe0u, b, c, d, e, scan};
		if (LoadCardDataToBuffer1_FromDeckIndex(a) == 0x7du) {
			f = 0xc0u;
			break;
		}
	}

	a = hTempCardIndex_ff98;
	PutHandPokemonResult placed = PutHandPokemonCardInPlayArea(a, f);
	gb_write8(wDuelInitialPrizes_ADDR, 2);
	return (SamsPracticeResult){2, placed.f, b, c, d, e, placed.hl};
}

/* >>> factory GetPlayAreaLocationOfRaticateOrRattata */
/* sams_practice.asm:79-93 */
void GetPlayAreaLocationOfRaticateOrRattata(void)
{
	LookResult r = LookForCardIDInPlayArea_Bank5(RATICATE, PLAY_AREA_BENCH_1);
	if (r.a != 0xFFu) {
		hTempPlayAreaLocation_ff9d = r.a;
		return;
	}
	r = LookForCardIDInPlayArea_Bank5(RATTATA, PLAY_AREA_BENCH_1);
	if (r.a != 0xFFu) {
		hTempPlayAreaLocation_ff9d = r.a;
		return;
	}
	hTempPlayAreaLocation_ff9d = PLAY_AREA_BENCH_1;
}
/* <<< factory GetPlayAreaLocationOfRaticateOrRattata */

/* >>> factory AIPerformScriptedTurn */
SamsPracticeResult AIPerformScriptedTurn(uint8_t a, uint8_t f, uint8_t b,
					uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t scripted_turn = (uint8_t)(wDuelTurns >> 1);
	switch (scripted_turn) {
	case 0: {
		AIAttachEnergyInHandToCardInPlayAreaResult result =
			AIAttachEnergyInHandToCardInPlayArea(MACHOP, FIGHTING_ENERGY);
		a = result.a;
		f = result.f;
		d = MACHOP;
		e = FIGHTING_ENERGY;
		break;
	}
	case 1: {
		CoreCardListResult hand = LookForCardIDInHandList_Bank5(RATTATA);
		hTemp_ffa0 = hand.a;
		AIMakeDecisionResult decision =
			AIMakeDecision(OPPACTION_PLAY_BASIC_PKMN, b, c, d, e);
		b = decision.b;
		c = decision.c;
		d = decision.d;
		e = decision.e;
		f = decision.f;
		AIAttachEnergyInHandToCardInPlayAreaResult result =
			AIAttachEnergyInHandToCardInPlayArea(RATTATA, FIGHTING_ENERGY);
		a = result.a;
		f = result.f;
		d = RATTATA;
		e = FIGHTING_ENERGY;
		break;
	}
	case 2: {
		LookResult found = LookForCardIDInPlayArea_Bank5(RATTATA, PLAY_AREA_ARENA);
		hTempPlayAreaLocation_ffa1 = found.a;
		CoreCardListResult hand = LookForCardIDInHandList_Bank5(RATICATE);
		hTemp_ffa0 = hand.a;
		AIMakeDecisionResult decision =
			AIMakeDecision(OPPACTION_EVOLVE_PKMN, b, c, d, e);
		b = decision.b;
		c = decision.c;
		d = decision.d;
		e = decision.e;
		f = decision.f;
		AIAttachEnergyInHandToCardInPlayAreaResult result =
			AIAttachEnergyInHandToCardInPlayArea(RATICATE, LIGHTNING_ENERGY);
		a = result.a;
		f = result.f;
		d = RATICATE;
		e = LIGHTNING_ENERGY;
		break;
	}
	case 3: {
		AIAttachEnergyInHandToCardInPlayAreaResult result =
			AIAttachEnergyInHandToCardInPlayArea(RATICATE, LIGHTNING_ENERGY);
		a = result.a;
		f = result.f;
		d = RATICATE;
		e = LIGHTNING_ENERGY;
		break;
	}
	case 4: {
		CoreCardListResult hand = LookForCardIDInHandList_Bank5(MACHOP);
		hTemp_ffa0 = hand.a;
		AIMakeDecisionResult decision =
			AIMakeDecision(OPPACTION_PLAY_BASIC_PKMN, b, c, d, e);
		b = decision.b;
		c = decision.c;
		d = decision.d;
		e = decision.e;
		f = decision.f;
		AIAttachEnergyInHandToCardInBenchResult result =
			AIAttachEnergyInHandToCardInBench(MACHOP, FIGHTING_ENERGY);
		a = result.a;
		f = result.f;
		d = MACHOP;
		e = FIGHTING_ENERGY;
		DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
		uint8_t retreat_a = PLAY_AREA_BENCH_1;
		uint8_t retreat_f;
		if (arena.a == MACHOP) {
			retreat_a = PLAY_AREA_BENCH_2;
			retreat_f = 0u;
		} else {
			retreat_f = 0x40u;
			if ((arena.a & 0x0Fu) < (MACHOP & 0x0Fu))
				retreat_f = (uint8_t)(retreat_f | 0x20u);
			if (arena.a < MACHOP)
				retreat_f = (uint8_t)(retreat_f | 0x10u);
		}
		AITryToRetreatResult retreat = AITryToRetreat(retreat_a, retreat_f);
		a = retreat.a;
		f = retreat.f;
		break;
	}
	case 5:
	case 6: {
		AIAttachEnergyInHandToCardInPlayAreaResult result =
			AIAttachEnergyInHandToCardInPlayArea(MACHOP, FIGHTING_ENERGY);
		a = result.a;
		f = result.f;
		d = MACHOP;
		e = FIGHTING_ENERGY;
		break;
	}
	default:
		break;
	}

	a = 0u;
	f = 0x80u;
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
	CheckIfSelectedAttackIsUnusableResult unusable =
		CheckIfSelectedAttackIsUnusable(a, f, b, c, d, e, hl);
	a = unusable.a;
	f = unusable.f;
	b = unusable.b;
	c = unusable.c;
	d = unusable.d;
	e = unusable.e;
	hl = unusable.hl;
	if ((f & 0x10u) == 0u) {
		AITryUseAttackResult attack = AITryUseAttack(b);
		f = attack.f;
		return (SamsPracticeResult){a, f, b, c, d, e, hl};
	}
	AIMakeDecisionResult decision =
		AIMakeDecision(OPPACTION_FINISH_NO_ATTACK, b, c, d, e);
	b = decision.b;
	c = decision.c;
	d = decision.d;
	e = decision.e;
	f = decision.f;
	a = (uint8_t)(wDuelFinished | 1u);
	return (SamsPracticeResult){a, f, b, c, d, e, hl};
}
/* <<< factory AIPerformScriptedTurn */
