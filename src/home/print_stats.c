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

#include "home/print_stats.h"
#include "generated/wram.h"
#include "mem.h"
#define SYM_0 0x20u
#define SYM_SPACE 0x00u

#include "home/print_stats.h"
#include "home/empty_screen.h"
#include "home/bg_map.h"
#include "generated/wram.h"
#include "mem.h"
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

/* >>> factory ConvertWordToNumericalDigits */
static uint8_t get_number_symbol(uint16_t *hl, uint16_t bc, uint16_t *de)
{
	uint8_t a = (uint8_t)(SYM_0 - 1u);
	for (;;) {
		a = (uint8_t)(a + 1u);
		uint32_t sum = (uint32_t)*hl + bc;
		*hl = (uint16_t)sum;
		if (sum <= 0xFFFFu) break;
	}
	gb_write8(*de, a);
	*de = (uint16_t)(*de + 1u);
	*hl = (uint16_t)(*hl - bc);
	return a;
}

ConvertWordToNumericalDigitsResult ConvertWordToNumericalDigits(uint16_t hl)
{
	uint16_t de = wDecimalChars_ADDR;
	(void)get_number_symbol(&hl, 0xFF9Cu, &de);
	(void)get_number_symbol(&hl, 0xFFF6u, &de);
	uint8_t a = (uint8_t)((uint8_t)hl + SYM_0);
	gb_write8(de, a);
	hl = wDecimalChars_ADDR;
	uint8_t c = 2u;
	uint8_t f;
	for (;;) {
		a = gb_read8(hl);
		if (a != SYM_0) { f = 0x40u; break; }
		gb_write8(hl, SYM_SPACE);
		hl = (uint16_t)(hl + 1u);
		c = (uint8_t)(c - 1u);
		if (c == 0u) { f = 0xC0u; break; }
	}
	return (ConvertWordToNumericalDigitsResult){a, f, 0xFFu, c, (uint8_t)(de >> 8), (uint8_t)de, hl};
}
/* <<< factory ConvertWordToNumericalDigits */

/* >>> factory PrintAlbumProgress_SkipGetProgress */
void PrintAlbumProgress_SkipGetProgress(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	(void)ConvertWordToNumericalDigits((uint16_t)d);
	uint16_t dest1 = BCCoordToBGMap0Address(b, c);
	uint16_t src1 = wDecimalChars_ADDR;
	SafeCopyDataHLtoDE(&src1, &dest1, 3u);

	(void)ConvertWordToNumericalDigits((uint16_t)e);
	uint8_t b2 = (uint8_t)(b + 4u);
	uint16_t dest2 = BCCoordToBGMap0Address(b2, c);
	uint16_t src2 = wDecimalChars_ADDR;
	SafeCopyDataHLtoDE(&src2, &dest2, 3u);
}
/* <<< factory PrintAlbumProgress_SkipGetProgress */

/* >>> factory PrintPlayTime_SkipUpdateTime */
void PrintPlayTime_SkipUpdateTime(uint8_t b, uint8_t c)
{
	uint8_t lo = gb_read8((uint16_t)(wPlayTimeHourMinutes_ADDR + 1u));
	uint8_t hi = gb_read8((uint16_t)(wPlayTimeHourMinutes_ADDR + 2u));
	uint16_t hours = (uint16_t)(((uint16_t)hi << 8) | lo);
	(void)ConvertWordToNumericalDigits(hours);

	uint16_t dest1 = BCCoordToBGMap0Address(b, c);
	uint16_t src1 = wDecimalChars_ADDR;
	SafeCopyDataHLtoDE(&src1, &dest1, 3u);

	uint8_t minutes = gb_read8(wPlayTimeHourMinutes_ADDR);
	uint16_t sum = (uint16_t)((uint16_t)minutes + 100u);
	(void)ConvertWordToNumericalDigits(sum);

	uint8_t b2 = (uint8_t)(b + 4u);
	uint16_t dest2 = BCCoordToBGMap0Address(b2, c);
	uint16_t src2 = (uint16_t)(wDecimalChars_ADDR + 1u);
	SafeCopyDataHLtoDE(&src2, &dest2, 2u);
}
/* <<< factory PrintPlayTime_SkipUpdateTime */
