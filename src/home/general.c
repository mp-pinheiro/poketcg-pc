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
