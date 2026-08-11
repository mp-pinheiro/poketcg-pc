#include "home/config.h"

#include "generated/wram.h"

#include "home/bg_map.h"

void DrawConfigMenuCursor(uint8_t a, uint8_t c)
{
	uint8_t cursor;
	uint8_t x;
	uint8_t y;

	switch (c) {
	case 0:
		cursor = wConfigMessageSpeedCursorPos;
		x = (uint8_t)(5u + (uint8_t)(cursor << 1));
		y = 6;
		break;
	case 1:
		cursor = wConfigDuelAnimationCursorPos;
		if (cursor == 0)
			x = 1;
		else if (cursor == 1)
			x = 7;
		else
			x = 15;
		y = 12;
		break;
	default:
		cursor = wConfigExitSettingsCursorPos;
		x = 1;
		y = 16;
		break;
	}
	WriteByteToBGMap0(a, x, y);
}
