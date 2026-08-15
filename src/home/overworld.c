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

#include "generated/wram.h"
#include "home/map.h"
#include "home/npc_core.h"
#include "home/play_animation.h"
#include "mem.h"

/* The engine/overworld bank is labeled in pret's bank-linear space: names like
 * Func_c158 address the bank-3 slot $c000-$ffff, i.e. runtime address
 * (name - $8000). SetOverworldDoFrameFunction occupies $c199 (7 bytes:
 * ld hl,nn / call nn / ret), and OverworldDoFrameFunction is the next label,
 * so the pointer handed to SetDoFrameFunction is runtime $41a0. */
#define OVERWORLD_DO_FRAME_FUNCTION 0x41a0u

#define GAME_EVENT_DUEL      0x01u
#define LOADED_NPC_DIRECTION 0x04u
#define OVERWORLD_MAP        0x00u
#define OWMODE_MAP           0x00u
#define OWMODE_MOVE          0x01u
#define FLAG_CARRY           0x10u
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

/* >>> factory Func_c158 */
/* overworld.asm:174-197 */
uint8_t Func_c158(void)
{
	uint8_t event = wActiveGameEvent;
	if (event != GAME_EVENT_DUEL)
		return event;
	wTempNPC = wNPCDuelist;
	NPCSearchResult npc = FindLoadedNPC();
	if (npc.f & FLAG_CARRY)
		return npc.a;
	PermissionResult slot = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_DIRECTION);
	gb_write8(slot.hl, wNPCDuelistDirection);
	return UpdateNPCAnimation();
}
/* <<< factory Func_c158 */

/* >>> factory Func_c184 */
/* overworld.asm:198-211 */
void Func_c184(void)
{
	uint8_t mode = OWMODE_MOVE;
	if (wCurMap == OVERWORLD_MAP)
		mode = OWMODE_MAP;
	wOverworldMode = mode;
	wOverworldModeBackup = mode;
}
/* <<< factory Func_c184 */
