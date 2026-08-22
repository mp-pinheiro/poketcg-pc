#include "home/npc_core.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/load_animation.h"
#include "home/map.h"
#include "home/random.h"
#include "home/sprite_animations.h"
#include "mem.h"

/* engine/overworld/npc_core.asm constants */
#define NPC_RONALD1              0x02u
#define NPC_RONALD2              0x71u
#define NPC_RONALD3              0x72u
#define LOADED_NPC_SPRITE        0x01u
#define LOADED_NPC_DIRECTION     0x04u
#define LOADED_NPC_FLAGS         0x05u
#define LOADED_NPC_ANIM          0x06u
#define NPC_FLAG_DIRECTIONLESS_F 0x04u
#define SPRITE_ANIM_COUNTER      0x0eu

/* flag byte bits: Z=0x80, N=0x40, H=0x20, C=0x10 */
#define F_Z                      0x80u
#define F_C                      0x10u

#include "home/map.h"
#include "home/npc_core.h"

#define LOADED_NPC_DIRECTION_BACKUP 0x07u

#include "home/map.h"

/* engine/overworld/npc_core.asm constants */
#define DIRECTION_MASK           0x7fu /* $ff ^ NO_MOVE ($80) */
#define LOADED_NPC_MOVEMENT_STEP 0x08u
#define NPC_FLAG_MOVING_F        0x05u
#define MOVEMENT_CMD_SPECIAL     0xf0u
#define MOVEMENT_CMD_STOP        0xffu

static const uint8_t player_movement_offset_table_tiles[] = {
	0x00u, 0xffu,
	0x01u, 0x00u,
	0x00u, 0x01u,
	0xffu, 0x00u,
};

#define LOADED_NPC_COORD_X 0x02u
#define LOADED_NPC_COORD_Y 0x03u

#define NPC_FLAG_MOVING (1u << NPC_FLAG_MOVING_F)
#define SPRITE_ANIM_COORD_X 0x02u

#include "generated/wram.h"
#include "home/map.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/map.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/map.h"
#include "home/npc_core.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/map.h"

#include "generated/wram.h"
#include "mem.h"

#include "generated/wram.h"

#define LOADED_NPC_LENGTH 0x0Cu
#define LOADED_NPC_MAX 0x08u

#include "home/npc_core.h"
#include "generated/wram.h"

#include "generated/wram.h"
#include "home/map.h"
#include "home/npc_core.h"

#include "generated/wram.h"
#include "home/map.h"
#include "home/npc_core.h"
#include "home/sprite_animations.h"
#include "mem.h"

#define TRUE 0x01u

#include "generated/wram.h"
#include "home/map.h"
#include "home/npc_data.h"
#include "home/npc_core.h"
#include "home/overworld.h"
#include "mem.h"
#define RESTORE_FACING_DIRECTION 0x01u
/* <<< factory statics */

/* >>> factory CheckIfNPCIsRonald */
/* npc_core.asm:123-138. Compares the id in a against the three Ronald ids and
 * exits through `scf` on a match or `or a` otherwise, so the whole flag byte
 * is an output: Z|C ($90) for a Ronald, Z ($80) when a == 0, else $00. */
uint8_t CheckIfNPCIsRonald(uint8_t a)
{
	if (a == NPC_RONALD1 || a == NPC_RONALD2 || a == NPC_RONALD3)
		return (uint8_t)(F_Z | F_C); /* cp sets Z, scf clears N/H and sets C */
	return (uint8_t)(a == 0 ? F_Z : 0x00u); /* or a: Z=(a==0), N/H/C clear */
}
/* <<< factory CheckIfNPCIsRonald */

/* >>> factory UpdateNPCAnimation */
/* npc_core.asm:229-261. Temporarily aims wWhichSprite at the temp NPC's sprite
 * and starts its animation, offset by the facing direction unless the NPC is
 * flagged directionless. a (echo of wWhichSprite), f, bc, hl and wWhichSprite
 * itself are all restored before ret; only the sprite animation state written
 * by StartNewSpriteAnimation survives. */
uint8_t UpdateNPCAnimation(void)
{
	uint8_t saved_which = wWhichSprite;
	uint16_t npc = GetLoadedNPCID(wLoadedNPCTempIndex).hl;
	if (gb_read8(npc) != 0) {
		wWhichSprite = gb_read8((uint16_t)(npc + LOADED_NPC_SPRITE));
		uint8_t anim = gb_read8((uint16_t)(npc + LOADED_NPC_ANIM));
		if ((gb_read8((uint16_t)(npc + LOADED_NPC_FLAGS)) & (1u << NPC_FLAG_DIRECTIONLESS_F)) == 0)
			anim = (uint8_t)(anim + gb_read8((uint16_t)(npc + LOADED_NPC_DIRECTION)));
		StartNewSpriteAnimation(anim);
	}
	wWhichSprite = saved_which;
	return saved_which;
}
/* <<< factory UpdateNPCAnimation */

/* >>> factory ApplyRandomCountToNPCAnim */
/* npc_core.asm:262-309. Subtracts a random 0..counter-1 amount from the temp
 * NPC's sprite animation counter (skipped when the counter is 0 or $ff) so
 * same-animation NPCs start out of phase. a (echo of wWhichSprite), f, bc, hl
 * and wWhichSprite itself are all restored before ret. */
uint8_t ApplyRandomCountToNPCAnim(void)
{
	uint8_t saved_sprite = wWhichSprite;
	uint16_t npc = GetLoadedNPCID(wLoadedNPCTempIndex).hl;
	if (gb_read8(npc) != 0) {
		wWhichSprite = gb_read8((uint16_t)(npc + LOADED_NPC_SPRITE));
		uint16_t counter = GetSpriteAnimBufferProperty(SPRITE_ANIM_COUNTER);
		uint8_t count = gb_read8(counter);
		if (count != 0u && count != 0xFFu) {
			uint8_t r = Random((uint8_t)(count - 1u));
			gb_write8(counter, (uint8_t)(count - r));
		}
	}
	wWhichSprite = saved_sprite;
	return saved_sprite;
}
/* <<< factory ApplyRandomCountToNPCAnim */

/* >>> factory SetNPCAnimation */
/* npc_core.asm:215-227 */
uint8_t SetNPCAnimation(uint8_t a)
{
	PermissionResult r = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_ANIM);
	gb_write8(r.hl, a);
	return UpdateNPCAnimation();
}
/* <<< factory SetNPCAnimation */

/* >>> factory SetNPCDirection */
/* npc_core.asm:312-323 */
uint8_t SetNPCDirection(uint8_t a)
{
	PermissionResult r = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_DIRECTION);
	gb_write8(r.hl, a);
	return UpdateNPCAnimation();
}
/* <<< factory SetNPCDirection */

/* >>> factory StartNPCMovement */
/* npc_core.asm:618-698 */
uint8_t StartNPCMovement(uint16_t *bc)
{
	uint16_t ptr = *bc;

	/* set NPC as moving */
	PermissionResult r = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_FLAGS);
	gb_write8(r.hl, (uint8_t)(gb_read8(r.hl) | (1u << NPC_FLAG_MOVING_F)));

	/* reset its movement step; the asm's `ld [hli], a` then leaves hl on LOADED_NPC_MOVEMENT_PTR */
	r = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_MOVEMENT_STEP);
	gb_write8(r.hl, 0x00u);
	uint16_t field = (uint16_t)(r.hl + 1u);

	for (;;) {
		gb_write8(field, (uint8_t)ptr);
		gb_write8((uint16_t)(field + 1u), (uint8_t)(ptr >> 8));
		uint8_t cmd = GetNextNPCMovementByte(ptr);
		if (cmd >= MOVEMENT_CMD_SPECIAL) {
			if (cmd == MOVEMENT_CMD_STOP) {
				/* .stop_movement: clear the moving flag */
				PermissionResult s = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_FLAGS);
				gb_write8(s.hl, (uint8_t)(gb_read8(s.hl) & (uint8_t)~(1u << NPC_FLAG_MOVING_F)));
				*bc = ptr;
				return s.a;
			}
			/* jump to a movement command: bc += 1 + sign-extended argument */
			uint16_t argaddr = (uint16_t)(ptr + 1u);
			uint8_t arg = GetNextNPCMovementByte(argaddr);
			uint16_t offset = arg;
			if (arg & 0x80u)
				offset |= 0xff00u;
			ptr = (uint16_t)(argaddr + offset);
		} else {
			SetNPCDirection((uint8_t)(cmd & DIRECTION_MASK));
			/* if it was not a rotation, exit... otherwise jump to the next movement instruction */
			if (!(cmd & 0x80u)) {
				*bc = ptr;
				return cmd;
			}
			ptr = (uint16_t)(ptr + 1u);
		}
	}
}
/* <<< factory StartNPCMovement */

/* >>> factory Func_1c5e9 */
/* npc_core.asm:296-317 */
uint8_t Func_1c5e9(void)
{
	PermissionResult r = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex,
		LOADED_NPC_DIRECTION_BACKUP);
	uint8_t direction = gb_read8(r.hl);
	uint16_t hl = (uint16_t)(r.hl + (uint16_t)(LOADED_NPC_DIRECTION - LOADED_NPC_DIRECTION_BACKUP));
	gb_write8(hl, direction);
	return UpdateNPCAnimation();
}
/* <<< factory Func_1c5e9 */

/* >>> factory UpdateNPCPosition */
/* npc_core.asm:719-751 */
uint8_t UpdateNPCPosition(void)
{
	PermissionResult item = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex,
		LOADED_NPC_DIRECTION);
	uint16_t hl = item.hl;
	uint8_t direction = gb_read8(hl);
	hl = (uint16_t)(hl - 1u);

	uint8_t offset_index = (uint8_t)(direction << 1);
	uint8_t y_offset = player_movement_offset_table_tiles[(uint8_t)(offset_index + 1u)];
	uint8_t x_offset = player_movement_offset_table_tiles[offset_index];

	uint8_t y = (uint8_t)(gb_read8(hl) + y_offset);
	gb_write8(hl, y);
	hl = (uint16_t)(hl - 1u);

	uint8_t x = (uint8_t)(gb_read8(hl) + x_offset);
	gb_write8(hl, x);
	return x;
}
/* <<< factory UpdateNPCPosition */

/* >>> factory UpdateNPCSpritePosition */
UpdateNPCSpritePositionResult UpdateNPCSpritePosition(uint16_t hl)
{
	uint16_t npc = hl;
	uint8_t flags = gb_read8((uint16_t)(npc + LOADED_NPC_FLAGS));
	uint8_t direction = 0u;
	uint8_t step = 0u;
	if ((flags & NPC_FLAG_MOVING) != 0u) {
		direction = gb_read8((uint16_t)(npc + LOADED_NPC_DIRECTION));
		step = gb_read8((uint16_t)(npc + LOADED_NPC_MOVEMENT_STEP));
	}
	uint8_t b;
	uint8_t c;
	if (direction == 0u) {
		c = gb_read8(hSCY_ADDR);
		b = gb_read8(hSCX_ADDR);
	} else if (direction == 1u) {
		b = (uint8_t)(gb_read8(hSCX_ADDR) - step);
		c = gb_read8(hSCY_ADDR);
	} else if (direction == 2u) {
		c = (uint8_t)(gb_read8(hSCY_ADDR) - step);
		b = gb_read8(hSCX_ADDR);
	} else {
		step = (uint8_t)(0u - step);
		b = (uint8_t)(gb_read8(hSCX_ADDR) - step);
		c = gb_read8(hSCY_ADDR);
	}
	uint16_t sprite = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
	uint8_t x = (uint8_t)(gb_read8((uint16_t)(npc + LOADED_NPC_COORD_X)) * 8u + 0x08u);
	x = (uint8_t)(x - b);
	gb_write8(sprite, x);
	uint8_t y_base = gb_read8((uint16_t)(npc + LOADED_NPC_COORD_X + 1u));
	uint8_t y = (uint8_t)(y_base * 8u + 0x10u);
	uint8_t y_result = (uint8_t)(y - c);
	gb_write8((uint16_t)(sprite + 1u), y_result);
	UpdateNPCSpritePositionResult result;
	result.a = y_result;
	result.f = 0x40u;
	if (y_result == 0u)
		result.f |= 0x80u;
	if ((y & 0x0fu) < (c & 0x0fu))
		result.f |= 0x20u;
	if (y < c)
		result.f |= 0x10u;
	return result;
}
/* <<< factory UpdateNPCSpritePosition */

/* >>> factory CheckIsAnNPCMoving */
CheckIsAnNPCMovingResult CheckIsAnNPCMoving(void)
{
	uint8_t a = (uint8_t)(wIsAnNPCMoving & NPC_FLAG_MOVING);
	uint8_t f = (uint8_t)(0x20u | (a == 0u ? 0x80u : 0u));
	return (CheckIsAnNPCMovingResult){a, f};
}
/* <<< factory CheckIsAnNPCMoving */

/* >>> factory UpdateNPCsTilePermission */
uint8_t UpdateNPCsTilePermission(void)
{
	uint8_t index = wLoadedNPCTempIndex;
	PermissionResult entry = GetItemInLoadedNPCIndex(index, LOADED_NPC_COORD_X);
	uint8_t x = gb_read8(entry.hl);
	uint8_t y = gb_read8((uint16_t)(entry.hl + 1u));
	uint8_t result = UpdatePermissionOfMapPosition(0x40u, x, y);
	return result;
}
/* <<< factory UpdateNPCsTilePermission */

/* >>> factory SetNPCsTilePermission */
uint8_t SetNPCsTilePermission(void)
{
	PermissionResult entry = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_COORD_X);
	uint8_t x = gb_read8(entry.hl);
	uint8_t y = gb_read8((uint16_t)(entry.hl + 1u));
	SetPermissionOfMapPosition(0x40u, x, y);
	return 0x40u;
}
/* <<< factory SetNPCsTilePermission */

/* >>> factory SetNPCPosition */
uint8_t SetNPCPosition(uint8_t b, uint8_t c)
{
	(void)UpdateNPCsTilePermission();
	PermissionResult entry = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_COORD_X);
	gb_write8(entry.hl, b);
	gb_write8((uint16_t)(entry.hl + 1u), c);
	return SetNPCsTilePermission();
}
/* <<< factory SetNPCPosition */

/* >>> factory Func_1c53f */
uint8_t Func_1c53f(void)
{
	PermissionResult r = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex,
		LOADED_NPC_DIRECTION);
	uint8_t value = gb_read8(r.hl);
	uint16_t backup = (uint16_t)(r.hl + (LOADED_NPC_DIRECTION_BACKUP - LOADED_NPC_DIRECTION));
	gb_write8(backup, value);
	(void)Func_1c5e9();
	return value;
}
/* <<< factory Func_1c53f */

/* >>> factory GetNPCDirection */
uint8_t GetNPCDirection(void)
{
	PermissionResult r = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_DIRECTION);
	return gb_read8(r.hl);
}
/* <<< factory GetNPCDirection */

/* >>> factory GetNPCPosition */
NPCPositionResult GetNPCPosition(void)
{
	PermissionResult r = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_COORD_X);
	uint8_t x = gb_read8(r.hl);
	uint8_t y = gb_read8((uint16_t)(r.hl + 1u));
	return (NPCPositionResult){x, x, y};
}
/* <<< factory GetNPCPosition */

/* >>> factory UpdateIsAnNPCMovingFlag */
UpdateIsAnNPCMovingFlagResult UpdateIsAnNPCMovingFlag(uint16_t hl)
{
	uint8_t a = (uint8_t)(wIsAnNPCMoving | gb_read8((uint16_t)(hl + LOADED_NPC_FLAGS)));
	wIsAnNPCMoving = a;
	return (UpdateIsAnNPCMovingFlagResult){a, (a == 0u) ? 0x80u : 0x00u};
}
/* <<< factory UpdateIsAnNPCMovingFlag */

/* >>> factory ClearNPCs */
uint8_t ClearNPCs(void)
{
	for (uint8_t i = 0; i < (LOADED_NPC_MAX * LOADED_NPC_LENGTH); ++i)
		wLoadedNPCs_PTR[i] = 0x00u;
	wNumLoadedNPCs = 0x00u;
	wRonaldIsInMap = 0x00u;
	return 0x00u;
}
/* <<< factory ClearNPCs */

/* >>> factory SetAllNPCTilePermissions */
SetAllNPCTilePermissionsResult SetAllNPCTilePermissions(void)
{
	uint8_t a = 0u;
	for (uint8_t i = 0u; i < LOADED_NPC_MAX; ++i) {
		if (wLoadedNPCs_PTR[(uint16_t)i * LOADED_NPC_LENGTH] != 0u) {
			wLoadedNPCTempIndex = i;
			a = SetNPCsTilePermission();
		} else {
			a = 0u;
		}
	}
	return (SetAllNPCTilePermissionsResult){a, 0xC0u};
}
/* <<< factory SetAllNPCTilePermissions */

/* >>> factory Func_1c557 */
uint8_t Func_1c557(uint8_t a)
{
	uint8_t old_index = wLoadedNPCTempIndex;
	uint8_t old_npc = wTempNPC;
	wTempNPC = a;
	NPCSearchResult found = FindLoadedNPC();
	uint8_t result = 0;
	if ((found.f & 0x10u) == 0u)
		result = Func_1c53f();
	wTempNPC = old_npc;
	wLoadedNPCTempIndex = old_index;
	return result;
}
/* <<< factory Func_1c557 */

/* >>> factory LoadNPC */
uint8_t LoadNPC(void)
{
	wLoadedNPCTempIndex = 0;
	uint8_t index = 0;
	uint8_t remaining = LOADED_NPC_MAX;
	uint16_t entry = wLoadedNPCs_ADDR;
	while (remaining != 0u) {
		uint8_t id = gb_read8(entry);
		if (id == 0u)
			break;
		entry = (uint16_t)(entry + LOADED_NPC_LENGTH);
		index++;
		remaining--;
	}
	if (remaining == 0u)
		return gb_read8((uint16_t)(wLoadedNPCs_ADDR + (uint16_t)(LOADED_NPC_MAX - 1u) * LOADED_NPC_LENGTH));

	wLoadedNPCTempIndex = index;
	uint8_t create_result = CreateSpriteAndAnimBufferEntry(wNPCSpriteID, 0u);
	if ((create_result & 0x10u) != 0u)
		return create_result;

	PermissionResult result = GetLoadedNPCID(wLoadedNPCTempIndex);
	uint16_t npc = result.hl;
	gb_write8(npc, wTempNPC);
	npc++;
	gb_write8(npc, wWhichSprite);
	npc++;
	gb_write8(npc, wLoadNPCXPos);
	npc++;
	gb_write8(npc, wLoadNPCYPos);
	npc++;
	gb_write8(npc, wLoadNPCDirection);
	npc++;
	gb_write8(npc, wNPCAnimFlags);
	npc++;
	gb_write8(npc, wNPCAnim);
	npc++;
	gb_write8(npc, wLoadNPCDirection);

	(void)UpdateNPCAnimation();
	(void)ApplyRandomCountToNPCAnim();
	wNumLoadedNPCs++;
	(void)UpdateNPCSpritePosition(result.hl);
	(void)SetNPCsTilePermission();

	uint8_t npc_id = wTempNPC;
	if ((CheckIfNPCIsRonald(npc_id) & 0x10u) != 0u) {
		wRonaldIsInMap = TRUE;
	}
	return npc_id;
}
/* <<< factory LoadNPC */

/* >>> factory SetNewScriptNPC */
SetNewScriptNPCResult SetNewScriptNPC(uint16_t hl)
{
	uint16_t saved_hl = hl;
	PermissionResult direction = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex, LOADED_NPC_DIRECTION);
	gb_write8(direction.hl, (uint8_t)(wPlayerDirection ^ 0x02u));
	(void)UpdateNPCAnimation();
	(void)SetOverworldNPCFlags(0x01u << RESTORE_FACING_DIRECTION);
	PermissionResult npc = GetLoadedNPCID(wLoadedNPCTempIndex);
	GetNPCNameAndScriptResult result = GetNPCNameAndScript(gb_read8(npc.hl));
	return (SetNewScriptNPCResult){result.a, result.f, result.b, result.c, saved_hl};
}
/* <<< factory SetNewScriptNPC */

/* >>> factory UnloadNPC */
uint8_t UnloadNPC(void)
{
	UpdateNPCsTilePermission();
	PermissionResult npc = GetLoadedNPCID(wLoadedNPCTempIndex);
	uint8_t id = gb_read8(npc.hl);
	if (id == 0u)
		return 0u;
	uint8_t ronald = CheckIfNPCIsRonald(id);
	if ((ronald & 0x10u) != 0u)
		wRonaldIsInMap = 0u;
	gb_write8(npc.hl, 0u);
	uint8_t sprite = gb_read8((uint16_t)(npc.hl + 1u));
	DisableSpriteAnim(sprite);
	wNumLoadedNPCs = (uint8_t)(wNumLoadedNPCs - 1u);
	return (uint8_t)(sprite << 4);
}
/* <<< factory UnloadNPC */

/* >>> factory Func_1c52e */
uint8_t Func_1c52e(uint8_t a)
{
	PermissionResult r = GetItemInLoadedNPCIndex(wLoadedNPCTempIndex,
		LOADED_NPC_DIRECTION_BACKUP);
	gb_write8(r.hl, a);
	return Func_1c5e9();
}
/* <<< factory Func_1c52e */
