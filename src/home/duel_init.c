#include "home/duel_init.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "home/color.h"
#include "home/init_menu.h"
#include "home/labels.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/load_animation.h"
#include "home/menus.h"
#include "home/play_song.h"
#include "home/sound.h"
#include "home/text_box.h"

/* duel_init.asm:57-69, in Duel_Init's own bank 04, so the interpreter reads
 * them through the bank the guard selects on entry. */
#define OPPONENT_TITLE_AND_NAME_LABEL 0x4451u
#define OPPONENT_DECK_NAME_LABEL      0x4456u
#define OPPONENT_TITLES_AND_DECK_NAMES 0x445Bu
/* <<< factory statics */

/* >>> factory Duel_Init */
DuelInitResult Duel_Init(uint8_t f)
{
	uint8_t saved_d291 = wd291;

	DisableLCD();
	(void)InitMenuScreen();
	wTextBoxFrameType = 4u;

	uint16_t box = 0u;
	DrawRegularTextBox(&box, 0u, 20u, 6u, 0u, 12u);

	uint16_t entry = (uint16_t)(OPPONENT_TITLES_AND_DECK_NAMES
				    + (uint8_t)(wNPCDuelDeckID << 2));
	wTxRam2 = gb_read8(entry);
	wTxRam2_PTR[1] = gb_read8((uint16_t)(entry + 1u));
	wTxRam2_b = wOpponentName;
	wTxRam2_b_PTR[1] = wOpponentName_PTR[1];
	(void)PrintLabels(OPPONENT_TITLE_AND_NAME_LABEL, 0u, 0u);

	uint8_t low = gb_read8((uint16_t)(entry + 2u));
	uint8_t high = gb_read8((uint16_t)(entry + 3u));
	wTxRam2 = low;
	wTxRam2_PTR[1] = high;
	if ((uint8_t)(high | low) != 0u)
		(void)PrintLabels(OPPONENT_DECK_NAME_LABEL, 0u, 0u);

	DrawOpponentPortrait(wOpponentPortrait, 7u, 3u);
	PlaySong(wMatchStartTheme);
	(void)FlashWhiteScreen();
	DoFrameIfLCDEnabled();
	(void)SetCursorParametersForTextBox(18u, 17u, 0x2Fu, 0x1Du);
	(void)WaitForButtonAorB();
	WaitForSongToFinish();
	FadeScreenToWhite();

	wd291 = saved_d291;
	return (DuelInitResult){saved_d291, f};
}
/* <<< factory Duel_Init */
