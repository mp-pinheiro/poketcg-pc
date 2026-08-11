#ifndef POKETCG_HOME_LOAD_GFX_H
#define POKETCG_HOME_LOAD_GFX_H

#include <stdint.h>

typedef struct { uint8_t a, f; } LoadTilesetChunkResult;

void LoadTilemap_ToSRAM(uint8_t b, uint8_t c);
void LoadTilemap_ToVRAM(uint8_t b, uint8_t c);
void LoadTilemap(uint8_t b, uint8_t c);
void LoadTilemap_InitAndDecompressBGMap(void);
void LoadTilemap_Decompress(uint16_t *de);
void FuncEightZeroOneFourEight(uint16_t hl, uint8_t b);
void CopyBGDataToVRAMOrSRAM(uint16_t *hl, uint16_t *de, uint8_t b);
void SafelyCopyBGMapFromSRAMToVRAM(void);
void ClearSRAMBGMaps(void);
typedef struct {
	uint16_t hl;
	uint8_t f;
} MapDataPointerResult;
MapDataPointerResult GetMapDataPointer(uint8_t a, uint8_t l);
void LoadGraphicsPointerFromHL(uint16_t *hl);
void Func_80238(void);
uint8_t LoadSpriteGfx(uint8_t a);
void LoadGfxDataFromTempPointerToVRAMBank(void);
void LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2(void);
void LoadGfxDataFromTempPointer(void);
void GetTileOffsetPointerAndSwitchVRAM(void);
void GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2(void);
void LoadTilesetGfx(void);
void LoadTilesetGfx_LoadTileGfx(void);
LoadTilesetChunkResult LoadTilesetGfx_CopyGfxData(uint8_t b, uint8_t c);
void Func_803b9(void);
void LoadBGPalette(uint8_t a);
void LoadPaletteDataFromHL(uint16_t hl, uint8_t b, uint8_t c);
void LoadOBPalette(uint8_t a);
void LoadPaletteDataToBuffer(uint8_t a);

#endif
