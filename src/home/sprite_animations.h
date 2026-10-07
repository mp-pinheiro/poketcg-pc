#ifndef POKETCG_HOME_SPRITE_ANIMATIONS_H
#define POKETCG_HOME_SPRITE_ANIMATIONS_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part SpriteAnimLookupResult */
typedef struct { uint8_t a, f; } SpriteAnimLookupResult;
/* <<< part SpriteAnimLookupResult */

/* >>> factory _ClearSpriteAnimations */
void _ClearSpriteAnimations(void);
/* <<< factory _ClearSpriteAnimations */
/* >>> factory CreateSpriteAndAnimBufferEntry */
uint8_t CreateSpriteAndAnimBufferEntry(uint8_t a, uint8_t f);
/* <<< factory CreateSpriteAndAnimBufferEntry */
/* >>> factory FillNewSpriteAnimBufferEntry */
void FillNewSpriteAnimBufferEntry(uint16_t hl);
/* <<< factory FillNewSpriteAnimBufferEntry */
/* >>> factory DisableCurSpriteAnim */
void DisableCurSpriteAnim(void);
/* <<< factory DisableCurSpriteAnim */
/* >>> factory DisableSpriteAnim */
void DisableSpriteAnim(uint8_t a);
/* <<< factory DisableSpriteAnim */
/* >>> factory GetSpriteAnimCounter */
uint8_t GetSpriteAnimCounter(void);
/* <<< factory GetSpriteAnimCounter */
/* >>> factory _HandleAllSpriteAnimations */
void _HandleAllSpriteAnimations(void);
/* <<< factory _HandleAllSpriteAnimations */
/* >>> factory LoadSpriteDataForAnimationFrame */
void LoadSpriteDataForAnimationFrame(uint16_t hl);
/* <<< factory LoadSpriteDataForAnimationFrame */
/* >>> factory TryHandleSpriteAnimationFrame */
void TryHandleSpriteAnimationFrame(uint16_t hl);
/* <<< factory TryHandleSpriteAnimationFrame */
/* >>> factory StartNewSpriteAnimation */
void StartNewSpriteAnimation(uint8_t a);
/* <<< factory StartNewSpriteAnimation */
/* >>> factory StartSpriteAnimation */
uint8_t StartSpriteAnimation(uint8_t a);
/* <<< factory StartSpriteAnimation */
/* >>> factory Func_12ac9 */
void Func_12ac9(uint8_t a, uint8_t c);
/* <<< factory Func_12ac9 */
/* >>> factory LoadSpriteAnimPointers */
uint16_t LoadSpriteAnimPointers(uint8_t a);
/* <<< factory LoadSpriteAnimPointers */
/* >>> factory HandleAnimationFrame */
uint8_t HandleAnimationFrame(uint16_t hl);
/* <<< factory HandleAnimationFrame */
/* >>> factory GetAnimFramePointerFromOffset */
void GetAnimFramePointerFromOffset(uint8_t a, uint16_t hl);
/* <<< factory GetAnimFramePointerFromOffset */
/* >>> factory SetAnimationCounterAndLoop */
uint8_t SetAnimationCounterAndLoop(uint8_t a, uint16_t hl);
/* <<< factory SetAnimationCounterAndLoop */
/* >>> factory Func_12ba7 */
void Func_12ba7(void);
/* <<< factory Func_12ba7 */
/* >>> factory Func_12bcd */
void Func_12bcd(void);
/* <<< factory Func_12bcd */
/* >>> factory ClearSpriteVRAMBuffer */
void ClearSpriteVRAMBuffer(void);
/* <<< factory ClearSpriteVRAMBuffer */
/* >>> factory Func_12c05 */
SpriteAnimLookupResult Func_12c05(uint8_t a);
/* <<< factory Func_12c05 */
/* >>> factory Func_12c4f */
uint8_t Func_12c4f(uint8_t a, uint8_t d);
/* <<< factory Func_12c4f */
/* >>> factory Func_12c5e */
void Func_12c5e(void);
/* <<< factory Func_12c5e */

#endif
