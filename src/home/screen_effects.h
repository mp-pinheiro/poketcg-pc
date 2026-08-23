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
/* >>> factory Func_1ce03 */
void Func_1ce03(uint8_t a);
/* <<< factory Func_1ce03 */
/* >>> factory ShakeScreenX_Big */
void ShakeScreenX_Big(void);
/* <<< factory ShakeScreenX_Big */
/* >>> factory ShakeScreenX_Small */
void ShakeScreenX_Small(void);
/* <<< factory ShakeScreenX_Small */
/* >>> factory DistortScreen */
void DistortScreen(void);
/* <<< factory DistortScreen */
/* >>> factory WhiteFlashScreen */
void WhiteFlashScreen(void);
/* <<< factory WhiteFlashScreen */
#endif /* POKETCG_HOME_SCREEN_EFFECTS_H */
