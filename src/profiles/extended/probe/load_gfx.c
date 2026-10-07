/* === part includes */
/* >>> factory _DrawPortrait */
static void adapt__DrawPortrait(ProbeState *s)
{
	_DrawPortrait(s->b, s->c);
}
/* <<< factory _DrawPortrait */
/* --- factory Func_80238 */
/* --- part const */
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
