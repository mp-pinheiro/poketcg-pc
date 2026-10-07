/* >>> part includes */
#include "home/medal.h"
#include "home/frames.h"
#include "home/play_song.h"

#include "generated/text_ids.h"
#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "generated/wram.h"
#include "home/init_menu.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/music1.h"
#include "home/print_stats.h"
#include "home/print_text.h"
#include "home/sound.h"
#include "mem.h"
/* <<< part includes_2 */



/* >>> factory ShowMedalReceivedScreen */
/* MasterMedalNames' eight `tx` entries (medal.asm:52-62) resolved through
 * poketcg/src/text/text_offsets.asm:822-829. */
void ShowMedalReceivedScreen(uint8_t a)
{
	/* medal.asm:1-51. `sub $8` turns the caller's event id into the medal
	 * index. MasterMedalNames (medal.asm:52-62) is this file's own two-byte
	 * table, inlined here the way print_stats.c inlines the medal coordinate
	 * table it reads; the single callsite only ever passes the eight medal
	 * ids $08-$0F. */
	static const uint16_t master_medal_names[NUM_MEDALS] = {
		GrassClubMapName, ScienceClubMapName, FireClubMapName,
		WaterClubMapName, LightningClubMapName, PsychicClubMapName,
		RockClubMapName, FightingClubMapName,
	};
	uint8_t medal = (uint8_t)(a - 8u);
	uint8_t saved_d291 = wd291;
	uint16_t medal_name;

	wWhichMedal = medal;
	PauseSong();
	PlaySong(MUSIC_STOP);
	/* `farcall SetMainSGBBorder` (engine/sgb.asm:1-4) returns at its own first
	 * compare unless wConsole is CONSOLE_SGB, and the SGB path it guards only
	 * sends border packets over JOYP. That routine has no C body in this tree,
	 * so the DMG path is what is reproduced here. */
	DisableLCD();
	(void)InitMenuScreen();
	wMedalScreenYOffset = (uint8_t)-6;
	DrawCollectedMedals();
	medal_name = master_medal_names[medal];
	wTxRam2 = (uint8_t)medal_name;
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), (uint8_t)(medal_name >> 8));
	(void)FlashWhiteScreen();
	PlaySong(MUSIC_MEDAL);
	wMedalDisplayTimer = 0xFFu;
	do {
		do {
			DoFrameIfLCDEnabled();
			wMedalDisplayTimer = (uint8_t)(wMedalDisplayTimer + 1u);
		} while (wMedalDisplayTimer & 0x0Fu);
		FlashReceivedMedal();
	} while (wMedalDisplayTimer != 0xE0u);
	(void)PrintScrollableText_NoTextBoxLabel(WonTheMedalText);
	if (frame_boundary_is_installed())
		WaitForSongToFinish();
	else
		while (AssertSongFinished() != 0u)
			SoundTimerHandler();
	ResumeSong();
	wd291 = saved_d291;
}
/* <<< factory ShowMedalReceivedScreen */
