#ifndef POKETCG_HOME_COMMANDS_H
#define POKETCG_HOME_COMMANDS_H

#include <stdint.h>

/* >>> factory AnimationCommand_AnimEnd2 */
uint8_t AnimationCommand_AnimEnd2(uint8_t a);
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
/* >>> factory AnimationCommand_AnimEnd */
uint8_t AnimationCommand_AnimEnd(uint8_t a);
/* <<< factory AnimationCommand_AnimEnd */
#endif
