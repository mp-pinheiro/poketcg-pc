#include "home/config.h"

#include "home/bg_map.h"
#include "mem.h"
#include "generated/wram.h"

void DrawConfigMenuCursor(uint8_t a, uint8_t c)
{
	uint16_t hl;

	switch ((uint8_t)(c << 1)) {
	case 0:
		hl = wConfigMessageSpeedCursorPos_ADDR;
		break;
	case 2:
		hl = wConfigDuelAnimationCursorPos_ADDR;
		break;
	default:
		hl = wConfigExitSettingsCursorPos_ADDR;
		break;
	}

	uint8_t cursor = gb_read8(hl++);
	uint8_t b = gb_read8(hl++);
	uint8_t lookup = gb_read8((uint16_t)(((uint16_t)b << 8) | cursor));
	hl = (uint16_t)(hl + (uint8_t)(lookup << 1));
	b = gb_read8(hl++);
	c = gb_read8(hl);
	WriteByteToBGMap0(a, b, c);
}
