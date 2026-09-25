#include "presentation.h"

#define PRESENTATION_RGB555(r, g, b) \
	((uint16_t)((r) | ((g) << 5) | ((b) << 10)))

static uint16_t sgb_frame_pixel(int x, int y)
{
	static const uint16_t palette[] = {
		PRESENTATION_RGB555(2u, 3u, 10u),
		PRESENTATION_RGB555(5u, 8u, 19u),
		PRESENTATION_RGB555(11u, 15u, 27u),
		PRESENTATION_RGB555(25u, 23u, 11u),
	};
	int edge = x < 8 || x >= PRESENTATION_SGB_WIDTH - 8 ||
	           y < 8 || y >= PRESENTATION_SGB_HEIGHT - 8;
	int band = (x / 8 + y / 8) & 1;
	if (edge)
		return palette[3];
	if (x < 40 || x >= PRESENTATION_SGB_WIDTH - 40 ||
	    y < 32 || y >= PRESENTATION_SGB_HEIGHT - 32)
		return palette[band ? 2 : 1];
	return palette[band ? 1 : 0];
}

void presentation_render(PresentationMode mode, uint16_t *output,
                         const uint16_t *game)
{
	if (!output || !game)
		return;
	if (mode != PRESENTATION_SGB_FRAME) {
		for (int y = 0; y < SCREEN_H; y++)
			for (int x = 0; x < SCREEN_W; x++)
				output[y * SCREEN_W + x] = game[y * SCREEN_W + x];
		return;
	}
	for (int y = 0; y < PRESENTATION_SGB_HEIGHT; y++)
		for (int x = 0; x < PRESENTATION_SGB_WIDTH; x++)
			output[y * PRESENTATION_SGB_WIDTH + x] = sgb_frame_pixel(x, y);
	for (int y = 0; y < SCREEN_H; y++)
		for (int x = 0; x < SCREEN_W; x++)
			output[(y + 40) * PRESENTATION_SGB_WIDTH + x + 48] =
				game[y * SCREEN_W + x];
}
