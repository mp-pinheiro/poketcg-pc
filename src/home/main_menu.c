#include "home/main_menu.h"
#include "home/start.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/common.h"
#include "home/lcd_enable_frame.h"
#include "home/overworld.h"
#include "home/sound.h"
#include "generated/wram.h"
#define MUSIC_CARD_POP 0x08u
#define MUSIC_STOP 0x00u

#include "home/scripting.h"

#include "home/objects.h"
#include "generated/wram.h"
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
void MainMenu_NewGame(void)
{
	Func_c1b1();
	wGameEvent = 0u;
}
/* <<< factory MainMenu_NewGame */

/* >>> factory MainMenu_ContinueFromDiary */
void MainMenu_ContinueFromDiary(void)
{
	PlaySong(MUSIC_STOP);
}
/* <<< factory MainMenu_ContinueFromDiary */

/* >>> factory MainMenu_ContinueDuel */
void MainMenu_ContinueDuel(void)
{
	PlaySong(MUSIC_STOP);
	ClearEvents();
}
/* <<< factory MainMenu_ContinueDuel */

/* >>> factory _GameLoop */
void _GameLoop(void)
{
	ZeroObjectPositions();
	wVBlankOAMCopyToggle = (uint8_t)(wVBlankOAMCopyToggle + 1u);
	/* SetIntroSGBBorder is scope-excluded by the Phase 1 transform. */
	Func_c1f8();
	wLastSelectedStartMenuItem = 0xFFu;
	HandleTitleScreen();
}
/* <<< factory _GameLoop */
