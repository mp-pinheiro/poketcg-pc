#include "home/legendary_articuno.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/core.h"
#include "home/duel.h"
#include "home/legendary_articuno.h"
#define ARTICUNO_LV35 0x5Eu
#define DEWGONG 0x4Cu
#define LAPRAS 0x59u
#define PLAY_AREA_BENCH_1 0x01u
#define SEEL 0x4Bu
/* <<< factory statics */

/* >>> factory ScoreLegendaryArticunoCards */
void ScoreLegendaryArticunoCards(void)
{
	SwapTurn();
	uint8_t prizes = CountPrizes();
	SwapTurn();
	if (prizes < 3u)
		return;

	CheckForBenchIDAtHalfHPAndCanUseSecondAttackResult check =
		CheckForBenchIDAtHalfHPAndCanUseSecondAttack(LAPRAS, 0u, 0u, 0u, 0u, 0u, 0u);
	uint8_t use_lapras = 0u;
	if (!(check.f & 0x10u)) {
		check = CheckForBenchIDAtHalfHPAndCanUseSecondAttack(ARTICUNO_LV35, 0u, check.b, check.c, check.d, check.e, check.hl);
		if (check.f & 0x10u)
			use_lapras = 1u;
		else {
			check = CheckForBenchIDAtHalfHPAndCanUseSecondAttack(DEWGONG, 0u, check.b, check.c, check.d, check.e, check.hl);
			if (check.f & 0x10u)
				use_lapras = 1u;
		}
	}

	if (use_lapras) {
		LookResult found = LookForCardIDInPlayArea_Bank5(LAPRAS, PLAY_AREA_BENCH_1);
		if (found.f & 0x10u) {
			CountNumberOfEnergyCardsAttachedResult energy = CountNumberOfEnergyCardsAttached(found.a);
			if (energy.a < 3u)
				(void)RaiseAIScoreToAllMatchingIDsInBench(LAPRAS);
			return;
		}
	}

	LookResult found = LookForCardIDInPlayArea_Bank5(ARTICUNO_LV35, PLAY_AREA_BENCH_1);
	if (found.f & 0x10u) {
		(void)RaiseAIScoreToAllMatchingIDsInBench(ARTICUNO_LV35);
		return;
	}
	found = LookForCardIDInPlayArea_Bank5(DEWGONG, PLAY_AREA_BENCH_1);
	if (found.f & 0x10u) {
		(void)RaiseAIScoreToAllMatchingIDsInBench(DEWGONG);
		return;
	}
	found = LookForCardIDInPlayArea_Bank5(SEEL, PLAY_AREA_BENCH_1);
	if (found.f & 0x10u)
		(void)RaiseAIScoreToAllMatchingIDsInBench(SEEL);
}
/* <<< factory ScoreLegendaryArticunoCards */
