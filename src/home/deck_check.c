#include "home/deck_check.h"

#include "generated/wram.h"
#include "home/bg_map.h"
#include "home/random.h"
#include "home/sound.h"

#define SFX_CONFIRM 0x02u
#define SFX_CANCEL 0x03u

DrawCheckMenuCursorResult DrawCheckMenuCursor(uint8_t a)
{
	uint16_t product = HtimesL((uint16_t)((uint16_t)wCheckMenuCursorXPosition << 8 | 10u));
	uint8_t b = (uint8_t)(product + 1u);
	uint8_t c = (uint8_t)((uint8_t)(wCheckMenuCursorYPosition << 1) + 14u);

	WriteByteToBGMap0(a, b, c);
	return (DrawCheckMenuCursorResult){a, a, a == 0 ? 0x80u : 0};
}

void PlaySFXConfirmOrCancel(uint8_t a)
{
	uint8_t sfx_id = (uint8_t)(a + 1u) == 0 ? SFX_CANCEL : SFX_CONFIRM;
	PlaySFX(sfx_id);
}
