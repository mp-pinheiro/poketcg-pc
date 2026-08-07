#ifndef POKETCG_HOME_PLAY_ANIMATION_H
#define POKETCG_HOME_PLAY_ANIMATION_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
} AnimationStatusResult;

typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} FrameFunctionResult;

AnimationStatusResult CheckAnyAnimationPlaying(void);
FrameFunctionResult SetDoFrameFunction(uint16_t hl);
FrameFunctionResult ResetDoFrameFunction(uint16_t hl);

#endif
