#ifndef POKETCG_HOME_LOAD_ANIMATION_H
#define POKETCG_HOME_LOAD_ANIMATION_H

#include <stdint.h>

uint16_t GetFirstSpriteAnimBufferProperty(void);
uint16_t GetSpriteAnimBufferProperty(uint8_t c);
uint16_t GetSpriteAnimBufferProperty_SpriteInA(uint8_t a, uint8_t c);
void Func_3ddb(uint8_t a);
void Func_3de7(uint8_t a);
void DrawSpriteAnimationFrame(uint16_t *hl);
void GetAnimationFramePointer(uint16_t hl);

#endif
