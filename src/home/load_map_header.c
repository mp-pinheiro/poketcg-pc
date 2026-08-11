#include "home/load_map_header.h"

#include "generated/wram.h"
#include "mem.h"

#define MAP_HEADERS_BANK 7u
#define MAP_HEADERS 0x4374u
#define MAP_HEADER_SIZE 6u
#define CONSOLE_CGB 2u

void LoadMapHeader(void)
{
	uint16_t entry = (uint16_t)(MAP_HEADERS + (uint16_t)gb_read8(wCurMap_ADDR) * MAP_HEADER_SIZE);
	const uint8_t *header = rom_ptr(MAP_HEADERS_BANK, entry);
	uint8_t cgb_tilemap = header[1];

	gb_write8(wCurTilemap_ADDR, header[0]);
	gb_write8(wCurMapInitialPalette_ADDR, header[2]);
	gb_write8(wCurMapSGBPals_ADDR, header[3]);
	gb_write8(wCurMapPalette_ADDR, header[4]);
	gb_write8(wDefaultSong_ADDR, header[5]);
	if (gb_read8(wConsole_ADDR) == CONSOLE_CGB && cgb_tilemap != 0)
		gb_write8(wCurTilemap_ADDR, cgb_tilemap);
}
