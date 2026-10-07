#ifndef POKETCG_HOME_DUEL_CORE_H
#define POKETCG_HOME_DUEL_CORE_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part TrainerConvertResult */
/* poketcg/src/engine/duel/core.asm */

typedef struct {
	uint8_t a;
	uint8_t c;
	uint16_t hl;
} TrainerConvertResult;
/* <<< part TrainerConvertResult */

/* >>> factory ConvertSpecialTrainerCardToPokemon */
TrainerConvertResult ConvertSpecialTrainerCardToPokemon(uint8_t a, uint16_t hl, uint16_t de);
/* <<< factory ConvertSpecialTrainerCardToPokemon */
/* >>> factory ResetAttackAnimationIsPlaying */
void ResetAttackAnimationIsPlaying(void);
/* <<< factory ResetAttackAnimationIsPlaying */
/* >>> factory ClearNonTurnTemporaryDuelvars */
void ClearNonTurnTemporaryDuelvars(void);
/* <<< factory ClearNonTurnTemporaryDuelvars */
/* >>> factory ClearNonTurnTemporaryDuelvars_CopyStatus */
void ClearNonTurnTemporaryDuelvars_CopyStatus(void);
/* <<< factory ClearNonTurnTemporaryDuelvars_CopyStatus */
/* >>> factory UpdateArenaCardLastTurnDamage */
void UpdateArenaCardLastTurnDamage(void);
/* <<< factory UpdateArenaCardLastTurnDamage */
/* >>> part CardOneStageBelowResult */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
	uint8_t f;
} CardOneStageBelowResult;
/* <<< part CardOneStageBelowResult */

/* >>> factory GetCardOneStageBelow */
CardOneStageBelowResult GetCardOneStageBelow(uint8_t d, uint8_t e);
/* <<< factory GetCardOneStageBelow */

/* >>> factory PrintThereWasNoEffectFromStatusText */
uint16_t PrintThereWasNoEffectFromStatusText(void);
/* <<< factory PrintThereWasNoEffectFromStatusText */
/* >>> factory WaitAttackAnimation */
void WaitAttackAnimation(void);
/* <<< factory WaitAttackAnimation */
/* >>> factory ApplyStatusConditionQueue */
uint8_t ApplyStatusConditionQueue(void);
/* <<< factory ApplyStatusConditionQueue */

/* >>> factory SetDefaultConsolePalettes */
void SetDefaultConsolePalettes(void);
/* <<< factory SetDefaultConsolePalettes */
#endif
