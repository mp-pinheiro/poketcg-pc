#include "home/gift_center.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define CONSOLE_CGB 0x02u
#define NORTH 0x00u
/* <<< factory statics */

/* >>> factory Preload_GiftCenterClerk */
PreloadGiftCenterClerkResult Preload_GiftCenterClerk(void)
{
	uint8_t console = gb_read8(wConsole_ADDR);

	if (console == CONSOLE_CGB)
		return (PreloadGiftCenterClerkResult){console, 0x90u};

	gb_write8(wLoadNPCDirection_ADDR, NORTH);
	return (PreloadGiftCenterClerkResult){NORTH, 0x10u};
}
/* <<< factory Preload_GiftCenterClerk */
