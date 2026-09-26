#include "presentation.h"

#include <stddef.h>

#define PRESENTATION_RGB555(r, g, b) \
	((uint16_t)((r) | ((g) << 5) | ((b) << 10)))
#define BORDER_TILES 0x0000u
#define BORDER_MAP 0x2000u
#define BORDER_PALETTES 0x2800u
#define GAME_X 48
#define GAME_Y 40

static uint16_t g_border[PRESENTATION_SGB_WIDTH * PRESENTATION_SGB_HEIGHT];
static int g_border_loaded;

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

static uint16_t border_color(const uint8_t *border, unsigned palette, unsigned color)
{
	unsigned index = color ? palette * 16u + color : 0u;
	const uint8_t *entry = border + BORDER_PALETTES + index * 2u;
	return (uint16_t)((entry[0] | entry[1] << 8) & 0x7FFFu);
}

void presentation_set_border(const uint8_t *border)
{
	g_border_loaded = border != NULL;
	if (!border)
		return;
	for (unsigned tile_y = 0; tile_y < 28u; tile_y++) {
		for (unsigned tile_x = 0; tile_x < 32u; tile_x++) {
			const uint8_t *cell = border + BORDER_MAP + (tile_y * 32u + tile_x) * 2u;
			unsigned entry = cell[0] | cell[1] << 8;
			unsigned palette = (entry >> 10) & 7u;
			palette = palette >= 4u ? palette - 4u : 0u;
			const uint8_t *tile = border + BORDER_TILES + (entry & 0xFFu) * 32u;
			for (unsigned y = 0; y < 8u; y++) {
				unsigned row = (entry & 0x8000u) ? 7u - y : y;
				unsigned p0 = tile[row * 2u], p1 = tile[row * 2u + 1u];
				unsigned p2 = tile[16u + row * 2u], p3 = tile[16u + row * 2u + 1u];
				for (unsigned x = 0; x < 8u; x++) {
					unsigned bit = (entry & 0x4000u) ? x : 7u - x;
					unsigned color = ((p0 >> bit) & 1u) | ((p1 >> bit) & 1u) << 1 |
						((p2 >> bit) & 1u) << 2 | ((p3 >> bit) & 1u) << 3;
					g_border[(tile_y * 8u + y) * PRESENTATION_SGB_WIDTH + tile_x * 8u + x] =
						border_color(border, palette, color);
				}
			}
		}
	}
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
			output[y * PRESENTATION_SGB_WIDTH + x] = g_border_loaded
				? g_border[y * PRESENTATION_SGB_WIDTH + x] : sgb_frame_pixel(x, y);
	for (int y = 0; y < SCREEN_H; y++)
		for (int x = 0; x < SCREEN_W; x++)
			output[(y + GAME_Y) * PRESENTATION_SGB_WIDTH + x + GAME_X] =
				game[y * SCREEN_W + x];
}
