#include "home/attacks.h"

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/hram.h"
#include "home/core.h"

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/special_attacks.h"
#include "home/damage_calculation.h"
#define AI_FLAG_USED_PLUSPOWER 0x01u
#define AI_MEWTWO_MILL 0x80u
#define AI_TRAINER_CARD_PHASE_14 0x0eu
#define ATTACK_FLAG1_ADDRESS 0x00u
#define DAMAGE_TO_OPPONENT_BENCH_F 0x05u
#define FIRST_ATTACK_OR_PKMN_POWER 0x00u
#define PLAY_AREA_ARENA 0x00u
#define SECOND_ATTACK 0x01u
#define TRUE 0x01u

#include "generated/wram.h"
#include "home/attacks.h"
/* <<< factory statics */

/* engine/duel/ai/attacks.asm:26-41 */
void RetrievePlayAreaAIScoreFromBackup2(void)
{
	for (uint8_t i = 0; i < 6; i++)
		gb_write8((uint16_t)(wPlayAreaAIScore_ADDR + i),
			  gb_read8((uint16_t)(wTempPlayAreaAIScore_ADDR + i)));
	gb_write8(wAIScore_ADDR, gb_read8(wTempAIScore_ADDR));
}

/* >>> factory GetAIScoreOfAttack */
void GetAIScoreOfAttack(uint8_t a)
{
	wSelectedAttack = a;
	wAIScore = 0x50u;
	hTempPlayAreaLocation_ff9d = 0u;
	CheckIfSelectedAttackIsUnusableResult unusable =
		CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	if ((unusable.f & 0x10u) != 0u)
		wAIScore = 0u;
}
/* <<< factory GetAIScoreOfAttack */

/* >>> factory AIProcessAttacks */
AIProcessAttacksResult AIProcessAttacks(void)
{
	if ((wPreviousAIFlags & AI_FLAG_USED_PLUSPOWER) != 0u) {
		wSelectedAttack = wAIPlusPowerAttack;
		goto attack_chosen;
	}
	if (wAIBarrierFlagCounter == AI_MEWTWO_MILL)
		goto dont_attack;

	GetAIScoreOfAttack(FIRST_ATTACK_OR_PKMN_POWER);
	wFirstAttackAIScore = wAIScore;
	GetAIScoreOfAttack(SECOND_ATTACK);

	uint8_t chosen_attack = SECOND_ATTACK;
	uint8_t chosen_score = wAIScore;
	if (chosen_score < wFirstAttackAIScore) {
		chosen_attack = FIRST_ATTACK_OR_PKMN_POWER;
		chosen_score = wFirstAttackAIScore;
	}
	if (chosen_score < 0x50u)
		goto dont_attack;
	wSelectedAttack = chosen_attack;
	if (chosen_attack != FIRST_ATTACK_OR_PKMN_POWER)
		CheckWhetherToSwitchToFirstAttack();

attack_chosen:
	if (wAIExecuteProcessedAttack != 0u) {
		RetrievePlayAreaAIScoreFromBackup2();
		return (AIProcessAttacksResult){0x10u};
	}

	(void)AIProcessHandTrainerCards(AI_TRAINER_CARD_PHASE_14);
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
	if (wDamage != 0u)
		goto can_damage;
	{
		AttackFlagResult bench = CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | DAMAGE_TO_OPPONENT_BENCH_F);
		if ((bench.f & 0x10u) != 0u)
			goto can_damage;
	}
	wAIRetreatScore = (uint8_t)(wAIRetreatScore + 1u);
	goto use_attack;

can_damage:
	wAIRetreatScore = 0u;

use_attack:
	wAITriedAttack = TRUE;
	{
		AITryUseAttackResult tried = AITryUseAttack(TRUE);
		return (AIProcessAttacksResult){(uint8_t)((tried.f & 0x80u) | 0x10u)};
	}

dont_attack:
	if (wAIExecuteProcessedAttack != 0u) {
		RetrievePlayAreaAIScoreFromBackup2();
		return (AIProcessAttacksResult){0x00u};
	}
	wAIRetreatScore = (uint8_t)(wAIRetreatScore + 1u);
	return (AIProcessAttacksResult){0x80u};
}
/* <<< factory AIProcessAttacks */

/* >>> factory AIProcessAndTryToUseAttack */
AIProcessAttacksResult AIProcessAndTryToUseAttack(void)
{
	wAIExecuteProcessedAttack = 0u;
	return AIProcessAttacks();
}
/* <<< factory AIProcessAndTryToUseAttack */
