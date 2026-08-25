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
void AnimationCommand_AnimEnd(void);
/* <<< factory AnimationCommand_AnimEnd */
/* >>> factory DuelAnim154 */
void DuelAnim154(void);
/* <<< factory DuelAnim154 */
/* >>> factory DuelAnim155 */
void DuelAnim155(void);
/* <<< factory DuelAnim155 */
/* >>> factory DuelAnim156 */
void DuelAnim156(void);
/* <<< factory DuelAnim156 */
/* >>> factory GetDamageText */
uint16_t GetDamageText(uint16_t hl);
/* <<< factory GetDamageText */
/* >>> factory PlayAttackAnimationCommands_NextCommand */
typedef struct {
	uint8_t d;
	uint8_t e;
} PlayAttackAnimationCommands_NextCommandResult;

PlayAttackAnimationCommands_NextCommandResult PlayAttackAnimationCommands_NextCommand(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory PlayAttackAnimationCommands_NextCommand */
/* >>> factory DuelAnim157 */
/* poketcg/src/engine/duel/animations/commands.asm */
void DuelAnim157(void);
/* <<< factory DuelAnim157 */
/* >>> factory PrintDamageText */
/* poketcg/src/engine/duel/animations/commands.asm */
typedef struct {
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} PrintDamageTextResult;

PrintDamageTextResult PrintDamageText(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PrintDamageText */
/* >>> factory UpdateMainSceneHUD */
void UpdateMainSceneHUD(void);
/* <<< factory UpdateMainSceneHUD */
#endif
