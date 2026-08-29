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

#include "generated/wram.h"
#include "home/overworld.h"

#include "generated/wram.h"
#include "home/copy.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/load_animation.h"
#include "home/map.h"
#include "mem.h"

#include "home/overworld.h"
#include "generated/wram.h"

#include "home/play_animation.h"

#include "home/give_booster_pack.h"
#include "generated/wram.h"

#include "generated/wram.h"
#include "mem.h"

#define POKEMON_DOME_ENTRANCE 0x1fu

#include "home/text_box.h"
#include "home/overworld.h"

#include "generated/wram.h"
#include "home/copy.h"
#include "home/palettes.h"

#include "generated/wram.h"
#include "home/overworld.h"
#define SCREEN_WIDTH 0x14u
#define SCREEN_HEIGHT 0x12u

#include "generated/wram.h"
#include "home/map.h"
#include "home/load_animation.h"

#define SPRITE_ANIM_FLAG_UNSKIPPABLE 0x80u

#include "generated/wram.h"
#include "home/sprite_animations.h"

#include "home/overworld.h"
#include "generated/wram.h"
#include "generated/hram.h"
#define B_PAD_B_MASK 0x02u

#include "home/load_gfx.h"
#include "home/sprite_animations.h"
#include "home/overworld_map.h"

#define CONSOLE_CGB 0x02u
#define SOUTH 0x02u
#define SPRITE_OW_PLAYER 0x00u
#define SPRITE_ANIM_LIGHT_NPC_UP 0x00u
#define SPRITE_ANIM_RED_NPC_UP 0x1Eu
#define PALETTE_OVERWORLD_OAM 0x1Du

#include "home/scripting.h"
#include "home/save.h"
#include "generated/hram.h"

#include "home/scripting.h"
#include "home/map_events.h"
#include "home/masters_beaten_list.h"
#include "home/challenge_machine.h"
#include "generated/wram.h"
#include "generated/hram.h"
#define OWMAP_POKEMON_DOME 0x0Cu

#include "home/overworld.h"
#include "home/load_animation.h"
#include "home/overworld_map.h"
#include "generated/wram.h"
#define SPRITE_ANIM_COORD_X 0x02u

#include "home/overworld.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/load_animation.h"
#include "home/default_palettes.h"
#include "home/objects.h"
#include "generated/wram.h"

#include "generated/wram.h"
#include "home/overworld_map.h"

#include "generated/wram.h"
#include "home/labels.h"
#define PAUSE_MENU_PARAMS 0x4D98u

#include "generated/wram.h"
#include "home/lcd_enable_frame.h"
#include "home/menus.h"
#include "mem.h"

#include "home/diary.h"
#include "generated/wram.h"

#include "home/labels.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#define PC_MENU_PARAMS 0x4DA9u
#define PC_MENU_BANK 0x04u

#define PAUSE_MENU_TEXT_LIST_BANK 0x03u
#define PAUSE_MENU_TEXT_LIST_ADDR 0x427Cu

#include "home/status.h"

#include "home/process_text.h"
#define POINTER_TABLE_C152 0x4152u
#define POINTER_TABLE_C152_BANK 3u

#include "home/load_overworld.h"
#include "generated/wram.h"
#define AUTO_CLOSE_TEXTBOX 0x00u

#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#include "home/lcd.h"
#include "home/credits_sequence_commands.h"
#include "home/load_animation.h"
#include "home/color.h"
#include "home/sprite_animations.h"
#include "home/overworld.h"
#include "home/load_overworld.h"
#include "home/npc_core.h"
#define HIDE_ALL_NPC_SPRITES 0x07u
#define PLAYER_TURN 0xC2u

#define RESTORE_FACING_DIRECTION 0x01u

#include "generated/wram.h"
#include "home/map.h"
#include "home/npc_core.h"
#include "home/script.h"
#define OWMODE_SCRIPT 0x03u
#define OWMODE_START_SCRIPT 0x02u

#include "generated/wram.h"
#include "home/overworld.h"
#include "home/scripting.h"
#include "home/map.h"

#include "home/overworld.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define PAD_CTRL_PAD 0xF0u
#define PAD_A 0x01u

#include "home/pc_glossary.h"

#include "generated/wram.h"
#include "home/scripting.h"

#include "generated/hram.h"
#include "home/card_album.h"
#include "home/credits_sequence_commands.h"
#include "home/lcd.h"

#include "home/config.h"

/* overworld.asm:1264 (PCMenu_ReadMail). The farcall target _PCMenu_ReadMail
 * is already ported and lives in home/mail.h; nothing else is needed here. */
#include "home/mail.h"

#include "home/overworld.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/load_animation.h"
#include "home/color.h"
#include "home/sprite_animations.h"
#include "home/process_text.h"
#include "home/objects.h"
#include "generated/wram.h"

#include "home/deck_configuration.h"
#include "home/credits_sequence_commands.h"
#include "home/lcd.h"
#include "generated/hram.h"
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

/* >>> factory GetDirectionFromDPad */
GetDirectionFromDPadResult GetDirectionFromDPad(uint8_t a)
{
	GetDirectionFromDPadResult result;
	if (a == 0u) {
		result.a = 0x02u;
		result.f = 0x80u;
	} else if (a & 0x80u) {
		result.a = 0x02u;
		result.f = 0x10u;
	} else if (a & 0x40u) {
		result.a = 0x00u;
		result.f = 0x10u;
	} else if (a & 0x20u) {
		result.a = 0x03u;
		result.f = 0x10u;
	} else {
		result.a = 0x01u;
		result.f = 0x10u;
	}
	return result;
}
/* <<< factory GetDirectionFromDPad */

/* >>> factory Func_c694 */
void Func_c694(uint8_t a, uint8_t c)
{
	static const int8_t movement_offsets[8] = {0, -1, 1, 0, 0, 1, -1, 0};
	uint8_t offset = (uint8_t)(a << 1);
	for (;;) {
		uint8_t dx = (uint8_t)movement_offsets[offset];
		uint8_t dy = (uint8_t)movement_offsets[(uint8_t)(offset + 1u)];
		if (dx != 0u)
			Func_c6cc(dx);
		if (dy != 0u)
			Func_c6d4(dy);
		wd338--;
		if (wd338 == 0u)
			break;
		c--;
		if (c == 0u)
			break;
	}
	if (wd338 == 0u)
		wPlayerCurrentlyMoving |= 0x02u;
	Func_c41c();
	Func_c469();
}
/* <<< factory Func_c694 */

/* >>> factory FindPlayerMovementWithOffset */
FindPlayerMovementWithOffsetResult FindPlayerMovementWithOffset(uint8_t a)
{
	static const uint8_t offsets[8] = {0u, 0xFEu, 2u, 0u, 0u, 2u, 0xFEu, 0u};
	uint8_t index = (uint8_t)(a << 1);
	uint8_t x_offset = offsets[index];
	uint8_t y_offset = offsets[(uint8_t)(index + 1u)];
	uint8_t x = (uint8_t)(wPlayerXCoord + x_offset);
	uint8_t y0 = wPlayerYCoord;
	uint8_t y = (uint8_t)(y0 + y_offset);
	uint8_t f = (uint8_t)((y == 0u ? 0x80u : 0u)
		| (((y0 & 0x0Fu) + (y_offset & 0x0Fu) > 0x0Fu) ? 0x20u : 0u)
		| (((uint16_t)y0 + (uint16_t)y_offset > 0xFFu) ? 0x10u : 0u));
	FindPlayerMovementWithOffsetResult result = {y, f, x, y};
	return result;
}
/* <<< factory FindPlayerMovementWithOffset */

/* >>> factory BackupObjectPalettes */
void BackupObjectPalettes(void)
{
	gb_write8(wOBP0Backup_ADDR, gb_read8(wOBP0_ADDR));
	gb_write8(wOBP1Backup_ADDR, gb_read8(wOBP1_ADDR));
	CopyDataHLtoDE_SaveRegisters(wObjectPalettesCGB_ADDR, wObjectPalettesCGBBackup_ADDR, 64u);
}
/* <<< factory BackupObjectPalettes */

/* >>> factory AttemptPlayerMovement */
void AttemptPlayerMovement(uint8_t b, uint8_t c)
{
	if (b >= 0x1fu || c >= 0x1fu)
		return;
	uint8_t permission = GetPermissionOfMapPosition(b, c);
	if ((permission & (0x40u | 0x80u)) != 0u)
		return;
	wPlayerXCoord = b;
	wPlayerYCoord = c;
	wPlayerCurrentlyMoving = (uint8_t)(wPlayerCurrentlyMoving | 1u);
	wd338 = 0x10u;
	uint16_t hl = GetSpriteAnimBufferProperty(SPRITE_ANIM_FLAGS);
	gb_write8(hl, (uint8_t)(gb_read8(hl) | (1u << SPRITE_ANIM_FLAG_CENTERED_F)));
	hl = GetSpriteAnimBufferProperty(SPRITE_ANIM_COUNTER);
	gb_write8(hl, 0x04u);
}
/* <<< factory AttemptPlayerMovement */

/* >>> factory FindPlayerMovementFromDirection */
FindPlayerMovementWithOffsetResult FindPlayerMovementFromDirection(void)
{
	return FindPlayerMovementWithOffset(wPlayerDirection);
}
/* <<< factory FindPlayerMovementFromDirection */

/* >>> factory Func_c1a0 */
FuncC1A0Result Func_c1a0(uint16_t hl)
{
	FrameFunctionResult result = ResetDoFrameFunction(hl);
	return (FuncC1A0Result){result.a, result.f, result.hl};
}
/* <<< factory Func_c1a0 */

/* >>> factory PauseMenu_Exit */
void PauseMenu_Exit(void)
{
	_PauseMenu_Exit();
}
/* <<< factory PauseMenu_Exit */

/* >>> factory AttemptPlayerMovementFromDirection */
void AttemptPlayerMovementFromDirection(void)
{
	FindPlayerMovementWithOffsetResult movement = FindPlayerMovementFromDirection();
	AttemptPlayerMovement(movement.b, movement.c);
}
/* <<< factory AttemptPlayerMovementFromDirection */

/* >>> factory Func_c687 */
void Func_c687(void)
{
	uint8_t c = wd33a;
	uint8_t a = wd339;
	Func_c694(a, c);
}
/* <<< factory Func_c687 */

/* >>> factory Func_c36a */
void Func_c36a(void)
{
	wOWMapEvents = 0u;
	if (wCurMap == POKEMON_DOME_ENTRANCE)
		gb_write8(0xD324u, 0u);
}
/* <<< factory Func_c36a */

/* >>> factory Func_c915 */
FuncC3caResult Func_c915(void)
{
	uint8_t d = 0x00;
	uint8_t e = 0x0C;
	uint8_t b = 0x14;
	uint8_t c = 0x06;
	AdjustCoordinatesForBGScroll(&d, &e);
	FuncC3caResult result = Func_c3ca(b, c, d, e);
	return result;
}
/* <<< factory Func_c915 */

/* >>> factory StartScriptedMovement */
void StartScriptedMovement(void)
{
	wWhichSprite = wPlayerSpriteIndex;
	FindPlayerMovementWithOffsetResult result = FindPlayerMovementWithOffset(wd339);
	AttemptPlayerMovement(result.b, result.c);
}
/* <<< factory StartScriptedMovement */

/* >>> factory RestoreObjectPalettes */
void RestoreObjectPalettes(void)
{
	wOBP0 = wOBP0Backup;
	wOBP1 = wOBP1Backup;
	CopyDataHLtoDE_SaveRegisters(0xD0CCu, 0xCB30u, 64u);
	FlushAllPalettes();
}
/* <<< factory RestoreObjectPalettes */

/* >>> factory Func_c3ff */
void Func_c3ff(void)
{
	wd237 = (uint8_t)(wBGMapWidth - SCREEN_WIDTH);
	wd238 = (uint8_t)(wBGMapHeight - SCREEN_HEIGHT);
	Func_c41c();
	Func_c469();
	(void)SetScreenScrollWram();
	SetScreenScroll();
}
/* <<< factory Func_c3ff */

/* >>> factory Func_c49c */
void Func_c49c(void)
{
	wPlayerXCoord = (uint8_t)(wPlayerXCoord & 0x1Fu);
	wPlayerXCoordPixels = (uint8_t)((wPlayerXCoord << 3) | (wPlayerXCoord >> 5));
	wPlayerYCoord = (uint8_t)(wPlayerYCoord & 0x1Fu);
	wPlayerYCoordPixels = (uint8_t)((wPlayerYCoord << 3) | (wPlayerYCoord >> 5));
}
/* <<< factory Func_c49c */

/* >>> factory Func_c58b */
void Func_c58b(void)
{
	uint8_t permission = GetPermissionOfMapPosition(wPlayerXCoord, wPlayerYCoord);
	uint16_t hl = GetSpriteAnimBufferProperty(SPRITE_ANIM_FLAGS);
	uint8_t flags = gb_read8(hl);
	if ((permission & 0x10u) != 0u)
		flags = (uint8_t)(flags | SPRITE_ANIM_FLAG_UNSKIPPABLE);
	else
		flags = (uint8_t)(flags & (uint8_t)~SPRITE_ANIM_FLAG_UNSKIPPABLE);
	gb_write8(hl, flags);
}
/* <<< factory Func_c58b */

/* >>> factory UpdatePlayerSprite */
void UpdatePlayerSprite(void)
{
	wWhichSprite = wPlayerSpriteIndex;
	uint8_t animation = (uint8_t)(wPlayerSpriteBaseAnimation + wPlayerDirection);
	StartNewSpriteAnimation(animation);
}
/* <<< factory UpdatePlayerSprite */

/* >>> factory UpdatePlayerDirection */
void UpdatePlayerDirection(uint8_t a)
{
	wPlayerDirection = a;
	UpdatePlayerSprite();
}
/* <<< factory UpdatePlayerDirection */

/* >>> factory UpdatePlayerDirectionFromDPad */
void UpdatePlayerDirectionFromDPad(uint8_t a)
{
	GetDirectionFromDPadResult result = GetDirectionFromDPad(a);
	UpdatePlayerDirection(result.a);
}
/* <<< factory UpdatePlayerDirectionFromDPad */

/* >>> factory SetOverworldDoFrameFunction */
void SetOverworldDoFrameFunction(void)
{
	(void)SetDoFrameFunction(0x380eu);
}
/* <<< factory SetOverworldDoFrameFunction */

/* >>> factory Func_c3ee */
void Func_c3ee(void)
{
	uint16_t hl = wPermissionMap_ADDR;
	for (uint16_t i = 0; i < 256u; i++) {
		gb_write8(hl, (uint8_t)(gb_read8(hl) & (uint8_t)~0x10u));
		hl++;
	}
}
/* <<< factory Func_c3ee */

/* >>> factory Func_c66c */
void Func_c66c(void)
{
	uint8_t c = 1u;
	uint8_t keys = hKeysHeld;
	if (keys & B_PAD_B_MASK) {
		uint8_t wd338_val = wd338;
		if (wd338_val >= 2u)
			c = 2u;
	}
	Func_c694(wPlayerDirection, c);
}
/* <<< factory Func_c66c */

/* >>> factory Func_c4b9 */
void Func_c4b9(void)
{
	wWhichOBP = 0u;
	wWhichOBPalIndex = 0u;
	LoadOBPalette(PALETTE_OVERWORLD_OAM);

	uint8_t console = wConsole;
	uint8_t base_anim = SPRITE_ANIM_LIGHT_NPC_UP;
	uint8_t f_cgb = 0x40u;
	if ((console & 0x0Fu) < (CONSOLE_CGB & 0x0Fu))
		f_cgb |= 0x20u;
	if (console < CONSOLE_CGB)
		f_cgb |= 0x10u;
	if (console == CONSOLE_CGB) {
		f_cgb |= 0x80u;
		base_anim = SPRITE_ANIM_RED_NPC_UP;
	}
	wPlayerSpriteBaseAnimation = base_anim;

	(void)CreateSpriteAndAnimBufferEntry(SPRITE_OW_PLAYER, f_cgb);
	wPlayerSpriteIndex = wWhichSprite;

	uint8_t cur_map = wCurMap;
	uint8_t dir = SOUTH;
	if (cur_map != OVERWORLD_MAP)
		dir = wTempPlayerDirection;
	wPlayerDirection = dir;
	UpdatePlayerSprite();

	if (cur_map != OVERWORLD_MAP) {
		uint16_t hl = 0u;
		(void)Func_c6f7(&hl);
	}

	wPlayerCurrentlyMoving = 0u;
	wd338 = 0u;
	if (cur_map == OVERWORLD_MAP)
		OverworldMap_InitCursorSprite();
}
/* <<< factory Func_c4b9 */

/* >>> factory DecompressPermissionMap */
DecompressPermissionMapResult DecompressPermissionMap(uint16_t hl)
{
	uint8_t ptr_lo = gb_read8(wBGMapPermissionDataPtr_ADDR);
	uint8_t ptr_hi = gb_read8((uint16_t)(wBGMapPermissionDataPtr_ADDR + 1u));
	if ((uint8_t)(ptr_hi | ptr_lo) == 0u)
		return (DecompressPermissionMapResult){hl, ptr_hi, ptr_lo};

	InitDataDecompression((uint16_t)((uint16_t)ptr_hi << 8 | ptr_lo), 0xC0u);
	wTempPointerBank = wBGMapBank;
	uint8_t rows = (uint8_t)((uint8_t)(wBGMapHeight + 1u) >> 1);
	uint8_t cols = (uint8_t)((uint8_t)(wBGMapWidth + 1u) >> 1);
	uint16_t dest = hl;
	do {
		DecompressDataFromBank(cols, dest);
		dest = (uint16_t)(dest + 0x10u);
		rows--;
	} while (rows != 0u);
	return (DecompressPermissionMapResult){hl, (uint8_t)(dest >> 8), (uint8_t)dest};
}
/* <<< factory DecompressPermissionMap */

/* >>> factory LoadPermissionMap */
void LoadPermissionMap(void)
{
	for (uint16_t i = 0; i < 256u; i++)
		gb_write8((uint16_t)(wPermissionMap_ADDR + i), 0x80u);
	DecompressPermissionMap(wPermissionMap_ADDR);
}
/* <<< factory LoadPermissionMap */

/* >>> factory Func_c1ed */
void Func_c1ed(void)
{
	ClearEvents();
	LoadBackupSaveData();
	DetermineImakuniAndChallengeHall();
}
/* <<< factory Func_c1ed */

/* >>> factory Func_c1b1 */
void Func_c1b1(void)
{
	wOverworldMapSelection = OWMAP_POKEMON_DOME;
	wTempMap = OVERWORLD_MAP;
	wTempPlayerXCoord = 0x0Cu;
	wTempPlayerYCoord = 0x0Cu;
	wTempPlayerDirection = SOUTH;
	ClearEvents();
	DetermineImakuniAndChallengeHall();
	ClearOWMapEvents();
	uint8_t f_out;
	(void)ClearMasterBeatenList(&f_out);
	ChallengeMachine_Reset();
	gb_write8((uint16_t)(wPlayTimeCounter_ADDR + 0u), 0u);
	gb_write8((uint16_t)(wPlayTimeCounter_ADDR + 1u), 0u);
	gb_write8((uint16_t)(wPlayTimeCounter_ADDR + 2u), 0u);
	gb_write8((uint16_t)(wPlayTimeCounter_ADDR + 3u), 0u);
	gb_write8((uint16_t)(wPlayTimeCounter_ADDR + 4u), 0u);
}
/* <<< factory Func_c1b1 */

/* >>> factory Func_c554 */
void Func_c554(void)
{
	wWhichSprite = wPlayerSpriteIndex;
	if (wCurMap == OVERWORLD_MAP) {
		OverworldMap_UpdatePlayerAndCursorSprites();
		return;
	}
	Func_c58b();
	uint8_t scx = wSCXBuffer;
	uint8_t scy = wSCYBuffer;
	uint16_t hl = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
	uint8_t x = (uint8_t)((uint8_t)(wPlayerXCoordPixels - scx) + 8u);
	gb_write8(hl, x);
	hl++;
	uint8_t y = (uint8_t)((uint8_t)(wPlayerYCoordPixels - scy) + 0x10u);
	gb_write8(hl, y);
}
/* <<< factory Func_c554 */

/* >>> factory Func_c280 */
void Func_c280(void)
{
	BackupPlayerPosition();
	EnableAndClearSpriteAnimations();
	ZeroObjectPositions();
	wVBlankOAMCopyToggle = (uint8_t)(wVBlankOAMCopyToggle + 1u);
	EnableLCD();
	DoFrameIfLCDEnabled();
	DisableLCD();
	Func_12871();
}
/* <<< factory Func_c280 */

/* >>> factory UpdateOverworldMap */
void UpdateOverworldMap(void)
{
	OverworldMap_Update();
}
/* <<< factory UpdateOverworldMap */

/* >>> factory DisplayPauseMenu */
void DisplayPauseMenu(void)
{
	uint8_t selected = wSelectedPauseMenuItem;
	InitAndPrintMenu(PAUSE_MENU_PARAMS, selected);
}
/* <<< factory DisplayPauseMenu */

/* >>> factory Func_c8ed */
FuncC8edResult Func_c8ed(uint16_t hl)
{
	(void)SetOverworldNPCFlags(1u);
	(void)Func_c915();
	DoFrameIfLCDEnabled();
	HandleYesOrNoMenuResult result;
	if (hl != 0u) {
		gb_write8(wd3b9_ADDR, 0u);
		gb_write8((uint16_t)(wd3b9_ADDR + 1u), 0u);
		result = YesOrNoMenuWithText(hl);
	} else {
		result = YesOrNoMenu();
	}
	return (FuncC8edResult){result.a, result.f};
}
/* <<< factory Func_c8ed */

/* >>> factory PauseMenu_Diary */
void PauseMenu_Diary(void)
{
	_PauseMenu_Diary();
}
/* <<< factory PauseMenu_Diary */

/* >>> factory DisplayPCMenu */
void DisplayPCMenu(void)
{
	uint8_t selected = wSelectedPCMenuItem;
	uint8_t saved_bank = hBankROM;
	BankswitchROM(PC_MENU_BANK);
	InitAndPrintMenu(PC_MENU_PARAMS, selected);
	BankswitchROM(saved_bank);
}
/* <<< factory DisplayPCMenu */

/* >>> factory Func_c268 */
void Func_c268(void)
{
	uint16_t hl = PAUSE_MENU_TEXT_LIST_ADDR;
	for (;;) {
		const uint8_t *entry = rom_ptr(PAUSE_MENU_TEXT_LIST_BANK, hl);
		uint16_t text_id = (uint16_t)(entry[0] | ((uint16_t)entry[1] << 8));
		hl = (uint16_t)(hl + 2u);
		if (text_id == 0u)
			break;
		(void)ProcessTextFromID(text_id);
	}
}
/* <<< factory Func_c268 */

/* >>> factory PauseMenu_Status */
void PauseMenu_Status(void)
{
	_PauseMenu_Status();
}
/* <<< factory PauseMenu_Status */

/* >>> factory Func_c258 */
void Func_c258(void)
{
	uint8_t saved_hffb0 = hffb0;
	hffb0 = 2u;
	Func_c268();
	hffb0 = saved_hffb0;
}
/* <<< factory Func_c258 */

/* >>> factory Func_c251 */
/* >>> factory Func_c251 */
void Func_c251(void)
{
	uint8_t saved_hffb0 = hffb0;
	hffb0 = 1u;
	Func_c268();
	hffb0 = saved_hffb0;
}
/* <<< factory Func_c251 */

/* >>> factory Func_c241 */
void Func_c241(void)
{
	(void)SetupText(0x30u, 0x7Fu);
	Func_c258();
}
/* <<< factory Func_c241 */

/* >>> factory Func_c141 */
/* overworld.asm:156-166 -- seventeen bytes with FOUR exits:
 *   wActiveGameEvent == 0 -> `ret z`, an ordinary return, nothing cleared
 *   otherwise it clears the event and dispatches through PointerTable_c152:
 *     GAME_EVENT_DUEL          (1) -> Func_c9bc  $49BC
 *     GAME_EVENT_BATTLE_CENTER (2) -> Func_fc2b  $7C2B
 *     GAME_EVENT_GIFT_CENTER   (3) -> Func_fcad  $7CAD
 * Each case declares the completion its seed reaches, so the dispatch target is
 * observed as a stop point AND as `hl`.
 *
 * `push af` / `xor a` / `ld [hl], a` / `pop af` clears the event while restoring
 * a and f, so `dec a` sees the ORIGINAL event value and the table index is
 * event-1. JumpToFunctionInTable is an excluded leaf-slice, resolved here:
 *   add a / add l / ld l, a / ld a, $0 / adc h / ld a, [hli] / ld h, [hl] /
 *   ld l, a / jp hl
 * so at the target a = target & 0xFF, hl = target, and f comes from the `adc h`
 * that finishes the 16-bit index add -- not from the pointer load, since `ld`
 * never touches flags. */
Func_c141Result Func_c141(void)
{
	uint16_t hl = wActiveGameEvent_ADDR;
	uint8_t event = gb_read8(hl);
	uint8_t idx2, lo, hi, carry, res, f;
	uint16_t sum, entry, target;
	const uint8_t *p;

	if (event == 0u)
		return (Func_c141Result){0u, 0x80u, hl}; /* or a set Z; ret z */

	gb_write8(hl, 0u);
	idx2 = (uint8_t)((uint8_t)(event - 1u) << 1); /* dec a ; add a */
	lo = (uint8_t)POINTER_TABLE_C152;
	hi = (uint8_t)(POINTER_TABLE_C152 >> 8);
	sum = (uint16_t)idx2 + lo;                     /* add l */
	carry = (uint8_t)(sum > 0xFFu);
	res = (uint8_t)(hi + carry);                   /* ld a, $0 ; adc h */
	f = 0u;
	if (res == 0u)
		f |= 0x80u;
	if (((hi & 0x0Fu) + carry) > 0x0Fu)
		f |= 0x20u;
	if (((uint16_t)hi + carry) > 0xFFu)
		f |= 0x10u;

	entry = (uint16_t)((uint16_t)res << 8 | (uint8_t)sum);
	p = rom_ptr(POINTER_TABLE_C152_BANK, entry);
	target = (uint16_t)(p[0] | (uint16_t)p[1] << 8);
	return (Func_c141Result){(uint8_t)(target & 0xFFu), f, target};
}
/* <<< factory Func_c141 */

/* >>> factory CloseTextBox */
void CloseTextBox(void)
{
	ReloadMapAfterTextClose();
	uint8_t flags = wOverworldNPCFlags;
	flags = (uint8_t)(flags & (uint8_t)~(1u << AUTO_CLOSE_TEXTBOX));
	wOverworldNPCFlags = flags;
}
/* <<< factory CloseTextBox */

/* >>> factory Func_c891 */
void Func_c891(uint16_t hl)
{
	if ((wOverworldNPCFlags & (1u << AUTO_CLOSE_TEXTBOX)) != 0u &&
	    (wd3b9 != 0u || gb_read8((uint16_t)(wd3b9_ADDR + 1u)) != 0u)) {
		CloseTextBox();
	}
	wd3b9 = 0u;
	gb_write8((uint16_t)(wd3b9_ADDR + 1u), 0u);
	(void)SetOverworldNPCFlags(1u << AUTO_CLOSE_TEXTBOX);
	Func_c241();
	(void)Func_c915();
	DoFrameIfLCDEnabled();
	(void)PrintScrollableText_NoTextBoxLabel(hl);
}
/* <<< factory Func_c891 */

/* >>> factory ReturnToOverworld */
uint8_t ReturnToOverworld(void)
{
	DisableLCD();
	Set_OBJ_8x8();
	EnableAndClearSpriteAnimations();
	Func_12bcd();
	hWhoseTurn = PLAYER_TURN;
	Func_c241();
	EmptyScreen();
	uint8_t default_song = wDefaultSong;
	LoadMapGfxAndPermissions();
	wDefaultSong = default_song;
	wOverworldNPCFlags &= (uint8_t)~(1u << AUTO_CLOSE_TEXTBOX);
	RestoreObjectPalettes();
	Func_12c5e();
	SetAllNPCTilePermissions();
	wOverworldNPCFlags &= (uint8_t)~(1u << HIDE_ALL_NPC_SPRITES);
	uint8_t callback_lo = gb_read8(wReloadOverworldCallbackPtr_ADDR);
	uint8_t callback_hi = gb_read8(wReloadOverworldCallbackPtr_ADDR + 1u);
	(void)callback_lo;
	(void)callback_hi;
	return FadeScreenFromWhite();
}
/* <<< factory ReturnToOverworld */

/* >>> factory CloseAdvancedDialogueBox */
void CloseAdvancedDialogueBox(void)
{
	uint8_t flags = wOverworldNPCFlags;
	if (flags & (uint8_t)(1u << AUTO_CLOSE_TEXTBOX))
		CloseTextBox();
	flags = wOverworldNPCFlags;
	if (flags & (uint8_t)(1u << RESTORE_FACING_DIRECTION)) {
		wLoadedNPCTempIndex = wScriptNPC;
		(void)Func_1c5e9();
	}
	wOverworldNPCFlags = 0u;
	wOverworldMode = wOverworldModeBackup;
}
/* <<< factory CloseAdvancedDialogueBox */

/* >>> factory Func_c8ba */
void Func_c8ba(uint16_t hl, uint16_t de)
{
	if (de == 0u) {
		Func_c891(hl);
		return;
	}
	uint8_t flags = wOverworldNPCFlags;
	if ((flags & (1u << AUTO_CLOSE_TEXTBOX)) != 0u) {
		if (wd3b9 != (uint8_t)de ||
		    gb_read8((uint16_t)(wd3b9_ADDR + 1u)) != (uint8_t)(de >> 8)) {
			CloseTextBox();
		}
	}
	wd3b9 = de;
	gb_write8((uint16_t)(wd3b9_ADDR + 1u), (uint8_t)(de >> 8));
	(void)SetOverworldNPCFlags(1u << AUTO_CLOSE_TEXTBOX);
	Func_c241();
	(void)Func_c915();
	DoFrameIfLCDEnabled();
	(void)PrintScrollableText_WithTextBoxLabel(hl, de);
}
/* <<< factory Func_c8ba */

/* >>> factory ReturnToOverworldNoCallback */
uint8_t ReturnToOverworldNoCallback(void)
{
	wReloadOverworldCallbackPtr = 0u;
	gb_write8((uint16_t)(wReloadOverworldCallbackPtr_ADDR + 1u), 0u);
	return ReturnToOverworld();
}
/* <<< factory ReturnToOverworldNoCallback */

/* >>> factory ReturnToOverworldWithCallback */
uint8_t ReturnToOverworldWithCallback(uint16_t hl)
{
	wReloadOverworldCallbackPtr = (uint8_t)hl;
	gb_write8((uint16_t)(wReloadOverworldCallbackPtr_ADDR + 1u), (uint8_t)(hl >> 8));
	return ReturnToOverworld();
}
/* <<< factory ReturnToOverworldWithCallback */

/* >>> factory FindNPCOrObject */
FindNPCOrObjectResult FindNPCOrObject(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	wScriptNPC = 0xffu;
	FindPlayerMovementWithOffsetResult movement = FindPlayerMovementFromDirection();
	uint8_t permission = GetPermissionOfMapPosition(movement.b, movement.c);
	uint8_t next_a = (uint8_t)(permission & 0x40u);
	uint8_t next_f = (next_a == 0u) ? 0xa0u : 0x20u;
	uint8_t next_b = movement.b;
	uint8_t next_c = movement.c;
	if (next_a != 0u) {
		FindNPCAtLocationResult npc = FindNPCAtLocation(next_b, next_c, d, e, hl);
		if ((npc.f & 0x10u) == 0u) {
			wScriptNPC = wLoadedNPCTempIndex;
			wOverworldMode = OWMODE_START_SCRIPT;
			return (FindNPCOrObjectResult){OWMODE_START_SCRIPT, 0x10u, npc.b, npc.c, npc.d, npc.e, npc.hl};
		}
		next_a = npc.a;
		next_f = npc.f;
		next_b = npc.b;
		next_c = npc.c;
		d = npc.d;
		e = npc.e;
		hl = npc.hl;
	}
	HandleMoveModeAPressResult move = HandleMoveModeAPress(next_a, next_f, next_b, next_c, d, e, hl);
	if ((move.f & 0x10u) == 0u)
		return (FindNPCOrObjectResult){move.a, (move.a == 0u) ? 0x80u : 0u, move.b, move.c, move.d, move.e, move.hl};
	wOverworldMode = OWMODE_SCRIPT;
	return (FindNPCOrObjectResult){OWMODE_SCRIPT, 0x10u, move.b, move.c, move.d, move.e, move.hl};
}
/* <<< factory FindNPCOrObject */

/* >>> factory Func_c6dc */
FuncC6dcResult Func_c6dc(uint16_t saved_hl)
{
	uint16_t movement_hl = 0xD335u;
	wPlayerCurrentlyMoving = (uint8_t)(wPlayerCurrentlyMoving & (uint8_t)~0x03u);
	(void)Func_c6f7(&movement_hl);
	HandleMapWarp();
	(void)Func_c70d();
	uint8_t mode = wOverworldMode;
	if (mode == OWMODE_MOVE) {
		CallMapScriptResult script = Func_c9c0();
		return (FuncC6dcResult){script.a, script.f, 0x0Eu, saved_hl};
	}
	uint8_t flags = 0x40u;
	if ((mode & 0x0Fu) < (OWMODE_MOVE & 0x0Fu))
		flags |= 0x20u;
	if (mode < OWMODE_MOVE)
		flags |= 0x10u;
	return (FuncC6dcResult){mode, flags, 0x0Eu, saved_hl};
}
/* <<< factory Func_c6dc */

/* >>> factory HandlePlayerMoveModeInput */
void HandlePlayerMoveModeInput(void)
{
	uint8_t held = hKeysHeld;
	if ((held & PAD_CTRL_PAD) != 0u) {
		UpdatePlayerDirectionFromDPad((uint8_t)(held & PAD_CTRL_PAD));
		AttemptPlayerMovementFromDirection();
		if ((wPlayerCurrentlyMoving & 1u) != 0u)
			return;
	}
	if ((hKeysPressed & PAD_A) != 0u) {
		(void)FindNPCOrObject(1u, 0u, 0u, 0u, 0u, 0u, 0u);
	}
}
/* <<< factory HandlePlayerMoveModeInput */

/* >>> factory PCMenu_Glossary */
void PCMenu_Glossary(void)
{
	_PCMenu_Glossary();
}
/* <<< factory PCMenu_Glossary */

/* >>> factory Func_c17a */
FuncC17aResult Func_c17a(uint16_t hl)
{
	if (wOverworldMode == OWMODE_SCRIPT) {
		FuncC17aResult result = {wOverworldMode, 0xC0u, hl};
		return result;
	}
	CallMapScriptResult result = Func_c9b8();
	return (FuncC17aResult){result.a, result.f, result.hl};
}
/* <<< factory Func_c17a */

/* >>> factory Func_c53d */
void Func_c53d(void)
{
	wWhichSprite = wPlayerSpriteIndex;
	if ((wPlayerCurrentlyMoving & 0x01u) != 0u)
		Func_c687();
	if ((wPlayerCurrentlyMoving & 0x02u) != 0u)
		(void)Func_c6dc(0u);
}
/* <<< factory Func_c53d */

/* >>> factory PCMenu_CardAlbum */
void PCMenu_CardAlbum(void)
{
	hSCX = 0u;
	hSCY = 0u;
	Set_OBJ_8x16();
	SetDefaultPalettes();
	CardAlbum();
	Set_OBJ_8x8();
}
/* <<< factory PCMenu_CardAlbum */

/* >>> factory PauseMenu_Config */
void PauseMenu_Config(void)
{
	_PauseMenu_Config();
}
/* <<< factory PauseMenu_Config */

/* >>> factory PCMenu_ReadMail */
/* overworld.asm:1264-1266. `farcall _PCMenu_ReadMail / ret`: rst $28's tail
 * (SwitchToBankAtSP, home/farcall.asm:44-55) pushes and pops af around the bank
 * restore, so the byte the callee leaves in a is this routine's own result. The
 * bank switch has no C model -- hBankROM ends holding the caller's own bank. */
uint8_t PCMenu_ReadMail(void)
{
	return _PCMenu_ReadMail();
}
/* <<< factory PCMenu_ReadMail */

/* >>> factory Func_c2a3 */
/* overworld.asm:363-384. hl, bc and de are pushed on entry and popped before
 * the ret, so only a and f are clobbered. */
void Func_c2a3(void)
{
	BackupObjectPalettes();
	FadeScreenToWhite();
	(void)SetOverworldNPCFlags(0x80u); /* 1 << HIDE_ALL_NPC_SPRITES, HIDE_ALL_NPC_SPRITES = 7 */
	(void)SetupText(0x30u, 0x7fu);
	Func_12ba7();
	EnableAndClearSpriteAnimations();
	ZeroObjectPositions();
	wVBlankOAMCopyToggle = 1u; /* TRUE */
	EnableLCD();
	DoFrameIfLCDEnabled();
	DisableLCD();
}
/* <<< factory Func_c2a3 */

/* >>> factory PauseMenu_Card */
void PauseMenu_Card(void)
{
	hSCX = 0u;
	hSCY = 0u;
	Set_OBJ_8x16();
	SetDefaultPalettes();
	HandlePlayersCardsScreen();
	Set_OBJ_8x8();
}
/* <<< factory PauseMenu_Card */
