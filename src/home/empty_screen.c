#include "home/empty_screen.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/lcd.h"
#include "home/setup.h"
#include "home/sgb.h"
#include "mem.h"
#include "ppu.h"

/* empty_screen.asm:2-14. DisableLCD first: it is what turns wLCDC's enable
 * bit off, so every WriteByteToBGMap0 until the next EnableLCD takes the
 * direct path (no wTempByte staging) and DoFrameIfLCDEnabled skips its
 * DoFrame, as on the ROM. FillTileMap is the home routine, not a copy. */
#define CONSOLE_SGB 0x01u
#define ATTR_BLK_PACKET_EMPTY_SCREEN 0x04BFu
void EmptyScreen(void)
{
	DisableLCD();
	(void)FillTileMap();
	wDuelDisplayedScreen = 0;
	if (wConsole != CONSOLE_SGB)
		return;
	EnableLCD();
	(void)SendSGB(0u, 0u, 0u, 0u, 0u, 0u, ATTR_BLK_PACKET_EMPTY_SCREEN);
	DisableLCD();
}

uint16_t BCCoordToBGMap0Address(uint8_t b, uint8_t c)
{
	uint16_t offset = (uint16_t)((uint16_t)c * TILEMAP_W + b);

	return (uint16_t)(0x9800u + offset);
}
