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
