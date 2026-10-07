#ifndef POKETCG_HOME_LOAD_ANIMATION_H
#define POKETCG_HOME_LOAD_ANIMATION_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory GetFirstSpriteAnimBufferProperty */
uint16_t GetFirstSpriteAnimBufferProperty(void);
/* <<< factory GetFirstSpriteAnimBufferProperty */
/* >>> factory GetSpriteAnimBufferProperty */
uint16_t GetSpriteAnimBufferProperty(uint8_t c);
/* <<< factory GetSpriteAnimBufferProperty */
/* >>> factory GetSpriteAnimBufferProperty_SpriteInA */
uint16_t GetSpriteAnimBufferProperty_SpriteInA(uint8_t a, uint8_t c);
/* <<< factory GetSpriteAnimBufferProperty_SpriteInA */
/* >>> factory Func_3ddb */
void Func_3ddb(uint8_t a);
/* <<< factory Func_3ddb */
/* >>> factory Func_3de7 */
void Func_3de7(uint8_t a);
/* <<< factory Func_3de7 */
/* >>> factory DrawSpriteAnimationFrame */
void DrawSpriteAnimationFrame(uint16_t *hl);
/* <<< factory DrawSpriteAnimationFrame */
/* >>> factory GetAnimationFramePointer */
void GetAnimationFramePointer(uint16_t hl);
/* <<< factory GetAnimationFramePointer */

/* >>> factory ClearSpriteAnimations */
void ClearSpriteAnimations(void);
/* <<< factory ClearSpriteAnimations */
/* >>> factory HandleAllSpriteAnimations */
void HandleAllSpriteAnimations(void);
/* <<< factory HandleAllSpriteAnimations */
/* >>> factory EnableAndClearSpriteAnimations */
void EnableAndClearSpriteAnimations(void);
/* <<< factory EnableAndClearSpriteAnimations */
/* >>> factory DrawPortrait */
void DrawPortrait(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory DrawPortrait */
/* >>> factory DrawOpponentPortrait */
void DrawOpponentPortrait(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory DrawOpponentPortrait */
/* >>> factory DrawPlayerPortrait */
void DrawPlayerPortrait(uint8_t b, uint8_t c);
/* <<< factory DrawPlayerPortrait */
/* >>> factory Func_3e31 */
void Func_3e31(void);
/* <<< factory Func_3e31 */
/* >>> factory LoadScene */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } LoadSceneResult;
LoadSceneResult LoadScene(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory LoadScene */
#endif
