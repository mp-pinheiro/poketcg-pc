/* >>> part includes */
#include "home/load_map_header.h"

#include "generated/wram.h"
#include "generated/rom.h"
#include "mem.h"
/* <<< part includes */
/* >>> part MAP_HEADERS_BANK */
#define MAP_HEADERS_BANK MapHeaders_BANK
/* <<< part MAP_HEADERS_BANK */
/* >>> part MAP_HEADER_SIZE */
#define MAP_HEADER_SIZE 4u
/* <<< part MAP_HEADER_SIZE */
/* >>> factory LoadMapHeader */
void LoadMapHeader(void)
{
	uint16_t entry = (uint16_t)(MAP_HEADERS +
		(uint16_t)gb_read8(wCurMap_ADDR) * MAP_HEADER_SIZE);
	const uint8_t *header = rom_ptr(MAP_HEADERS_BANK, entry);

	gb_write8(wCurTilemap_ADDR, header[0]);
	gb_write8(wCurMapInitialPalette_ADDR, header[1]);
	gb_write8(wCurMapPalette_ADDR, header[2]);
	gb_write8(wDefaultSong_ADDR, header[3]);
}
/* <<< factory LoadMapHeader */
