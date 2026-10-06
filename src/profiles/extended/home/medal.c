#include "home/medal.h"
#include "home/frames.h"
#include "home/play_song.h"

#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "home/init_menu.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/music.h"
#include "home/print_stats.h"
#include "home/print_text.h"
#include "home/sound.h"
#include "mem.h"
#include "home/load_gfx.h"
#include "home/process_text.h"
#include "home/text_box.h"

#define MUSIC_MEDAL 0x1du
#define MUSIC_STOP 0x00u
#define NUM_MEDALS 0x08u

#define WonTheMedalText 0x038bu
/* MasterMedalNames' eight `tx` entries (medal.asm:52-62) resolved through
 * poketcg/src/text/text_offsets.asm:822-829. */
#define FightingClubMapName 0x0332u
#define RockClubMapName 0x0333u
#define WaterClubMapName 0x0334u
#define LightningClubMapName 0x0335u
#define GrassClubMapName 0x0336u
#define PsychicClubMapName 0x0337u
#define ScienceClubMapName 0x0338u
#define FireClubMapName 0x0339u
#define PlayerStatusMedalsTitleText 0x0347u
#define PALETTE_118 0x36u
#define EVENT_MEDAL_FLAGS 0x10u

static void load_collected_medal_tilemaps(void)
{
	wd291 = 0u;
	uint16_t box = 0u;
	uint8_t d = 0u;
	uint8_t e = (uint8_t)(8u + wMedalScreenYOffset);
	DrawRegularTextBox(&box, 0u, 20u, 10u, d, e);
	d = 6u;
	e = (uint8_t)(9u + wMedalScreenYOffset);
	AdjustCoordinatesForBGScroll(&d, &e);
	InitTextPrinting(d, e);
	(void)PrintTextNoDelay(PlayerStatusMedalsTitleText, d, e);

	const uint8_t *table = rom_ptr(MedalCoordsAndTilemaps_BANK,
		MedalCoordsAndTilemaps_ADDR);
	uint8_t flags = GetEventValue(EVENT_MEDAL_FLAGS);
	if (flags == 0u)
		return;
	for (uint8_t index = 0u; index < NUM_MEDALS; index++) {
		if ((flags & 0x80u) != 0u) {
			uint8_t x = table[0];
			uint8_t y = (uint8_t)(wMedalScreenYOffset + table[1]);
			wCurTilemap = table[2];
			LoadTilemap_ToVRAM(x, y);
		}
		flags = (uint8_t)((flags << 1) | (flags >> 7));
		table += 3;
	}
	wVRAMTileOffset = 0x80u;
	wWhichVRAMBank = 0u;
	LoadTilesetGfx();
	wWhichOBP = 0u;
	wWhichBGPalIndex = 1u;
	LoadBGPalette(PALETTE_118);
}

/* <<< factory statics */

/* >>> factory ShowMedalReceivedScreen */
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
	load_collected_medal_tilemaps();
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
