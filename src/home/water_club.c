#include "home/water_club.h"

#include "generated/wram.h"

/* water_club.asm:229-264. Preloads Amy when the player reaches (20, 6)
 * while an active game event is in progress. */
PreloadAmyResult Preload_Amy(void)
{
	wd3d0 = 0;
	uint8_t active = wActiveGameEvent;
	if (active == 0)
		return (PreloadAmyResult){0, 0x90u};
	uint8_t x = wPlayerXCoord;
	if (x != 0x14u)
		return (PreloadAmyResult){x, 0x10u};
	uint8_t y = wPlayerYCoord;
	if (y != 0x06u)
		return (PreloadAmyResult){y, 0x10u};
	wLoadNPCXPos = 0x14u;
	wd3d0 = 1;
	return (PreloadAmyResult){0x14u, 0x90u};
}
