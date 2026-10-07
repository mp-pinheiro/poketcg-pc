/* >>> part includes */
#include "home/status.h"

#include "generated/text_ids.h"
#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/load_gfx.h"
#include "home/objects.h"
#include "home/process_text.h"
#include "home/print_text.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "generated/wram.h"
#include "home/print_stats.h"
#include "home/text_box.h"
#include "home/init_menu.h"
#include "home/labels.h"
#include "home/wait_keys.h"
#include "home/scripting.h"
/* <<< part includes_2 */
/* === part PAD_START */
/* >>> part OAM_X_OFS */
#define OAM_X_OFS 0x08u
/* <<< part OAM_X_OFS */
/* >>> part OAM_Y_OFS */
#define OAM_Y_OFS 0x10u
/* <<< part OAM_Y_OFS */
/* >>> part fire_medal_oam */
static const uint8_t fire_medal_oam[3] = {
	(uint8_t)(88u + OAM_X_OFS), 0x86u, 0x04u
};
/* <<< part fire_medal_oam */
/* >>> part water_medal_oam */
static const uint8_t water_medal_oam[3] = {
	(uint8_t)(128u + OAM_X_OFS), 0x89u, 0x03u
};
/* <<< part water_medal_oam */
/* >>> part show_oam_medal */
static void show_oam_medal(const uint8_t *data)
{
	uint8_t d = data[0];
	uint8_t c = data[1];
	uint8_t b = data[2];
	uint8_t e = (uint8_t)(80u + OAM_Y_OFS);
	for (uint8_t row = 0u; row < 3u; row++) {
		uint8_t x = d;
		for (uint8_t col = 0u; col < 3u; col++) {
			SetOneObjectAttributes(e, x, c, b);
			x = (uint8_t)(x + 8u);
			c = (uint8_t)(c + 1u);
		}
		e = (uint8_t)(e + 8u);
		c = (uint8_t)(c + 0x0du);
	}
}
/* <<< part show_oam_medal */
/* >>> part load_collected_medal_tilemaps */
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
/* <<< part load_collected_medal_tilemaps */
/* >>> factory _PauseMenu_Status */
void _PauseMenu_Status(void)
{
	uint8_t saved_d291 = wd291;
	InitMenuRegs init = InitMenuScreen();
	wMedalScreenYOffset = 0u;
	load_collected_medal_tilemaps();
	DrawRegularTextBox(&init.hl, 0u, 20u, 8u, 0u, 0u);
	(void)PrintLabels(StatusScreenLabels, 0u, 0u);
	DrawPauseMenuPlayerPortrait(1u, 1u); /* menus/status.asm:14, lb bc, 1, 1 */
	PrintAlbumProgress(12u, 4u);
	PrintPlayTime(13u, 6u);
	LoadOBPalette(PALETTE_118);
	uint8_t medal_flags = GetEventValue(EVENT_MEDAL_FLAGS);
	if ((medal_flags & (uint8_t)(1u << FIRE_MEDAL_F)) != 0u)
		show_oam_medal(fire_medal_oam);
	if ((medal_flags & (uint8_t)(1u << WATER_MEDAL_F)) != 0u)
		show_oam_medal(water_medal_oam);
	(void)FlashWhiteScreen();
	(void)WaitUntilKeysArePressed((uint8_t)(PAD_A | PAD_B | PAD_START));
	wd291 = saved_d291;
}
/* <<< factory _PauseMenu_Status */
