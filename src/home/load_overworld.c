#include "home/load_overworld.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/load_gfx.h"
#include "home/load_map_header.h"
#include "generated/wram.h"
/* <<< factory statics */

/* >>> factory LoadMapTilesAndPals */
void LoadMapTilesAndPals(void)
{
	LoadMapHeader();
	/* SetSGB2AndSGB3MapPalette: SGB path, dropped by Phase 1 (port-contract.md Reason 1) */
	LoadTilemap_ToSRAM(0u, 0u);

	wVRAMTileOffset = 0x80u;
	wWhichVRAMBank = 0u;
	LoadTilesetGfx();

	wWhichOBP = 0u;
	wWhichBGPalIndex = wd291;
	LoadBGPalette(wCurMapInitialPalette);
	wWhichBGPalIndex = wd291;
	uint8_t pal = wCurMapPalette;
	if (pal != 0u)
		LoadBGPalette(pal);
}
/* <<< factory LoadMapTilesAndPals */
