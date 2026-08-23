#include "home/print_stats.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/load_animation.h"

static const uint8_t kMedalCoordsAndTilemaps[24] = {
	 1u, 10u, 0x3eu,
	 6u, 10u, 0x3fu,
	11u, 10u, 0x40u,
	16u, 10u, 0x41u,
	 1u, 14u, 0x42u,
	 6u, 14u, 0x45u,
	11u, 14u, 0x44u,
	16u, 14u, 0x43u,
};
/* <<< factory statics */

/* >>> factory DrawPauseMenuPlayerPortrait */
void DrawPauseMenuPlayerPortrait(void)
{
	DrawPlayerPortrait();
}
/* <<< factory DrawPauseMenuPlayerPortrait */

/* >>> factory FlashReceivedMedal */
void FlashReceivedMedal(void)
{
	gb_write8(0xD291u, 0u);
	uint8_t which = wWhichMedal;
	uint8_t idx = (uint8_t)(which * 3u);
	uint8_t x = kMedalCoordsAndTilemaps[idx];
	uint8_t y = (uint8_t)(wMedalScreenYOffset + kMedalCoordsAndTilemaps[(uint8_t)(idx + 1u)]);
	uint8_t timer = wMedalDisplayTimer;
	if (timer & 0x10u) {
		uint16_t de = (uint16_t)(((uint16_t)x << 8) | y);
		FillRectangle(0u, 3u, 3u, de, 0u);
		return;
	}
	uint8_t tilemap = kMedalCoordsAndTilemaps[(uint8_t)(idx + 2u)];
	wCurTilemap = tilemap;
	LoadTilemap_ToVRAM(x, y);
}
/* <<< factory FlashReceivedMedal */
