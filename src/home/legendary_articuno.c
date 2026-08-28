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

#include "generated/wram.h"
#include "home/attacks.h"
#include "home/common.h"
#include "home/core.h"
#include "home/energy.h"
#include "home/general.h"
#include "home/hand_pokemon.h"
#include "home/init.h"
#define AI_FLAG_USED_PROFESSOR_OAK 0x04u
#define AI_TRAINER_CARD_PHASE_01 0x01u
#define AI_TRAINER_CARD_PHASE_02 0x02u
#define AI_TRAINER_CARD_PHASE_10 0x0au
#define AI_TRAINER_CARD_PHASE_13 0x0du
#define AI_TRAINER_CARD_PHASE_15 0x0fu
#define OPPACTION_FINISH_NO_ATTACK 0x05u
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

/* >>> factory AIDoTurn_LegendaryArticuno */
AIDoTurn_LegendaryArticunoResult AIDoTurn_LegendaryArticuno(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	InitAITurnVars();
	AIProcessHandTrainerCardsWrapResult trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_01);
	a = trainer.a;
	f = trainer.f;
	HandleAIAntiMewtwoDeckStrategyResult anti = HandleAIAntiMewtwoDeckStrategy(a, f, b, c, d, e, hl);
	a = anti.a;
	f = anti.f;
	if ((f & 0x10u) != 0u) {
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_02);
		a = trainer.a;
		f = trainer.f;
		AIDecidePlayPokemonCard();
		AIProcessRetreatResult retreat = AIProcessRetreat();
		a = retreat.a;
		f = retreat.f;
		if ((f & 0x10u) != 0u)
			return (AIDoTurn_LegendaryArticunoResult){f};
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10);
		a = trainer.a;
		f = trainer.f;
		if (wAlreadyPlayedEnergy == 0u)
			AIProcessAndTryToPlayEnergy();
		AIDecidePlayPokemonCard();
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_13);
		a = trainer.a;
		f = trainer.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_15);
		a = trainer.a;
		f = trainer.f;
		if ((wPreviousAIFlags & AI_FLAG_USED_PROFESSOR_OAK) != 0u) {
			trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_01);
			a = trainer.a;
			f = trainer.f;
			trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_02);
			a = trainer.a;
			f = trainer.f;
			AIDecidePlayPokemonCard();
			retreat = AIProcessRetreat();
			a = retreat.a;
			f = retreat.f;
			if ((f & 0x10u) != 0u)
				return (AIDoTurn_LegendaryArticunoResult){f};
			trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10);
			a = trainer.a;
			f = trainer.f;
			if (wAlreadyPlayedEnergy == 0u)
				AIProcessAndTryToPlayEnergy();
			AIDecidePlayPokemonCard();
		}
	}
	AIProcessAttacksResult attack = AIProcessAndTryToUseAttack();
	if ((attack.f & 0x10u) != 0u)
		return (AIDoTurn_LegendaryArticunoResult){attack.f};
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_FINISH_NO_ATTACK, b, c, d, e);
	return (AIDoTurn_LegendaryArticunoResult){decision.f};
}
/* <<< factory AIDoTurn_LegendaryArticuno */
