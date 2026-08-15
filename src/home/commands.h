#ifndef POKETCG_HOME_COMMANDS_H
#define POKETCG_HOME_COMMANDS_H

#include <stdint.h>

/* >>> factory AnimationCommand_AnimEnd2 */
void AnimationCommand_AnimEnd2(void);
/* <<< factory AnimationCommand_AnimEnd2 */

/* >>> factory UpdateDuelAnimationScreen */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} UpdateDuelAnimationScreenResult;

UpdateDuelAnimationScreenResult UpdateDuelAnimationScreen(uint16_t hl);
/* <<< factory UpdateDuelAnimationScreen */

/* >>> factory DuelAnim153 */
void DuelAnim153(void);
/* <<< factory DuelAnim153 */
#endif
