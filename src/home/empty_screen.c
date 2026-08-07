#include "home/empty_screen.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "ppu.h"

static void fill_bg_maps(uint8_t value)
{
	uint32_t count = (uint32_t)TILEMAP_W * TILEMAP_H;
	uint16_t address = 0x9800u;

	while (count-- != 0)
		gb_write8(address++, value);
}

void EmptyScreen(void)
{
	hBankVRAM = 0;
	gb_write8(0xFF4Fu, 0x00u);
	fill_bg_maps(wTileMapFill);
	wDuelDisplayedScreen = 0;

	if (wConsole == 0x02u) {
		hBankVRAM = 1;
		gb_write8(0xFF4Fu, 0x01u);
		fill_bg_maps(0);
		hBankVRAM = 0;
		gb_write8(0xFF4Fu, 0x00u);
	}
}

uint16_t BCCoordToBGMap0Address(uint8_t b, uint8_t c)
{
	uint16_t offset = (uint16_t)((uint16_t)c * TILEMAP_W + b);

	return (uint16_t)(0x9800u + offset);
}
