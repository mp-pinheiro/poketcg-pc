#include "title_badge.h"

#include "ppu.h"

#define BADGE_WIDTH 53
#define BADGE_HEIGHT 13
#define BADGE_X 98
#define BADGE_Y 38
#define BADGE_TEXT 0x02DFu
#define BADGE_OUTLINE 0x0C00u
#define BADGE_PLATE 0x0011u
#define BADGE_SHADOW 0x0008u
#define TITLE_SIGNATURE_MATCHES 6

static const char *const kBadge[BADGE_HEIGHT] = {
	".ooooooooooooooooooooooooooooooooooooooooooooooooooo.",
	"ommmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmo",
	"ommmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmo",
	"omm#####m#mmm#m#####m#####m#mmm#m####mm#####m####mmmo",
	"omm#sssss#smm#sms#sss#sssss##mm#s#sss#m#sssss#sss#mmo",
	"omm#smmmmm#m#msmm#smm#smmmm##sm#s#smm#s#smmmm#smm#smo",
	"omm####mmmm#msmmm#smm####mm#s#m#s#smm#s####mm#smm#smo",
	"omm#ssssmm#m#mmmm#smm#ssssm#sm##s#smm#s#ssssm#smm#smo",
	"omm#smmmm#msm#mmm#smm#smmmm#sm##s#smm#s#smmmm#smm#smo",
	"omm#####m#smm#smm#smm#####m#smm#s####ms#####m####msmo",
	"ommmsssssmsmmmsmmmsmmmsssssmsmmmsmssssmmsssssmssssmmo",
	"ommmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmo",
	".ooooooooooooooooooooooooooooooooooooooooooooooooooo.",
};

static const struct {
	uint8_t y;
	uint8_t x;
	uint16_t color;
} kTitleSignature[] = {
	{74u, 30u, 0x6D40u}, {74u, 128u, 0x6D40u}, {88u, 30u, 0x0000u}, {88u, 128u, 0x0000u},
	{80u, 24u, 0x6D40u}, {80u, 135u, 0x6D40u}, {20u, 40u, 0x02DFu}, {45u, 110u, 0x639Cu},
};

int title_badge_title_visible(const uint16_t *framebuffer)
{
	int matches = 0;
	for (unsigned i = 0; i < sizeof kTitleSignature / sizeof kTitleSignature[0]; i++)
		matches += framebuffer[kTitleSignature[i].y * SCREEN_W + kTitleSignature[i].x] ==
			kTitleSignature[i].color;
	return matches >= TITLE_SIGNATURE_MATCHES;
}

static uint16_t badge_color(char pixel)
{
	switch (pixel) {
	case '#':
		return BADGE_TEXT;
	case 'o':
		return BADGE_OUTLINE;
	case 's':
		return BADGE_SHADOW;
	default:
		return BADGE_PLATE;
	}
}

void title_badge_draw(uint16_t *frame, int stride, int x_offset, const uint16_t *background)
{
	for (int y = 0; y < BADGE_HEIGHT; y++) {
		int game_y = BADGE_Y + y;
		uint16_t *row = frame + game_y * stride + x_offset;
		const uint16_t *bg_row = background + game_y * SCREEN_W;
		for (int x = 0; x < BADGE_WIDTH; x++) {
			int game_x = BADGE_X + x;
			if (kBadge[y][x] == '.' || row[game_x] != bg_row[game_x])
				continue;
			row[game_x] = badge_color(kBadge[y][x]);
		}
	}
}
