#ifndef POKETCG_HOME_LOAD_GFX_H
#define POKETCG_HOME_LOAD_GFX_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part LoadTilesetChunkResult */
typedef struct { uint8_t a, f; } LoadTilesetChunkResult;
/* <<< part LoadTilesetChunkResult */

/* >>> factory LoadTilemap_ToSRAM */
void LoadTilemap_ToSRAM(uint8_t b, uint8_t c);
/* <<< factory LoadTilemap_ToSRAM */
/* >>> factory LoadTilemap_ToVRAM */
void LoadTilemap_ToVRAM(uint8_t b, uint8_t c);
/* <<< factory LoadTilemap_ToVRAM */
/* >>> factory LoadTilemap */
void LoadTilemap(uint8_t b, uint8_t c);
/* <<< factory LoadTilemap */
/* >>> factory LoadTilemap_InitAndDecompressBGMap */
void LoadTilemap_InitAndDecompressBGMap(void);
/* <<< factory LoadTilemap_InitAndDecompressBGMap */
/* >>> factory LoadTilemap_Decompress */
void LoadTilemap_Decompress(uint16_t *de);
/* <<< factory LoadTilemap_Decompress */
/* >>> part FuncEightZeroOneFourEight */
void FuncEightZeroOneFourEight(uint16_t hl, uint8_t b);
/* <<< part FuncEightZeroOneFourEight */
/* >>> factory CopyBGDataToVRAMOrSRAM */
void CopyBGDataToVRAMOrSRAM(uint16_t *hl, uint16_t *de, uint8_t b);
/* <<< factory CopyBGDataToVRAMOrSRAM */
/* >>> factory SafelyCopyBGMapFromSRAMToVRAM */
void SafelyCopyBGMapFromSRAMToVRAM(void);
/* <<< factory SafelyCopyBGMapFromSRAMToVRAM */
/* >>> factory ClearSRAMBGMaps */
void ClearSRAMBGMaps(void);
/* <<< factory ClearSRAMBGMaps */
/* >>> part MapDataPointerResult */
typedef struct {
	uint16_t hl;
	uint8_t f;
} MapDataPointerResult;
/* <<< part MapDataPointerResult */
/* >>> factory GetMapDataPointer */
MapDataPointerResult GetMapDataPointer(uint8_t a, uint8_t l);
/* <<< factory GetMapDataPointer */
/* >>> factory LoadGraphicsPointerFromHL */
void LoadGraphicsPointerFromHL(uint16_t *hl);
/* <<< factory LoadGraphicsPointerFromHL */
/* >>> factory LoadSpriteGfx */
uint8_t LoadSpriteGfx(uint8_t a);
/* <<< factory LoadSpriteGfx */
/* >>> factory LoadGfxDataFromTempPointerToVRAMBank */
void LoadGfxDataFromTempPointerToVRAMBank(void);
/* <<< factory LoadGfxDataFromTempPointerToVRAMBank */
/* >>> part LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2 */
void LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2(void);
/* <<< part LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2 */
/* >>> factory LoadGfxDataFromTempPointer */
void LoadGfxDataFromTempPointer(void);
/* <<< factory LoadGfxDataFromTempPointer */
/* >>> factory GetTileOffsetPointerAndSwitchVRAM */
void GetTileOffsetPointerAndSwitchVRAM(void);
/* <<< factory GetTileOffsetPointerAndSwitchVRAM */
/* >>> factory GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2 */
void GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2(void);
/* <<< factory GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2 */
/* >>> factory LoadTilesetGfx */
void LoadTilesetGfx(void);
/* <<< factory LoadTilesetGfx */
/* >>> part Func_80238 */
void Func_80238(void);
/* <<< part Func_80238 */
/* >>> factory LoadTilesetGfx_LoadTileGfx */
void LoadTilesetGfx_LoadTileGfx(void);
/* <<< factory LoadTilesetGfx_LoadTileGfx */
/* >>> factory LoadTilesetGfx_CopyGfxData */
LoadTilesetChunkResult LoadTilesetGfx_CopyGfxData(uint8_t b, uint8_t c);
/* <<< factory LoadTilesetGfx_CopyGfxData */
/* >>> factory Func_803b9 */
void Func_803b9(void);
/* <<< factory Func_803b9 */
/* >>> factory LoadBGPalette */
void LoadBGPalette(uint8_t a);
/* <<< factory LoadBGPalette */
/* >>> factory LoadPaletteDataFromHL */
void LoadPaletteDataFromHL(uint16_t hl, uint8_t b, uint8_t c);
/* <<< factory LoadPaletteDataFromHL */
/* >>> factory LoadOBPalette */
void LoadOBPalette(uint8_t a);
/* <<< factory LoadOBPalette */
/* >>> factory LoadPaletteDataToBuffer */
void LoadPaletteDataToBuffer(uint8_t a);
/* <<< factory LoadPaletteDataToBuffer */
/* >>> factory _DrawPortrait */
void _DrawPortrait(uint8_t b, uint8_t c);
/* <<< factory _DrawPortrait */

#endif
