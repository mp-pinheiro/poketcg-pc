#ifndef POKETCG_HOME_DUEL_CORE_H
#define POKETCG_HOME_DUEL_CORE_H

#include <stdint.h>

/* poketcg/src/engine/duel/core.asm */

typedef struct {
	uint8_t a;
	uint8_t c;
	uint16_t hl;
} TrainerConvertResult;

TrainerConvertResult ConvertSpecialTrainerCardToPokemon(uint8_t a, uint16_t hl, uint16_t de);
void ResetAttackAnimationIsPlaying(void);
void ClearNonTurnTemporaryDuelvars(void);
void ClearNonTurnTemporaryDuelvars_CopyStatus(void);
void UpdateArenaCardLastTurnDamage(void);
uint16_t PrintThereWasNoEffectFromStatusText(void);

void WaitAttackAnimation(void);

#endif
