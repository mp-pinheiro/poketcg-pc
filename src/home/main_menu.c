#include "home/main_menu.h"
#include "home/start.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "runtime.h"
#include "generated/sram.h"
#include "home/map.h"
#include "home/naming.h"
#include "home/starter_deck.h"
#include "home/switch_sram.h"
/* >>> factory statics */
#include "home/common.h"
#include "home/lcd_enable_frame.h"
#define MUSIC_OVERWORLD 0x09u
#include "home/overworld.h"
#include "home/sound.h"
#include "generated/wram.h"
#define MUSIC_CARD_POP 0x08u
#define MUSIC_STOP 0x00u
#define GAME_EVENT_OVERWORLD 0x00u
#define GAME_EVENT_CONTINUE_DUEL 0x05u
#define PLAYER_TURN 0xC2u

#include "home/scripting.h"

#include "home/objects.h"
#include "generated/wram.h"
#include "home/frames.h"
#include "home/save.h"
/* <<< factory statics */

/* >>> factory MainMenu_CardPop */
uint8_t MainMenu_CardPop(void)
{
	PlaySong(MUSIC_CARD_POP);
	DoCardPop();
	WhiteOutDMGPals();
	DoFrameIfLCDEnabled();
	PlaySong(MUSIC_STOP);
	return 0x10u;
}
/* <<< factory MainMenu_CardPop */

/* >>> factory MainMenu_NewGame */
uint8_t MainMenu_NewGame(void)
{
	runtime_mark_event(RUNTIME_EVENT_NEW_GAME_ENTERED);
	Func_c1b1();
	if (!frame_boundary_is_installed()) {
		/* Probe world: the oracle stops pre-ret right after Func_c1b1
		 * (main_menu.asm:33); the naming and portrait screens below are
		 * frame-driven and never terminate without the host loop. */
		return 0x00u;
	}
	(void)DisplayPlayerNamingScreen();
	InitSaveData();
	EnableSRAM();
	wAnimationsDisabled = sAnimationsDisabled;
	wTextSpeed = sTextSpeed;
	DisableSRAM();
	PlaySong(MUSIC_STOP);
	/* `farcall SetMainSGBBorder` (engine/sgb.asm:1-14) returns at its own
	 * first compare unless the console is SGB, and the SGB path it guards
	 * has no C body in this tree; the CGB/DMG path is a no-op. */
	wDefaultSong = MUSIC_OVERWORLD;
	(void)PlayDefaultSong();
	DrawPlayerPortraitAndPrintNewGameText();
	wGameEvent = GAME_EVENT_OVERWORLD;
	ExecuteGameEvent();
	return 0x00u; /* or a; ret */
}
/* <<< factory MainMenu_NewGame */

/* >>> factory MainMenu_ContinueFromDiary */
uint8_t MainMenu_ContinueFromDiary(void)
{
	PlaySong(MUSIC_STOP);
	if (!frame_boundary_is_installed()) {
		/* Probe world: the oracle stops pre-ret at the song stop
		 * (main_menu.asm:56-57), before backup save validation. */
		return 0x00u;
	}
	ValidateResult backup = ValidateBackupGeneralSaveData();
	if ((backup.f & 0x10u) == 0u)
		return MainMenu_NewGame(); /* jr nc: invalid backup save */
	Func_c1ed();
	/* SetMainSGBBorder is SGB-only; see MainMenu_NewGame. */
	EnableSRAM();
	sPlayerInChallengeMachine = 0u;
	DisableSRAM();
	wGameEvent = GAME_EVENT_OVERWORLD;
	ExecuteGameEvent();
	return 0x00u; /* or a; ret */
}
/* <<< factory MainMenu_ContinueFromDiary */

/* >>> factory MainMenu_ContinueDuel */
uint8_t MainMenu_ContinueDuel(void)
{
	PlaySong(MUSIC_STOP);
	ClearEvents();
	if (!frame_boundary_is_installed()) {
		/* Probe world: the oracle stops pre-ret after ClearEvents
		 * (main_menu.asm:85-86), before the bank-$04 save load. */
		return 0x00u;
	}
	LoadGeneralSaveData();
	/* SetMainSGBBorder is SGB-only; see MainMenu_NewGame. */
	wGameEvent = GAME_EVENT_CONTINUE_DUEL;
	ExecuteGameEvent();
	return 0x00u; /* or a; ret */
}
/* <<< factory MainMenu_ContinueDuel */

/* >>> factory _GameLoop */
typedef uint8_t (*MainMenuFunction)(void);

/* main_menu.asm:26-30 */
static const MainMenuFunction MainMenuFunctionTable[] = {
	MainMenu_CardPop,
	MainMenu_ContinueFromDiary,
	MainMenu_NewGame,
	MainMenu_ContinueDuel,
};

void _GameLoop(void)
{
	for (;;) { /* jr _GameLoop: virtually restart game (main_menu.asm:20) */
		ZeroObjectPositions();
		wVBlankOAMCopyToggle = (uint8_t)(wVBlankOAMCopyToggle + 1u);
		/* `farcall SetIntroSGBBorder` (engine/sgb.asm:17-21) is SGB-only;
		 * the non-SGB early return is what runs, so it is a no-op here. */
		wLastSelectedStartMenuItem = 0xFFu;
		if (!frame_boundary_is_installed()) {
			/* Probe world: the oracle stops pre-ret before
			 * .main_menu_loop (main_menu.asm:11); keep the bounded
			 * prefix instead of dispatching into the menu table. */
			Func_c1f8();
			HandleTitleScreen();
			return;
		}
		for (;;) { /* .main_menu_loop */
			hWhoseTurn = PLAYER_TURN;
			Func_c1f8();
			HandleTitleScreen();
			if ((MainMenuFunctionTable[wStartMenuChoice]() & 0x10u) != 0u)
				continue; /* jr c: return to main menu */
			break; /* jr _GameLoop */
		}
	}
}
/* <<< factory _GameLoop */
