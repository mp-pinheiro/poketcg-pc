#include "home/overworld_map.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/load_animation.h"

#define SPRITE_ANIM_COORD_X 0x02u

#include "generated/wram.h"
#include "home/sprite_animations.h"
#include "home/load_animation.h"

#define CONSOLE_CGB 0x02u
#define SPRITE_ANIM_CGB_VOLCANO_SMOKE 0x37u
#define SPRITE_ANIM_SGB_VOLCANO_SMOKE 0x34u
#define SPRITE_OW_MAP_OAM 0x25u

#include "generated/wram.h"
#include "home/sprite_animations.h"

#include "home/overworld_map.h"
#include "generated/wram.h"

#define NORTH 0x00u

static const uint8_t overworld_map_warps[13][4] = {
	{0x00u, 0x00u, 0x00u, 0x00u},
	{0x01u, 0x0eu, 0x1au, 0x00u},
	{0x03u, 0x08u, 0x14u, 0x00u},
	{0x04u, 0x08u, 0x0eu, 0x00u},
	{0x07u, 0x08u, 0x0eu, 0x00u},
	{0x0au, 0x08u, 0x0eu, 0x00u},
	{0x0du, 0x08u, 0x0eu, 0x00u},
	{0x10u, 0x08u, 0x0eu, 0x00u},
	{0x13u, 0x08u, 0x0eu, 0x00u},
	{0x16u, 0x08u, 0x0eu, 0x00u},
	{0x19u, 0x08u, 0x0eu, 0x00u},
	{0x1cu, 0x08u, 0x0eu, 0x00u},
	{0x1fu, 0x0eu, 0x0eu, 0x00u},
};

#include "home/division.h"
#include "home/overworld_map.h"
#include "generated/wram.h"

#define EAST 0x01u
#define WEST 0x03u

#include "generated/wram.h"
#include "home/scripting.h"

#define EVENT_ISHIHARAS_HOUSE_MENTIONED 0x1eu
#define OWMAP_ISHIHARAS_HOUSE 0x02u
#define OWMAP_MYSTERY_HOUSE 0x0du

#include "generated/wram.h"
#include "mem.h"
#include "home/load_animation.h"
#include "home/scripting.h"
#include "home/sprite_animations.h"

#define EVENT_MASON_LAB_STATE 0x3eu
#define SPRITE_ANIM_CGB_OWMAP_CURSOR 0x38u
#define SPRITE_ANIM_FLAGS 0x0fu
#define SPRITE_ANIM_FLAG_UNSKIPPABLE_F 0x07u
#define SPRITE_ANIM_SGB_OWMAP_CURSOR 0x35u

#include "home/load_animation.h"
#include "home/overworld_map.h"
#include "mem.h"
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

/* >>> factory OverworldMap_InitVolcanoSprite */
void OverworldMap_InitVolcanoSprite(uint8_t f)
{
	(void)CreateSpriteAndAnimBufferEntry(SPRITE_OW_MAP_OAM, f);
	uint16_t coords = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
	gb_write8(coords, 0x80u);
	gb_write8((uint16_t)(coords + 1u), 0x10u);
	uint8_t animation = SPRITE_ANIM_SGB_VOLCANO_SMOKE;
	if (wConsole == CONSOLE_CGB)
		animation = SPRITE_ANIM_CGB_VOLCANO_SMOKE;
	StartNewSpriteAnimation(animation);
}
/* <<< factory OverworldMap_InitVolcanoSprite */

/* >>> factory OverworldMap_UpdateCursorAnimation */
void OverworldMap_UpdateCursorAnimation(void)
{
	wWhichSprite = wOverworldMapCursorSprite;
	uint8_t animation = (uint8_t)(wOverworldMapCursorAnimation + 1u);
	StartNewSpriteAnimation(animation);
}
/* <<< factory OverworldMap_UpdateCursorAnimation */

/* >>> factory OverworldMap_LoadSelectedMap */
void OverworldMap_LoadSelectedMap(void)
{
	uint8_t selection = wOverworldMapSelection;
	const uint8_t *warp = overworld_map_warps[selection];
	wTempMap = warp[0];
	wTempPlayerXCoord = warp[1];
	wTempPlayerYCoord = warp[2];
	wTempPlayerDirection = NORTH;
	wOverworldTransition |= 0x10u;
}
/* <<< factory OverworldMap_LoadSelectedMap */

/* >>> factory OverworldMap_InitPlayerEastWestMovement */
void OverworldMap_InitPlayerEastWestMovement(uint8_t b, uint8_t c)
{
	uint8_t horizontal_sign = gb_read8((uint16_t)(wOverworldMapPlayerPathHorizontalMovement_ADDR + 1u));
	uint8_t vertical_sign = gb_read8((uint16_t)(wOverworldMapPlayerPathVerticalMovement_ADDR + 1u));
	wOverworldMapPlayerMovementCounter = b;

	wOverworldMapPlayerPathHorizontalMovement = 0u;
	gb_write8((uint16_t)(wOverworldMapPlayerPathHorizontalMovement_ADDR + 1u),
		(horizontal_sign & 0x80u) != 0u ? 0xffu : 0x01u);

	DivResult divided = DivideBCbyDE((uint16_t)((uint16_t)c << 8), (uint16_t)b);
	uint16_t quotient = divided.quotient;
	if ((vertical_sign & 0x80u) != 0u) {
		OverworldMapNegateBCResult negated = OverworldMap_NegateBC((uint8_t)(quotient >> 8), (uint8_t)quotient);
		quotient = (uint16_t)(((uint16_t)negated.b << 8) | negated.c);
	}
	wOverworldMapPlayerPathVerticalMovement = (uint8_t)quotient;
	gb_write8((uint16_t)(wOverworldMapPlayerPathVerticalMovement_ADDR + 1u),
		(uint8_t)(quotient >> 8));

	wPlayerDirection = (horizontal_sign & 0x80u) != 0u ? WEST : EAST;
}
/* <<< factory OverworldMap_InitPlayerEastWestMovement */

/* >>> factory OverworldMap_GetOWMapID */
uint8_t OverworldMap_GetOWMapID(void)
{
	uint8_t selection = wOverworldMapSelection;
	if (selection != OWMAP_ISHIHARAS_HOUSE)
		return selection;
	if (GetEventValue(EVENT_ISHIHARAS_HOUSE_MENTIONED) != 0u)
		return selection;
	return OWMAP_MYSTERY_HOUSE;
}
/* <<< factory OverworldMap_GetOWMapID */

/* >>> factory OverworldMap_InitCursorSprite */
void OverworldMap_InitCursorSprite(void)
{
	wOverworldMapStartingPosition = wOverworldMapSelection;
	wOverworldMapPlayerAnimationState = 0u;
	(void)CreateSpriteAndAnimBufferEntry(SPRITE_OW_MAP_OAM, 0x80u);
	wOverworldMapCursorSprite = wWhichSprite;
	uint8_t animation = SPRITE_ANIM_SGB_OWMAP_CURSOR;
	if (wConsole == CONSOLE_CGB)
		animation = SPRITE_ANIM_CGB_OWMAP_CURSOR;
	wOverworldMapCursorAnimation = animation;
	StartNewSpriteAnimation(animation);
	if (GetEventValue(EVENT_MASON_LAB_STATE) == 0u) {
		uint16_t flags = GetSpriteAnimBufferProperty(SPRITE_ANIM_FLAGS);
		gb_write8(flags, (uint8_t)(gb_read8(flags) | (uint8_t)(1u << SPRITE_ANIM_FLAG_UNSKIPPABLE_F)));
	}
}
/* <<< factory OverworldMap_InitCursorSprite */

/* >>> factory OverworldMap_GetMapPosition */
OverworldMapGetMapPositionResult OverworldMap_GetMapPosition(uint8_t a, uint8_t d, uint8_t e)
{
	static const uint8_t map_positions[] = {
		0x00u, 0x00u,
		0x0Cu, 0x68u,
		0x04u, 0x18u,
		0x34u, 0x68u,
		0x14u, 0x38u,
		0x6Cu, 0x64u,
		0x24u, 0x50u,
		0x7Cu, 0x40u,
		0x5Cu, 0x2Cu,
		0x7Cu, 0x20u,
		0x6Cu, 0x10u,
		0x3Cu, 0x20u,
		0x44u, 0x44u,
	};
	uint8_t index = (uint8_t)(a << 1u);
	uint8_t x = (uint8_t)((uint8_t)(map_positions[index] + 0x08u) + d);
	uint8_t y_base = (uint8_t)(map_positions[(uint8_t)(index + 1u)] + 0x10u);
	uint16_t y_sum = (uint16_t)y_base + e;
	OverworldMapGetMapPositionResult result = {
		.a = (uint8_t)y_sum,
		.f = (uint8_t)(((uint8_t)y_sum == 0u ? 0x80u : 0u) |
			((((uint8_t)(y_base & 0x0Fu) + (uint8_t)(e & 0x0Fu)) > 0x0Fu) ? 0x20u : 0u) |
			((y_sum > 0xFFu) ? 0x10u : 0u)),
		.d = x,
		.e = (uint8_t)y_sum,
	};
	return result;
}
/* <<< factory OverworldMap_GetMapPosition */

/* >>> factory OverworldMap_SetSpritePosition */
void OverworldMap_SetSpritePosition(uint8_t a, uint8_t d, uint8_t e)
{
	OverworldMapGetMapPositionResult position = OverworldMap_GetMapPosition(a, d, e);
	uint16_t hl = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
	gb_write8(hl, position.d);
	gb_write8((uint16_t)(hl + 1u), position.e);
}
/* <<< factory OverworldMap_SetSpritePosition */
