#include "home/load_animation.h"

#include "generated/wram.h"
#include "mem.h"

#define SPRITE_ANIM_BUFFER_CAPACITY 16u
#define SPRITE_ANIM_LENGTH 16u
#define SPRITE_ANIM_ENABLED 0u
#define SPRITE_ANIM_FLAGS 15u
#define SPRITE_ANIM_FLAG_CENTERED_F 2u

uint16_t GetSpriteAnimBufferProperty_SpriteInA(uint8_t a, uint8_t c)
{
	if (a >= SPRITE_ANIM_BUFFER_CAPACITY)
		a = SPRITE_ANIM_BUFFER_CAPACITY - 1u;
	return (uint16_t)(wSpriteAnimBuffer_ADDR + (uint16_t)a * SPRITE_ANIM_LENGTH + c);
}

uint16_t GetSpriteAnimBufferProperty(uint8_t c)
{
	return GetSpriteAnimBufferProperty_SpriteInA(gb_read8(wWhichSprite_ADDR), c);
}

uint16_t GetFirstSpriteAnimBufferProperty(void)
{
	return GetSpriteAnimBufferProperty_SpriteInA(SPRITE_ANIM_ENABLED, 0);
}

void Func_3ddb(uint8_t a)
{
	uint16_t address = GetSpriteAnimBufferProperty_SpriteInA(a, SPRITE_ANIM_FLAGS);
	gb_write8(address, (uint8_t)(gb_read8(address) & (uint8_t)~(1u << SPRITE_ANIM_FLAG_CENTERED_F)));
}

void Func_3de7(uint8_t a)
{
	uint16_t address = GetSpriteAnimBufferProperty_SpriteInA(a, SPRITE_ANIM_FLAGS);
	gb_write8(address, (uint8_t)(gb_read8(address) | (uint8_t)(1u << SPRITE_ANIM_FLAG_CENTERED_F)));
}
