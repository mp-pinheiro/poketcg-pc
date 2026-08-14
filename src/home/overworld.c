#include "home/overworld.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/load_animation.h"
#include "mem.h"

#define SPRITE_ANIM_COUNTER          0x0eu
#define SPRITE_ANIM_FLAGS            0x0fu
#define SPRITE_ANIM_FLAG_CENTERED_F  0x02u

#include "home/copy.h"
#include "home/print_text.h"
/* <<< factory statics */

/* >>> factory Func_c6cc */
/* overworld.asm:1027-1033. a += [wPlayerXCoordPixels]; the sum is stored back
 * and left in a. hl is push/pop-preserved; b/c/d/e untouched. */
uint8_t Func_c6cc(uint8_t a)
{
	uint8_t sum = (uint8_t)(a + wPlayerXCoordPixels);
	wPlayerXCoordPixels = sum;
	return sum;
}
/* <<< factory Func_c6cc */

/* >>> factory Func_c6d4 */
/* overworld.asm:1035-1041. a += [wPlayerYCoordPixels]; the sum is stored back
 * and left in a. hl is push/pop-preserved; b/c/d/e untouched. */
uint8_t Func_c6d4(uint8_t a)
{
	uint8_t sum = (uint8_t)(a + wPlayerYCoordPixels);
	wPlayerYCoordPixels = sum;
	return sum;
}
/* <<< factory Func_c6d4 */

/* >>> factory Func_c6f7 */
/* overworld.asm:1057-1067. Selects the player's sprite (wWhichSprite =
 * wPlayerSpriteIndex), clears its CENTERED animation flag and forces its
 * animation counter to $ff. Exits with a = $ff and the hl returned by the
 * (last) GetSpriteAnimBufferProperty call; c is call-setup residue ($0e),
 * f is residue of the callee, b/d/e preserved. */
uint8_t Func_c6f7(uint16_t *hl)
{
	wWhichSprite = wPlayerSpriteIndex;
	*hl = GetSpriteAnimBufferProperty(SPRITE_ANIM_FLAGS);
	gb_write8(*hl, (uint8_t)(gb_read8(*hl) & (uint8_t)~(1u << SPRITE_ANIM_FLAG_CENTERED_F)));
	*hl = GetSpriteAnimBufferProperty(SPRITE_ANIM_COUNTER);
	gb_write8(*hl, 0xffu);
	return 0xffu;
}
/* <<< factory Func_c6f7 */

/* >>> factory SetOverworldNPCFlags */
/* overworld.asm:355-361 */
OverworldNPCFlagsResult SetOverworldNPCFlags(uint8_t a)
{
	uint8_t value = (uint8_t)(a | wOverworldNPCFlags);

	wOverworldNPCFlags = value;
	return (OverworldNPCFlagsResult){
		.a = value,
		.f = value == 0u ? 0x80u : 0x00u,
	};
}
/* <<< factory SetOverworldNPCFlags */
