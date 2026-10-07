/* >>> part includes */
#include "home/load_gfx.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */
/* >>> factory _DrawPortrait */
static void adapt__DrawPortrait(ProbeState *s)
{
	_DrawPortrait(s->b, s->c);
}
/* <<< factory _DrawPortrait */
/* >>> part const */
static void (*const load_gfx_target)(void) = Func_80238;
/* <<< part const */

/* >>> factory LoadTilemap_ToSRAM */
static void adapt_LoadTilemap_ToSRAM(ProbeState *s){ LoadTilemap_ToSRAM(s->b,s->c); }
/* <<< factory LoadTilemap_ToSRAM */
/* >>> factory LoadTilemap_ToVRAM */
static void adapt_LoadTilemap_ToVRAM(ProbeState *s){ LoadTilemap_ToVRAM(s->b,s->c); }
/* <<< factory LoadTilemap_ToVRAM */
/* >>> factory LoadTilemap */
static void adapt_LoadTilemap(ProbeState *s){ LoadTilemap(s->b,s->c); }
/* <<< factory LoadTilemap */
/* >>> factory LoadTilemap_InitAndDecompressBGMap */
static void adapt_LoadTilemap_InitAndDecompressBGMap(ProbeState *s){ (void)s; LoadTilemap_InitAndDecompressBGMap(); }
/* <<< factory LoadTilemap_InitAndDecompressBGMap */
/* >>> factory LoadTilemap_Decompress */
static void adapt_LoadTilemap_Decompress(ProbeState *s){ uint16_t de=(uint16_t)(s->d<<8|s->e); LoadTilemap_Decompress(&de); s->d=(uint8_t)(de>>8); s->e=(uint8_t)de; }
/* <<< factory LoadTilemap_Decompress */
/* >>> factory Func_80148 */
static void adapt_Func_80148(ProbeState *s){ FuncEightZeroOneFourEight(s->hl,s->b); }
/* <<< factory Func_80148 */
/* >>> factory CopyBGDataToVRAMOrSRAM */
static void adapt_CopyBGDataToVRAMOrSRAM(ProbeState *s){ uint16_t de=(uint16_t)(s->d<<8|s->e); CopyBGDataToVRAMOrSRAM(&s->hl,&de,s->b); s->d=(uint8_t)(de>>8); s->e=(uint8_t)de; }
/* <<< factory CopyBGDataToVRAMOrSRAM */
/* >>> factory SafelyCopyBGMapFromSRAMToVRAM */
static void adapt_SafelyCopyBGMapFromSRAMToVRAM(ProbeState *s){ (void)s; SafelyCopyBGMapFromSRAMToVRAM(); }
/* <<< factory SafelyCopyBGMapFromSRAMToVRAM */
/* >>> factory ClearSRAMBGMaps */
static void adapt_ClearSRAMBGMaps(ProbeState *s){ (void)s; ClearSRAMBGMaps(); }
/* <<< factory ClearSRAMBGMaps */
/* >>> factory GetMapDataPointer */
static void adapt_GetMapDataPointer(ProbeState *s){ MapDataPointerResult r=GetMapDataPointer(s->a,(uint8_t)s->hl); s->hl=r.hl; s->f=r.f; }
/* <<< factory GetMapDataPointer */
/* >>> factory LoadGraphicsPointerFromHL */
static void adapt_LoadGraphicsPointerFromHL(ProbeState *s){ LoadGraphicsPointerFromHL(&s->hl); }
/* <<< factory LoadGraphicsPointerFromHL */
/* >>> factory LoadSpriteGfx */
static void adapt_LoadSpriteGfx(ProbeState *s){ s->a=LoadSpriteGfx(s->a); }
/* <<< factory LoadSpriteGfx */
/* >>> factory LoadGfxDataFromTempPointerToVRAMBank */
static void adapt_LoadGfxDataFromTempPointerToVRAMBank(ProbeState *s){ (void)s; LoadGfxDataFromTempPointerToVRAMBank(); }
/* <<< factory LoadGfxDataFromTempPointerToVRAMBank */
/* >>> part LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2 */
static void adapt_LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2(ProbeState *s){ (void)s; LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2(); }
/* <<< part LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2 */
/* >>> factory LoadGfxDataFromTempPointer */
static void adapt_LoadGfxDataFromTempPointer(ProbeState *s){ (void)s; LoadGfxDataFromTempPointer(); }
/* <<< factory LoadGfxDataFromTempPointer */
/* >>> factory GetTileOffsetPointerAndSwitchVRAM */
static void adapt_GetTileOffsetPointerAndSwitchVRAM(ProbeState *s){ (void)s; GetTileOffsetPointerAndSwitchVRAM(); }
/* <<< factory GetTileOffsetPointerAndSwitchVRAM */
/* >>> factory GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2 */
static void adapt_GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2(ProbeState *s){ (void)s; GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2(); }
/* <<< factory GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2 */
/* >>> factory LoadTilesetGfx */
static void adapt_LoadTilesetGfx(ProbeState *s){ (void)s; LoadTilesetGfx(); }
/* <<< factory LoadTilesetGfx */
/* >>> part Func_80238 */
static void adapt_LoadGfxTarget(ProbeState *s){ (void)s; load_gfx_target(); }
/* <<< part Func_80238 */
/* >>> factory LoadTilesetGfx_LoadTileGfx */
static void adapt_LoadTilesetGfx_LoadTileGfx(ProbeState *s){ (void)s; LoadTilesetGfx_LoadTileGfx(); }
/* <<< factory LoadTilesetGfx_LoadTileGfx */
/* >>> factory LoadTilesetGfx_CopyGfxData */
static void adapt_LoadTilesetGfx_CopyGfxData(ProbeState *s){ LoadTilesetChunkResult r=LoadTilesetGfx_CopyGfxData(s->b,s->c); s->a=r.a; s->f=r.f; }
/* <<< factory LoadTilesetGfx_CopyGfxData */
/* >>> factory Func_803b9 */
static void adapt_Func_803b9(ProbeState *s){ (void)s; Func_803b9(); }
/* <<< factory Func_803b9 */
/* >>> factory LoadBGPalette */
static void adapt_LoadBGPalette(ProbeState *s){ LoadBGPalette(s->a); }
/* <<< factory LoadBGPalette */
/* >>> factory LoadPaletteDataFromHL */
static void adapt_LoadPaletteDataFromHL(ProbeState *s){ LoadPaletteDataFromHL(s->hl,s->b,s->c); }
/* <<< factory LoadPaletteDataFromHL */
/* >>> factory LoadOBPalette */
static void adapt_LoadOBPalette(ProbeState *s){ LoadOBPalette(s->a); }
/* <<< factory LoadOBPalette */
/* >>> factory LoadPaletteDataToBuffer */
static void adapt_LoadPaletteDataToBuffer(ProbeState *s){ LoadPaletteDataToBuffer(s->a); }
/* <<< factory LoadPaletteDataToBuffer */

/* >>> part probe_entries_load_gfx */
const ProbeEntry probe_entries_load_gfx[] = {
	{ "_DrawPortrait", adapt__DrawPortrait },
 {"LoadTilemap_ToSRAM",adapt_LoadTilemap_ToSRAM},{"LoadTilemap_ToVRAM",adapt_LoadTilemap_ToVRAM},{"LoadTilemap",adapt_LoadTilemap},
 {"LoadTilemap.InitAndDecompressBGMap",adapt_LoadTilemap_InitAndDecompressBGMap},{"LoadTilemap.Decompress",adapt_LoadTilemap_Decompress},
 {"Func_80148",adapt_Func_80148},{"CopyBGDataToVRAMOrSRAM",adapt_CopyBGDataToVRAMOrSRAM},
 {"SafelyCopyBGMapFromSRAMToVRAM",adapt_SafelyCopyBGMapFromSRAMToVRAM},{"ClearSRAMBGMaps",adapt_ClearSRAMBGMaps},
 {"GetMapDataPointer",adapt_GetMapDataPointer},{"LoadGraphicsPointerFromHL",adapt_LoadGraphicsPointerFromHL},{"LoadSpriteGfx",adapt_LoadSpriteGfx},
 {"LoadGfxDataFromTempPointerToVRAMBank",adapt_LoadGfxDataFromTempPointerToVRAMBank},
 {"LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2",adapt_LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2},
 {"LoadGfxDataFromTempPointer",adapt_LoadGfxDataFromTempPointer},{"GetTileOffsetPointerAndSwitchVRAM",adapt_GetTileOffsetPointerAndSwitchVRAM},
 {"GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2",adapt_GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2},{"LoadTilesetGfx",adapt_LoadTilesetGfx},
 {"Func_80238",adapt_LoadGfxTarget},
 {"LoadTilesetGfx.LoadTileGfx",adapt_LoadTilesetGfx_LoadTileGfx},{"LoadTilesetGfx.CopyGfxData",adapt_LoadTilesetGfx_CopyGfxData},
 {"Func_803b9",adapt_Func_803b9},{"LoadBGPalette",adapt_LoadBGPalette},{"LoadPaletteDataFromHL",adapt_LoadPaletteDataFromHL},
 {"LoadOBPalette",adapt_LoadOBPalette},{"LoadPaletteDataToBuffer",adapt_LoadPaletteDataToBuffer},{NULL,NULL}
};
/* <<< part probe_entries_load_gfx */
