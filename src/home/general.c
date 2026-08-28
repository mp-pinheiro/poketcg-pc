#include "home/general.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "home/core.h"
#include "home/pkmn_powers.h"
#include "home/retreat.h"
#define AI_ENERGY_TRANS_RETREAT 0x09u
#define AI_FLAG_USED_SWITCH 0x02u
#define AI_TRAINER_CARD_PHASE_09 0x09u
#define TRUE 0x01u

#include "generated/wram.h"
#include "home/attacks.h"
#include "home/common.h"
#include "home/core.h"
#include "home/energy.h"
#include "home/hand_pokemon.h"
#include "home/init.h"
#include "home/pkmn_powers.h"
#define AI_ENERGY_TRANS_ATTACK 0x0du
#define AI_ENERGY_TRANS_TO_BENCH 0x0eu
#define AI_FLAG_USED_PROFESSOR_OAK 0x04u
#define AI_TRAINER_CARD_PHASE_01 0x01u
#define AI_TRAINER_CARD_PHASE_02 0x02u
#define AI_TRAINER_CARD_PHASE_03 0x03u
#define AI_TRAINER_CARD_PHASE_04 0x04u
#define AI_TRAINER_CARD_PHASE_05 0x05u
#define AI_TRAINER_CARD_PHASE_06 0x06u
#define AI_TRAINER_CARD_PHASE_07 0x07u
#define AI_TRAINER_CARD_PHASE_08 0x08u
#define AI_TRAINER_CARD_PHASE_10 0x0au
#define AI_TRAINER_CARD_PHASE_11 0x0bu
#define AI_TRAINER_CARD_PHASE_12 0x0cu
#define AI_TRAINER_CARD_PHASE_13 0x0du
#define AI_TRAINER_CARD_PHASE_15 0x0fu
#define OPPACTION_FINISH_NO_ATTACK 0x05u
/* <<< factory statics */

/* >>> factory AIProcessRetreat */
AIProcessRetreatResult AIProcessRetreat(void)
{
	uint8_t already_retreated = wAIRetreatedThisTurn;
	if (already_retreated != 0u)
		return (AIProcessRetreatResult){already_retreated, 0x00u};

	AIDecideWhetherToRetreatResult retreat = AIDecideWhetherToRetreat();
	if ((retreat.f & 0x10u) == 0u)
		return (AIProcessRetreatResult){retreat.a, retreat.f};

	AIDecideBenchPokemonToSwitchToResult bench = AIDecideBenchPokemonToSwitchTo();
	if ((bench.f & 0x10u) != 0u)
		return (AIProcessRetreatResult){bench.a, bench.f};

	wAIPlayAreaCardToSwitch = bench.a;
	wAIRetreatedThisTurn = TRUE;

	(void)AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_09);
	uint8_t previous_flags = wPreviousAIFlags;
	if ((previous_flags & AI_FLAG_USED_SWITCH) != 0u) {
		wPreviousAIFlags = (uint8_t)(previous_flags & (uint8_t)~AI_FLAG_USED_SWITCH);
		HandleAIEnergyTransResult energy = HandleAIEnergyTrans(AI_ENERGY_TRANS_RETREAT);
		return (AIProcessRetreatResult){energy.a, energy.f};
	}

	AITryToRetreatResult retreat_result = AITryToRetreat(wAIPlayAreaCardToSwitch, 0x80u);
	return (AIProcessRetreatResult){retreat_result.a, retreat_result.f};
}
/* <<< factory AIProcessRetreat */

/* >>> factory AIMainTurnLogic */
AIMainTurnLogicResult AIMainTurnLogic(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	InitAITurnVars();
	AIProcessHandTrainerCardsWrapResult trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_01);
	a = trainer.a; f = trainer.f;
	HandleAIAntiMewtwoDeckStrategyResult anti = HandleAIAntiMewtwoDeckStrategy(a, f, b, c, d, e, hl);
	a = anti.a; f = anti.f;
	if ((f & 0x10u) != 0u) {
		HandleAIGoGoRainDanceEnergyResult rain = HandleAIGoGoRainDanceEnergy(); a = rain.a; f = rain.f;
		HandleAIDamageSwapResult swap = HandleAIDamageSwap(f); a = swap.a; f = swap.f;
		HandleAIPkmnPowersResult powers = HandleAIPkmnPowers(); a = powers.a; f = powers.f;
		if ((f & 0x10u) != 0u) return (AIMainTurnLogicResult){f};
		HandleAICowardiceResult cowardice = HandleAICowardice(); a = cowardice.a; f = cowardice.f;
	}
	trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_02); a = trainer.a; f = trainer.f;
	trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_03); a = trainer.a; f = trainer.f;
	trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_04); a = trainer.a; f = trainer.f;
	AIDecidePlayPokemonCard();
	trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_05); a = trainer.a; f = trainer.f;
	trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_06); a = trainer.a; f = trainer.f;
	trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_07); a = trainer.a; f = trainer.f;
	trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_08); a = trainer.a; f = trainer.f;
	AIProcessRetreatResult retreat = AIProcessRetreat(); a = retreat.a; f = retreat.f;
	trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10); a = trainer.a; f = trainer.f;
	trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_11); a = trainer.a; f = trainer.f;
	trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_12); a = trainer.a; f = trainer.f;
	if (wAlreadyPlayedEnergy == 0u) AIProcessAndTryToPlayEnergy();
	AIDecidePlayPokemonCard();
	HandleAIDamageSwapResult swap2 = HandleAIDamageSwap(f); a = swap2.a; f = swap2.f;
	HandleAIPkmnPowersResult powers2 = HandleAIPkmnPowers(); a = powers2.a; f = powers2.f;
	if ((f & 0x10u) != 0u) return (AIMainTurnLogicResult){f};
	HandleAIGoGoRainDanceEnergyResult rain2 = HandleAIGoGoRainDanceEnergy(); a = rain2.a; f = rain2.f;
	HandleAIEnergyTransResult energy = HandleAIEnergyTrans(AI_ENERGY_TRANS_ATTACK); a = energy.a; f = energy.f;
	trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_13); a = trainer.a; f = trainer.f;
	trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_15); a = trainer.a; f = trainer.f;
	if ((wPreviousAIFlags & AI_FLAG_USED_PROFESSOR_OAK) != 0u) {
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_01); a = trainer.a; f = trainer.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_02); a = trainer.a; f = trainer.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_03); a = trainer.a; f = trainer.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_04); a = trainer.a; f = trainer.f;
		AIDecidePlayPokemonCard();
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_05); a = trainer.a; f = trainer.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_06); a = trainer.a; f = trainer.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_07); a = trainer.a; f = trainer.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_08); a = trainer.a; f = trainer.f;
		retreat = AIProcessRetreat(); a = retreat.a; f = retreat.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_10); a = trainer.a; f = trainer.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_11); a = trainer.a; f = trainer.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_12); a = trainer.a; f = trainer.f;
		if (wAlreadyPlayedEnergy == 0u) AIProcessAndTryToPlayEnergy();
		AIDecidePlayPokemonCard();
		HandleAIDamageSwapResult swap3 = HandleAIDamageSwap(f); a = swap3.a; f = swap3.f;
		HandleAIPkmnPowersResult powers3 = HandleAIPkmnPowers(); a = powers3.a; f = powers3.f;
		if ((f & 0x10u) != 0u) return (AIMainTurnLogicResult){f};
		HandleAIGoGoRainDanceEnergyResult rain3 = HandleAIGoGoRainDanceEnergy(); a = rain3.a; f = rain3.f;
		trainer = AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_13); a = trainer.a; f = trainer.f;
	}
	HandleAIEnergyTransResult bench = HandleAIEnergyTrans(AI_ENERGY_TRANS_TO_BENCH); a = bench.a; f = bench.f;
	AIProcessAttacksResult attack = AIProcessAndTryToUseAttack();
	if ((attack.f & 0x10u) != 0u) return (AIMainTurnLogicResult){attack.f};
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_FINISH_NO_ATTACK, b, c, d, e);
	return (AIMainTurnLogicResult){decision.f};
}
/* <<< factory AIMainTurnLogic */
