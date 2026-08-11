#include "home/deck_check.h"

#include "generated/wram.h"
#include "home/bg_map.h"
#include "home/random.h"
#include "home/sound.h"

#define SFX_CONFIRM 0x02u
#define SFX_CANCEL 0x03u

void DrawCheckMenuCursor(uint8_t a)
{
	uint16_t product = HtimesL((uint16_t)(10u << 8 | wCheckMenuCursorXPosition));
	uint8_t x = (uint8_t)(product + 1u);
	uint8_t y = (uint8_t)(wCheckMenuCursorYPosition * 2u + 14u);
	WriteByteToBGMap0(a, x, y);
}

void PlaySFXConfirmOrCancel(uint8_t a)
{
	if (a == 0xFFu)
		PlaySFX(SFX_CANCEL);
	else
		PlaySFX(SFX_CONFIRM);
}
