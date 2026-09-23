#include "widescreen.h"

#include "generated/wram.h"
#include "mem.h"
#include "ppu.h"

enum {
	IO_LCDC = 0x40,
	IO_SCX = 0x43,
};

static uint8_t wram(uint16_t address)
{
	return g_wram[address - 0xC000u];
}

WidescreenRect widescreen_rect(int extra)
{
	WidescreenRect rect = {0, SCREEN_W, 0};
	uint16_t frame_function = (uint16_t)(wram(wDoFrameFunction_ADDR) | wram(wDoFrameFunction_ADDR + 1u) << 8);

	if ((g_io[IO_LCDC] & 0x80u) && frame_function == WIDESCREEN_OVERWORLD_DO_FRAME &&
	    wram(wCurMap_ADDR) != WIDESCREEN_OVERWORLD_MAP) {
		int scx = g_io[IO_SCX];
		int map_right = wram(wBGMapWidth_ADDR) * 8 - scx;

		rect.room = 1;
		rect.x0 = -scx < -extra ? -extra : -scx;
		rect.x1 = map_right > SCREEN_W + extra ? SCREEN_W + extra : map_right;
		if (rect.x0 > 0)
			rect.x0 = 0;
		if (rect.x1 < SCREEN_W)
			rect.x1 = SCREEN_W;
	}
	return rect;
}

WidescreenRect widescreen_apply_viewport(uint16_t *fb, int extra)
{
	WidescreenRect rect = widescreen_rect(extra);
	int width = SCREEN_W + 2 * extra;

	if (!extra || !(g_io[IO_LCDC] & 0x80u))
		return rect;
	uint16_t fill = (uint16_t)((g_pal[0] | g_pal[1] << 8) & 0x7FFF);
	for (int ly = 0; ly < SCREEN_H; ly++) {
		uint16_t *row = fb + ly * width;
		for (int x = -extra; x < rect.x0; x++)
			row[x + extra] = fill;
		for (int x = rect.x1; x < SCREEN_W + extra; x++)
			row[x + extra] = fill;
	}
	return rect;
}
