#include "home/overworld_map.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/load_animation.h"

#define SPRITE_ANIM_COORD_X 0x02u
/* <<< factory statics */

/* >>> factory OverworldMap_ContinuePlayerWalkingAnimation */
/* overworld_map.asm:540-566 */
void OverworldMap_ContinuePlayerWalkingAnimation(void)
{
	uint8_t horizontal_subpixel = wOverworldMapPlayerHorizontalSubPixelPosition;
	uint8_t vertical_subpixel = wOverworldMapPlayerVerticalSubPixelPosition;
	uint16_t hl = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);

	uint16_t horizontal_sum = (uint16_t)wOverworldMapPlayerPathHorizontalMovement + horizontal_subpixel;
	uint8_t horizontal_high = gb_read8((uint16_t)(wOverworldMapPlayerPathHorizontalMovement_ADDR + 1u));
	uint8_t horizontal_coordinate = gb_read8(hl);
	gb_write8(hl, (uint8_t)(horizontal_high + horizontal_coordinate + (horizontal_sum > 0xffu)));
	hl = (uint16_t)(hl + 1u);

	uint16_t vertical_sum = (uint16_t)wOverworldMapPlayerPathVerticalMovement + vertical_subpixel;
	uint8_t vertical_high = gb_read8((uint16_t)(wOverworldMapPlayerPathVerticalMovement_ADDR + 1u));
	uint8_t vertical_coordinate = gb_read8(hl);
	gb_write8(hl, (uint8_t)(vertical_high + vertical_coordinate + (vertical_sum > 0xffu)));

	wOverworldMapPlayerHorizontalSubPixelPosition = (uint8_t)horizontal_sum;
	wOverworldMapPlayerVerticalSubPixelPosition = (uint8_t)vertical_sum;
	wOverworldMapPlayerMovementCounter--;
}
/* <<< factory OverworldMap_ContinuePlayerWalkingAnimation */

/* >>> factory OverworldMap_NegateBC */
OverworldMapNegateBCResult OverworldMap_NegateBC(uint8_t b, uint8_t c)
{
	uint16_t low_sum = (uint16_t)(c ^ 0xffu) + 1u;
	uint8_t out_c = (uint8_t)low_sum;
	uint8_t carry = (uint8_t)(low_sum > 0xffu);
	uint16_t high_sum = (uint16_t)(b ^ 0xffu) + carry;
	uint8_t out_b = (uint8_t)high_sum;
	uint8_t half_carry = (uint8_t)((((uint16_t)(b ^ 0xffu) & 0x0fu) + carry) > 0x0fu);
	OverworldMapNegateBCResult result = {
		.a = out_b,
		.f = (uint8_t)((out_b == 0u ? 0x80u : 0u) |
			(half_carry ? 0x20u : 0u) |
			(high_sum > 0xffu ? 0x10u : 0u)),
		.b = out_b,
		.c = out_c,
	};
	return result;
}
/* <<< factory OverworldMap_NegateBC */
