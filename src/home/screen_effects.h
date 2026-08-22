#ifndef POKETCG_HOME_SCREEN_EFFECTS_H
#define POKETCG_HOME_SCREEN_EFFECTS_H

#include <stdint.h>

/* >>> factory DecrementScreenAnimDuration */
typedef struct { uint16_t hl; uint8_t f; } DecrementDurResult;
DecrementDurResult DecrementScreenAnimDuration(uint8_t f);
/* <<< factory DecrementScreenAnimDuration */
/* >>> factory UpdateShakeOffset */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} UpdateShakeOffsetResult;

UpdateShakeOffsetResult UpdateShakeOffset(void);
/* <<< factory UpdateShakeOffset */
/* >>> factory DefaultScreenAnimationUpdate */
void DefaultScreenAnimationUpdate(void);
/* <<< factory DefaultScreenAnimationUpdate */
/* >>> factory DoScreenAnimationUpdate */
void DoScreenAnimationUpdate(void);
/* <<< factory DoScreenAnimationUpdate */
/* >>> factory LoadDefaultScreenAnimationUpdateWhenFinished */
void LoadDefaultScreenAnimationUpdateWhenFinished(void);
/* <<< factory LoadDefaultScreenAnimationUpdateWhenFinished */
/* >>> factory ShakeScreenX */
void ShakeScreenX(uint16_t hl);
/* <<< factory ShakeScreenX */
#endif /* POKETCG_HOME_SCREEN_EFFECTS_H */
