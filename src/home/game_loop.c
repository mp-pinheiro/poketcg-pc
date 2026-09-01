#include "home/game_loop.h"

#include "home/frames.h"
#include "home/input.h"
#include "home/duel_core.h"
#include "home/lcd.h"
#include "home/process_text.h"
#include "home/tiles.h"
/* >>> factory statics */
#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/credits_sequence_commands.h"
#include "home/main_menu.h"
#include "home/menus.h"
#include "home/serial.h"
#include "home/switch_sram.h"
#include "home/unused_save_validation.h"
#include "mem.h"
#define PAD_A 0x01u
#define PAD_B 0x02u
#define IE_VBLANK 0x01u
#define IE_TIMER 0x04u
#define rIE 0xFFFFu
#define ResetBackUpRamText 0x00a2u
/* <<< factory statics */

void SetupResetBackUpRamScreen(void)
{
	wTileMapFill = 0;
	DisableLCD();
	LoadSymbolsFont();
	SetDefaultConsolePalettes();
	SetupText(0x38, 0x7F);
}

/* >>> factory InitSaveDataAndSetUppercase */
void InitSaveDataAndSetUppercase(void)
{
	InitSaveData();
	wUppercaseHalfWidthLetters = 1u;
}
/* <<< factory InitSaveDataAndSetUppercase */

/* >>> factory GameLoop */
void GameLoop(void)
{
	ResetSerial();
	uint8_t interrupt_enable = gb_read8(rIE);
	gb_write8(rIE, (uint8_t)(interrupt_enable | IE_VBLANK));
	interrupt_enable = gb_read8(rIE);
	gb_write8(rIE, (uint8_t)(interrupt_enable | IE_TIMER));
	EnableSRAM();
	wTextSpeed = sTextSpeed;
	wSkipDelayAllowed = sSkipDelayAllowed;
	DisableSRAM();
	wUppercaseHalfWidthLetters = 1u;
	StubbedUnusedSaveDataValidation();
	if (hKeysHeld != (PAD_A | PAD_B)) {
		if (!frame_boundary_is_installed()) {
			/* Probe world: the oracle stops GameLoop pre-ret at the
			 * _GameLoop dispatch (game_loop.asm:22), so run the bounded
			 * prefix exactly once instead of looping. */
			_GameLoop();
			return;
		}
		for (;;)
			_GameLoop(); /* game_loop.asm:22-23 */
	}

	SetupResetBackUpRamScreen();
	EmptyScreen();
	HandleYesOrNoMenuResult menu = YesOrNoMenuWithText(ResetBackUpRamText);
	if ((menu.f & 0x10u) == 0u) {
		EnableSRAM();
		s0a000 = 0u;
		DisableSRAM();
	}
	(void)Reset(); /* .reset_game: jp Reset (game_loop.asm:35-36) */
}
/* <<< factory GameLoop */
