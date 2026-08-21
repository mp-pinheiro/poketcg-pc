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

#include "generated/sram.h"
#include "generated/wram.h"
#include "home/mail.h"
#include "home/switch_sram.h"

#include "generated/wram.h"

#include "generated/wram.h"
#include "home/map.h"
#include "mem.h"
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

/* >>> factory WhiteOutDMGPals */
/* overworld.asm:221-233 */
void WhiteOutDMGPals(void)
{
	SetBGP(0u);
	SetOBP0(0u);
	SetOBP1(0u);
}
/* <<< factory WhiteOutDMGPals */

/* >>> factory Func_c1f8 */
/* overworld.asm:260-307. */
void Func_c1f8(void)
{
	wSelectedPauseMenuItem = 0u;
	wSelectedPCMenuItem = 0u;
	wSelectedGiftCenterMenuItem = 0u;
	wConfigCursorYPos = 0u;
	wActiveGameEvent = 0u;
	wDefaultSong = 0u;
	wSongOverride = 0u;
	wRonaldIsInMap = 0u;
	EnableSRAM();
	wAnimationsDisabled = gb_read8(sAnimationsDisabled_ADDR);
	wTextSpeed = gb_read8(sTextSpeed_ADDR);
	DisableSRAM();
	InitPCPacks();
}
/* <<< factory Func_c1f8 */

/* >>> factory BackupPlayerPosition */
/* overworld.asm:279-291 */
void BackupPlayerPosition(void)
{
	wTempMap = wCurMap;
	wTempPlayerXCoord = wPlayerXCoord;
	wTempPlayerYCoord = wPlayerYCoord;
	wTempPlayerDirection = wPlayerDirection;
}
/* <<< factory BackupPlayerPosition */



/* >>> factory Func_c469 */
/* overworld.asm:651-677 */
void Func_c469(void)
{
	uint8_t scx = (uint8_t)(wSCXBuffer + 4u);
	scx &= 0xf8u;
	scx = (uint8_t)((scx >> 1) | (scx << 7));
	scx = (uint8_t)((scx >> 1) | (scx << 7));
	scx = (uint8_t)((scx >> 1) | (scx << 7));
	wd233 = scx;

	uint8_t scy = (uint8_t)(wSCYBuffer + 4u);
	scy &= 0xf8u;
	scy = (uint8_t)((scy >> 1) | (scy << 7));
	scy = (uint8_t)((scy >> 1) | (scy << 7));
	scy = (uint8_t)((scy >> 1) | (scy << 7));
	wd234 = scy;
}
/* <<< factory Func_c469 */



/* >>> factory SetScreenScrollWram */
/* overworld.asm:668-680 */
uint8_t SetScreenScrollWram(void)
{
	wSCX = wSCXBuffer;
	wSCY = wSCYBuffer;
	return wSCYBuffer;
}
/* <<< factory SetScreenScrollWram */



/* >>> factory SetScreenScroll */
/* overworld.asm:675-680 */
void SetScreenScroll(void)
{
	hSCX = wSCX;
	hSCY = wSCY;
}
/* <<< factory SetScreenScroll */

/* >>> factory Func_c70d */
/* overworld.asm:1069-1085 */
FuncC70dResult Func_c70d(void)
{
	uint8_t current = wCurMap;
	uint8_t temporary = wTempMap;
	uint8_t flags = 0x40u;

	if (current == temporary)
		flags |= 0x80u;
	if ((current & 0x0Fu) < (temporary & 0x0Fu))
		flags |= 0x20u;
	if (current < temporary)
		flags |= 0x10u;

	if (current != temporary)
		wOverworldTransition |= 0x10u;

	return (FuncC70dResult){current, flags};
}
/* <<< factory Func_c70d */

/* >>> factory Func_c430 */
void Func_c430(void)
{
	uint8_t x = (uint8_t)(wd237 << 3);
	uint8_t scx = wSCXBuffer;
	if (scx >= 0xB1u)
		scx = 0;
	else if (scx >= x)
		scx = x;
	wSCXBuffer = scx;

	uint8_t y = (uint8_t)(wd238 << 3);
	uint8_t scy = wSCYBuffer;
	if (scy >= 0xB9u)
		scy = 0;
	else if (scy >= y)
		scy = y;
	wSCYBuffer = scy;
}
/* <<< factory Func_c430 */

/* >>> factory Func_c41c */
void Func_c41c(void)
{
	wSCXBuffer = (uint8_t)(wPlayerXCoordPixels - 0x40u);
	wSCYBuffer = (uint8_t)(wPlayerYCoordPixels - 0x40u);
	Func_c430();
}
/* <<< factory Func_c41c */

/* >>> factory Func_c3ca */
FuncC3caResult Func_c3ca(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	PermissionResult permission = GetPermissionByteOfMapPosition(d, e);
	uint8_t columns = (uint8_t)(b >> 1);
	uint8_t rows = (uint8_t)(c >> 1);
	uint16_t row_count = rows == 0u ? 256u : rows;
	uint16_t column_count = columns == 0u ? 256u : columns;
	uint16_t row_start = permission.hl;
	uint8_t a = 0u;

	for (uint16_t row = 0u; row < row_count; row++) {
		uint16_t position = row_start;
		for (uint16_t column = 0u; column < column_count; column++) {
			a = (uint8_t)(gb_read8(position) | 0x10u);
			gb_write8(position++, a);
		}
		row_start = (uint16_t)(row_start + 0x10u);
	}

	uint8_t f = 0x40u;
	if (rows == 0u)
		f |= 0x20u;
	else
		f |= 0x80u;
	return (FuncC3caResult){a, f};
}
/* <<< factory Func_c3ca */
