#ifndef POKETCG_HOME_SPRITE_ANIMATIONS_H
#define POKETCG_HOME_SPRITE_ANIMATIONS_H

#include <stdint.h>

typedef struct { uint8_t a, f; } SpriteAnimLookupResult;

void _ClearSpriteAnimations(void);
uint8_t CreateSpriteAndAnimBufferEntry(uint8_t a, uint8_t f);
void FillNewSpriteAnimBufferEntry(uint16_t hl);
void DisableCurSpriteAnim(void);
void DisableSpriteAnim(uint8_t a);
uint8_t GetSpriteAnimCounter(void);
void _HandleAllSpriteAnimations(void);
void LoadSpriteDataForAnimationFrame(uint16_t hl);
void TryHandleSpriteAnimationFrame(uint16_t hl);
void StartNewSpriteAnimation(uint8_t a);
void StartSpriteAnimation(uint8_t a);
void Func_12ac9(uint8_t a, uint8_t c);
uint16_t LoadSpriteAnimPointers(uint8_t a);
void HandleAnimationFrame(uint16_t hl);
void GetAnimFramePointerFromOffset(uint8_t a, uint16_t hl);
uint8_t SetAnimationCounterAndLoop(uint8_t a, uint16_t hl);
void Func_12ba7(void);
void Func_12bcd(void);
void ClearSpriteVRAMBuffer(void);
SpriteAnimLookupResult Func_12c05(uint8_t a);
uint8_t Func_12c4f(uint8_t a, uint8_t d);
void Func_12c5e(void);

#endif
