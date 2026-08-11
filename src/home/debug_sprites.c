#include "home/debug_sprites.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/load_animation.h"
#include "home/random.h"
#include "mem.h"

#define PAD_B 0x02u
#define PAD_RIGHT 0x10u
#define PAD_LEFT 0x20u
#define PAD_UP 0x40u
#define PAD_DOWN 0x80u
#define SPRITE_ANIM_FLAGS 15u
#define SPRITE_ANIM_FLAG_X_INVERTED 1u
#define SPRITE_ANIM_FLAG_CENTERED 4u
#define SPRITE_ANIM_FLAG_CENTERED_F 2u
void Func_1c865(void)
{
}

static void adjust_scroll(uint8_t keys)
{
	uint8_t b = gb_read8(hSCX_ADDR);
	uint8_t c = gb_read8(hSCY_ADDR);
	if (keys & PAD_UP)
		c++;
	if (keys & PAD_DOWN)
		c--;
	if (keys & PAD_LEFT)
		b++;
	if (keys & PAD_RIGHT)
		b--;
	gb_write8(hSCX_ADDR, b);
	gb_write8(hSCY_ADDR, c);
}

void Func_1c866(void)
{
	uint8_t keys = gb_read8(hKeysHeld_ADDR);
	adjust_scroll(keys);
	if (keys & PAD_B)
		adjust_scroll(keys);
}

uint8_t Func_1c890(uint8_t *c_io, uint16_t *hl_io)
{
	uint8_t a = (uint8_t)(gb_read8(wVBlankCounter_ADDR) & 0x3fu);
	if (a != 0)
		return a;
	uint8_t state = gb_read8(wd41b_ADDR);
	a = state;
	if (state != 0x11u && (state < 0x0eu || state >= 0x10u))
		return a;
	*c_io = SPRITE_ANIM_FLAGS;
	gb_write8(wWhichSprite_ADDR, gb_read8(wd41c_ADDR));
	*hl_io = GetSpriteAnimBufferProperty(SPRITE_ANIM_FLAGS);
	a = (uint8_t)(UpdateRNGSources() & SPRITE_ANIM_FLAG_X_INVERTED);
	uint8_t flags = gb_read8(*hl_io);
	if (a != 0)
		flags |= (uint8_t)(1u << SPRITE_ANIM_FLAG_CENTERED_F);
	else
		flags &= (uint8_t)~(1u << SPRITE_ANIM_FLAG_CENTERED_F);
	gb_write8(*hl_io, flags);
	return a;
}
