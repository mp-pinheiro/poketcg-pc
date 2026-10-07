/* >>> part includes */
#include "home/overworld.h"

#include <stdio.h>
#include <stdlib.h>

#include "home/script_entry_dispatch.h"
#include "home/card_id_bus.h"

#include "generated/text_ids.h"
#include "generated/rom.h"
#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/frames.h"
#include "home/decompress.h"
#include "home/memory.h"
/* <<< part includes */
/* --- part includes_SPRITE_OW_MINT */
/* --- part SPRITE_OW_MINT */
/* >>> part includes_PAUSE_MENU_PARAMS */
#include "home/load_gfx.h"
#include "home/sprite_animations.h"
#include "home/overworld_map.h"


#include "home/scripting.h"
#include "home/battle_center.h"
#include "home/gift_center.h"
#include "home/save.h"
#include "generated/hram.h"

#include "home/scripting.h"
#include "home/map_events.h"
#include "home/masters_beaten_list.h"
#include "home/challenge_machine.h"
#include "generated/wram.h"
#include "generated/hram.h"

#include "home/overworld.h"
#include "home/load_animation.h"
#include "home/overworld_map.h"
#include "generated/wram.h"

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
/* <<< part includes_PAUSE_MENU_PARAMS */
/* >>> part includes_tail */
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/animation.h"
#include "home/core.h"
#include "home/color.h"
#include "home/credits_sequence_commands.h"
#include "home/duel_init.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/load_animation.h"
#include "home/load_overworld.h"
#include "home/map.h"
#include "home/npc_core.h"
#include "home/objects.h"
#include "home/overworld.h"
#include "home/scripting.h"
#include "home/sound.h"
#include "home/switch_sram.h"
#include "home/tiles.h"


#include "generated/hram.h"
#include "home/printer.h"
#include "generated/wram.h"
/* <<< part includes_tail */
/* >>> factory Func_c1f8 */
/* overworld.asm:245-261. */
void Func_c1f8(void)
{
	wSelectedPauseMenuItem = 0u;
	wSelectedPCMenuItem = 0u;
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
/* --- factory Func_c430 */
/* >>> factory Func_c41c */
void Func_c41c(void)
{
	wSCXBuffer = (uint8_t)(wPlayerXCoordPixels - 0x40u);
	wSCYBuffer = (uint8_t)(wPlayerYCoordPixels - 0x40u);

	uint8_t max_x = (uint8_t)(wd237 << 3);
	uint8_t scx = wSCXBuffer;
	if (scx >= 0xB1u) {
		scx = 0u;
	} else if (scx >= max_x) {
		scx = max_x;
	}
	wSCXBuffer = scx;

	uint8_t max_y = (uint8_t)(wd238 << 3);
	uint8_t scy = wSCYBuffer;
	if (scy >= 0xB9u) {
		scy = 0u;
	} else if (scy >= max_y) {
		scy = max_y;
	}
	wSCYBuffer = scy;
}
/* <<< factory Func_c41c */
/* >>> factory Func_c36a */
void Func_c36a(void)
{
	wOWMapEvents = 0u;
	if (wCurMap == POKEMON_DOME_ENTRANCE)
		gb_write8((uint16_t)(wOWMapEvents_ADDR + 1u), 0u);
}
/* <<< factory Func_c36a */
/* >>> factory Func_c4b9 */
void Func_c4b9(void)
{
	wWhichOBP = 0u;
	wWhichOBPalIndex = 0u;
	LoadOBPalette(PALETTE_29);
	wPlayerSpriteBaseAnimation = SPRITE_ANIM_RED_NPC_UP;

	(void)CreateSpriteAndAnimBufferEntry(SPRITE_OW_PLAYER, 0u);
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
/* --- factory Func_c251 */
/* >>> factory Func_c141 */
Func_c141Result Func_c141(void)
{
	uint8_t event = gb_read8(wActiveGameEvent_ADDR);
	if (event == 0u)
		return (Func_c141Result){0u, 0x80u, wActiveGameEvent_ADDR};
	gb_write8(wActiveGameEvent_ADDR, 0u);
	if (event == GAME_EVENT_DUEL) {
		CallMapScriptResult r = Func_c9bc();
		return (Func_c141Result){r.a, r.f, r.hl};
	}
	return (Func_c141Result){0u, 0u, 0u};
}
/* <<< factory Func_c141 */
/* --- factory EnterScript */
/* >>> factory SetScriptData */
SetScriptDataResult SetScriptData(uint16_t hl)
{
	uint8_t script_npc = wScriptNPC;
	wLoadedNPCTempIndex = script_npc;
	SetNewScriptNPCResult npc = SetNewScriptNPC(hl);
	wNextScriptBank = npc.a;
	wNextScript = npc.c;
	wNextScript_PTR[1] = npc.b;
	wOverworldMode = OWMODE_SCRIPT;
	ScriptEntryRegs entered = ScriptEntryEnterWithBank(
		(uint16_t)(wNextScript | ((uint16_t)wNextScript_PTR[1] << 8)),
		npc.a, npc.f, npc.b, npc.c, 0u, 0u);
	entered.a = npc.a;
	return (SetScriptDataResult){entered.a, entered.f, entered.b, entered.c, entered.hl};
}
/* <<< factory SetScriptData */
/* >>> factory HandleOverworldMode */
void HandleOverworldMode(uint16_t hl)
{
	uint8_t mode = (uint8_t)(wOverworldMode & 0x7fu);
	switch (mode) {
	case 0u:
		UpdateOverworldMap();
		break;
	case 1u:
		CallHandlePlayerMoveMode();
		break;
	case 2u:
		(void)SetScriptData(hl);
		break;
	case 3u: {
		(void)ScriptEntryEnterWithBank(
			(uint16_t)(wNextScript |
				((uint16_t)gb_read8((uint16_t)(wNextScript_ADDR + 1u)) << 8)),
			wNextScriptBank, 0u, 0u, 0u, 0u, 0u);
		break;
	}
	default:
		break;
	}
}
/* <<< factory HandleOverworldMode */
/* >>> factory LoadMap */
void LoadMap(void)
{
	DisableLCD();
	EnableSRAM();
	DiscardSavedDuelData();
	DisableSRAM();
	wGameEvent = GAME_EVENT_OVERWORLD;
	wReloadOverworldCallbackPtr = 0u;
	gb_write8((uint16_t)(wReloadOverworldCallbackPtr_ADDR + 1u), 0u);
	wMatchStartTheme = 0u;
	wd317 = 0u;
	WhiteOutDMGPals();
	ZeroObjectPositions();
	wTileMapFill = 0u;
	(void)LoadSymbolsFont();
	Set_OBJ_8x8();
	wLineSeparation = DOUBLE_SPACED;
	wd291 = 0u;

	for (;;) {
		FadeScreenToWhite();
		WhiteOutDMGPals();
		Func_c241();
		EmptyScreen();
		EnableAndClearSpriteAnimations();
		hWhoseTurn = PLAYER_TURN;
		(void)ClearNPCs();
		wCurMap = wTempMap;
		wPlayerXCoord = wTempPlayerXCoord;
		wPlayerYCoord = wTempPlayerYCoord;
		Func_c36a();
		Func_c184();
		Func_c49c();
		LoadMapGfxAndPermissions();
		Func_c4b9();
		(void)Func_c943(0u, 0u, 0u, 0u, 0u, 0u, 0u);
		(void)Func_c158();
		DoMapOWFrame();
		SetOverworldDoFrameFunction();
		wOverworldTransition = 0u;
		wOverworldNPCFlags = 0u;
		(void)PlayDefaultSong();
		(void)FadeScreenFromWhite();
		Func_c141Result active_event = Func_c141();
		FuncC17aResult loaded = Func_c17a(active_event.hl);

		runtime_record_event(RUNTIME_EVENT_OVERWORLD_READY);

		/* overworld.asm:54-61 .overworld_loop. hl stays whatever Func_c17a
		 * left because DoFrameIfLCDEnabled/SetScreenScroll never set it, and
		 * nothing downstream dereferences it: SetNewScriptNPC and
		 * ResetDoFrameFunction both return it untouched. */
		uint8_t transition;

		do {
			DoFrameIfLCDEnabled();
			SetScreenScroll();
			HandleOverworldMode(loaded.hl);
			transition = wOverworldTransition;
		} while ((transition & 0xD0u) == 0u);

		DoFrameIfLCDEnabled();
		if ((wOverworldTransition & 0x10u) != 0u) {
			PlaySFX(SFX_WARP);
			continue;
		}

		/* overworld.asm:71-79 .no_warp */
		FadeScreenToWhite();
		(void)Func_c1a0(loaded.hl);
		if (wMatchStartTheme != 0u) {
			Func_c280();
			(void)Duel_Init(0u);
		}
		Func_c280();
		return;
	}
}
/* <<< factory LoadMap */
/* --- part PCMENU_PRINT_ADDR */
/* --- factory PCMenu_Print */
/* >>> factory PCMenu */
void PCMenu(void)
{
	PlaySong(MUSIC_PC_MAIN_MENU);
	Func_c241();
	(void)Func_c915();
	DoFrameIfLCDEnabled();
	(void)PrintScrollableText_NoTextBoxLabel(TurnedPCOnText);
	DisplayPCMenu();
	for (;;) {
		(void)SetOverworldNPCFlags((uint8_t)(1u << AUTO_CLOSE_TEXTBOX));
		HandleMenuInputResult input;
		do {
			DoFrameIfLCDEnabled();
			input = HandleMenuInput();
		} while ((input.f & 0x10u) == 0u);
		wSelectedPCMenuItem = input.e;
		if (hCurMenuItem != input.e || input.e == 0x03u)
			break;
		Func_c2a3();
		switch (wSelectedPCMenuItem) {
		case 0u:
			PCMenu_CardAlbum();
			break;
		case 1u:
			(void)PCMenu_ReadMail();
			break;
		case 2u:
			PCMenu_Glossary();
			break;
		}
		(void)ReturnToOverworldWithCallback(DISPLAY_PC_MENU);
	}
	CloseTextBox();
	DoFrameIfLCDEnabled();
	Func_c891(TurnedPCOffText);
	CloseAdvancedDialogueBox();
	wSongOverride = 0u;
	(void)PlayDefaultSong();
}
/* <<< factory PCMenu */
