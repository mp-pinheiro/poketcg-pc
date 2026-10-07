#ifndef POKETCG_HOME_PLAY_ANIMATION_H
#define POKETCG_HOME_PLAY_ANIMATION_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part AnimationStatusResult */
typedef struct {
	uint8_t a;
	uint8_t f;
} AnimationStatusResult;
/* <<< part AnimationStatusResult */

/* >>> part FrameFunctionResult */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} FrameFunctionResult;
/* <<< part FrameFunctionResult */

/* >>> factory CheckAnyAnimationPlaying */
AnimationStatusResult CheckAnyAnimationPlaying(void);
/* <<< factory CheckAnyAnimationPlaying */
/* >>> factory SetDoFrameFunction */
FrameFunctionResult SetDoFrameFunction(uint16_t hl);
/* <<< factory SetDoFrameFunction */
/* >>> factory ResetDoFrameFunction */
FrameFunctionResult ResetDoFrameFunction(uint16_t hl);
/* <<< factory ResetDoFrameFunction */

/* >>> factory PlayDuelAnimation */
typedef struct {
	uint8_t a;
} PlayDuelAnimationResult;

PlayDuelAnimationResult PlayDuelAnimation(uint8_t a);
/* <<< factory PlayDuelAnimation */
/* >>> factory UpdateQueuedAnimations */
typedef struct {
	uint8_t a;
	uint16_t hl;
} UpdateQueuedAnimationsResult;

UpdateQueuedAnimationsResult UpdateQueuedAnimations(uint16_t hl);
/* <<< factory UpdateQueuedAnimations */
/* >>> factory Func_3bb5 */
void Func_3bb5(void (*effect)(void));
/* <<< factory Func_3bb5 */
#endif
