#include "home/load_gfx.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "generated/sram.h"
#include "home/bg_map.h"
#include "home/copy.h"
#include "home/decompress.h"
#include "home/empty_screen.h"
#include "home/map.h"
#include "home/memory.h"
#include "home/palettes.h"
#include "home/switch_rom.h"
#include "home/switch_sram.h"
#include "mem.h"

#define GFX_TABLE_POINTERS 0x4e5du
#define GFX_TABLE_TILEMAPS 0u
#define GFX_TABLE_TILESETS 2u
#define GFX_TABLE_SPRITES 4u
#define GFX_TABLE_PALETTES 8u
#define TILE_SIZE 16u

static void switch_vram(uint8_t bank)
{
	hBankVRAM = bank;
	gb_write8(0xff4fu, (uint8_t)(0xfeu | (bank & 1u)));
}

static uint16_t state16(uint16_t addr)
{
	return (uint16_t)(gb_read8(addr) | ((uint16_t)gb_read8((uint16_t)(addr + 1u)) << 8));
}

static void put16(uint16_t addr, uint16_t value)
{
	gb_write8(addr, (uint8_t)value);
	gb_write8((uint16_t)(addr + 1u), (uint8_t)(value >> 8));
}

void LoadTilemap_ToSRAM(uint8_t b, uint8_t c)
{
	wWriteBGMapToSRAM = 1;
	LoadTilemap(b, c);
}

void LoadTilemap_ToVRAM(uint8_t b, uint8_t c)
{
	wWriteBGMapToSRAM = 0;
	LoadTilemap(b, c);
}

void LoadTilemap(uint8_t b, uint8_t c)
{
	uint16_t de = BCCoordToBGMap0Address(b, c);
	put16(wVRAMPointer_ADDR, de);
	Func_803b9();
	wBGMapBank = wTempPointerBank;
	CopyBankedDataToDE(6u, wDecompressionBuffer_ADDR);
	wBGMapWidth = gb_read8(wDecompressionBuffer_ADDR);
	wBGMapHeight = gb_read8((uint16_t)(wDecompressionBuffer_ADDR + 1u));
	wBGMapPermissionDataPtr = gb_read8((uint16_t)(wDecompressionBuffer_ADDR + 2u));
	gb_write8(wBGMapPermissionDataPtr_ADDR + 1u,
		  gb_read8((uint16_t)(wDecompressionBuffer_ADDR + 3u)));
	wBGMapCGBMode = gb_read8((uint16_t)(wDecompressionBuffer_ADDR + 4u));
	LoadTilemap_InitAndDecompressBGMap();
}

void LoadTilemap_InitAndDecompressBGMap(void)
{
	uint16_t source = (uint16_t)(state16(wTempPointer_ADDR) + 5u);
	InitDataDecompression(source, (uint8_t)(wDecompressionSecondaryBuffer_ADDR >> 8));
	{
		uint16_t de = state16(wVRAMPointer_ADDR);
		LoadTilemap_Decompress(&de);
	}
}

void LoadTilemap_Decompress(uint16_t *de)
{
	uint8_t width = wBGMapWidth;
	uint8_t rows = wBGMapHeight;
	uint8_t row_width = (uint8_t)(width << (wBGMapCGBMode != 0));
	uint8_t row;
	wDecompressionRowWidth = row_width;
	for (row = 0; row < 0x40u; row++)
		gb_write8((uint16_t)(wDecompressionBuffer_ADDR + row), 0);
	for (row = 0;; row++) {
		uint16_t row_source = wDecompressionBuffer_ADDR;
		uint16_t row_dest = *de;
		DecompressDataFromBank((uint16_t)row_width, row_source);
		CopyBGDataToVRAMOrSRAM(&row_source, &row_dest, width);
		if (wConsole == 2u) {
			switch_vram(1);
			row_source = (uint16_t)(wDecompressionBuffer_ADDR + width);
			row_dest = *de;
			FuncEightZeroOneFourEight(row_source, width);
			CopyBGDataToVRAMOrSRAM(&row_source, &row_dest, width);
			switch_vram(0);
		}
		*de = (uint16_t)(*de + 32u);
		if ((uint8_t)(row + 1u) == rows)
			break;
	}
}

void FuncEightZeroOneFourEight(uint16_t hl, uint8_t b)
{
	uint8_t i;
	if (!wd291)
		return;
	if (wBGMapCGBMode) {
		for (i = 0; i < b; i++)
			gb_write8((uint16_t)(hl + i), (uint8_t)(gb_read8((uint16_t)(hl + i)) + wd291));
	} else {
		for (i = 0; i < b; i++)
			gb_write8((uint16_t)(hl + i), wd291);
	}
}

void CopyBGDataToVRAMOrSRAM(uint16_t *hl, uint16_t *de, uint8_t b)
{
	uint8_t saved = hBankSRAM;
	uint8_t i;
	if (!wWriteBGMapToSRAM) {
		SafeCopyDataHLtoDE(hl, de, b);
		return;
	}
	BankswitchSRAM(1);
	{
		uint16_t target = (uint16_t)(0xa000u + (*de - 0x9800u) + (hBankVRAM ? 0x400u : 0u));
		for (i = 0; i < b; i++) gb_write8((uint16_t)(target + i), gb_read8((uint16_t)(*hl + i)));
	}
	BankswitchSRAM(saved);
	DisableSRAM();
}

void SafelyCopyBGMapFromSRAMToVRAM(void)
{
	uint8_t saved = hBankSRAM;
	uint8_t row;
	BankswitchSRAM(1);
	for (row = 0; row < 32; row++) {
		uint16_t src = (uint16_t)(0xa000u + row * 32u);
		uint16_t dst = (uint16_t)(0x9800u + row * 32u);
		SafeCopyDataHLtoDE(&src, &dst, 0x20u);
		if (wConsole == 2u) {
			switch_vram(1);
			src = (uint16_t)(0xa400u + row * 32u);
			dst = (uint16_t)(0x9800u + row * 32u);
			SafeCopyDataHLtoDE(&src, &dst, 0x20u);
			switch_vram(0);
		}
	}
	BankswitchSRAM(saved);
	DisableSRAM();
}

void ClearSRAMBGMaps(void)
{
	uint8_t saved = hBankSRAM;
	BankswitchSRAM(1);
	FillMemoryWithA(0xa000u, 0x0800u, 0);
	BankswitchSRAM(saved);
	DisableSRAM();
}

MapDataPointerResult GetMapDataPointer(uint8_t a, uint8_t l)
{
	uint8_t saved = hBankROM;
	uint16_t base = (uint16_t)(GFX_TABLE_POINTERS + l);
	uint16_t table;
	uint16_t offset = (uint16_t)a * 4u;
	uint16_t result;
	uint8_t f;
	BankswitchROM(0x20);
	table = (uint16_t)(gb_read8(base) | ((uint16_t)gb_read8((uint16_t)(base + 1u)) << 8));
	BankswitchROM(saved);
	result = (uint16_t)(table + offset);
	f = (uint8_t)((offset < 0x100u ? 0x80u : 0u)
		| (((table & 0x0fffu) + (offset & 0x0fffu)) >= 0x1000u ? 0x20u : 0u)
		| (result < table ? 0x10u : 0u));
	return (MapDataPointerResult){result, f};
}

void LoadGraphicsPointerFromHL(uint16_t *hl)
{
	uint8_t saved = hBankROM;
	uint16_t p = *hl;
	BankswitchROM(0x20);
	wTempPointer = gb_read8(p++);
	gb_write8(wTempPointer_ADDR + 1u, gb_read8(p++));
	wTempPointerBank = (uint8_t)(gb_read8(p) + 0x20u);
	BankswitchROM(saved);
	*hl = (uint16_t)(p + 1u);
}

uint8_t LoadSpriteGfx(uint8_t a)
{
	uint8_t total;
	uint16_t hl = GetMapDataPointer(a, GFX_TABLE_SPRITES).hl;
	LoadGraphicsPointerFromHL(&hl);
	total = gb_read8(hl);
	wTotalNumTiles = total;
	wCurSpriteTileSize = TILE_SIZE;
	LoadGfxDataFromTempPointerToVRAMBank();
	return total;
}

void LoadGfxDataFromTempPointerToVRAMBank(void)
{
	GetTileOffsetPointerAndSwitchVRAM();
	LoadGfxDataFromTempPointer();
}

void LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2(void)
{
	GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2();
	LoadGfxDataFromTempPointer();
}

void LoadGfxDataFromTempPointer(void)
{
    uint16_t src = (uint16_t)(state16(wTempPointer_ADDR) + 2u);
    uint16_t dst = state16(wVRAMPointer_ADDR);
    CopyGfxDataFromTempBank(&src, &dst, wTotalNumTiles, wCurSpriteTileSize);
	switch_vram(0);
}

void GetTileOffsetPointerAndSwitchVRAM(void)
{
	uint8_t offset = wVRAMTileOffset;
	put16(wVRAMPointer_ADDR, (uint16_t)(0x8000u + ((uint16_t)offset << 4)));
	switch_vram((uint8_t)(wWhichVRAMBank & 1u));
}

void GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2(void)
{
	uint8_t saved = wVRAMTileOffset;
	wVRAMTileOffset ^= 0x80u;
	GetTileOffsetPointerAndSwitchVRAM();
	gb_write8(wVRAMPointer_ADDR + 1u, (uint8_t)(gb_read8(wVRAMPointer_ADDR + 1u) + 0x08u));
	wVRAMTileOffset = saved;
}

void LoadTilesetGfx(void)
{
	uint16_t hl = GetMapDataPointer(wCurTileset, GFX_TABLE_TILESETS).hl;
	LoadGraphicsPointerFromHL(&hl);
	LoadTilesetGfx_LoadTileGfx();
	switch_vram(0);
}

void Func_80238(void)
{
	uint16_t hl = GetMapDataPointer(wCurTileset, GFX_TABLE_TILESETS).hl;
	LoadGraphicsPointerFromHL(&hl);
	wTotalNumTiles = gb_read8(hl);
	wCurSpriteTileSize = TILE_SIZE;
	wWhichVRAMBank = 0;
	wVRAMTileOffset = 0x80;
	LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2();
}

void LoadTilesetGfx_LoadTileGfx(void)
{
	uint16_t hl = state16(wTempPointer_ADDR);
	uint8_t bank = wTempPointerBank;
	uint16_t total = (uint16_t)(GetFarByte(bank, hl)
			      | ((uint16_t)GetFarByte(bank, (uint16_t)(hl + 1u)) << 8));
	put16(wTotalNumTiles_ADDR, total);
	put16(wTempPointer_ADDR, (uint16_t)(hl + 2u));
	if (LoadTilesetGfx_CopyGfxData(0, 0).f & 0x80u)
		return;
	if (LoadTilesetGfx_CopyGfxData(0, 0x80u).f & 0x80u)
		return;
	if (wConsole != 2u)
		return;
	if (LoadTilesetGfx_CopyGfxData(1, 0).f & 0x80u)
		return;
	(void)LoadTilesetGfx_CopyGfxData(1, 0x80u);
}

LoadTilesetChunkResult LoadTilesetGfx_CopyGfxData(uint8_t b, uint8_t c)
{
	uint8_t current_bank = wWhichVRAMBank;
	uint8_t current_offset = wVRAMTileOffset;
	uint16_t remaining = state16(wTotalNumTiles_ADDR);
	uint8_t count;
	uint8_t next_offset;
	uint16_t destination;

	if (current_bank != b || (uint8_t)(current_offset ^ c) & 0x80u)
		return (LoadTilesetChunkResult){
			(uint8_t)remaining, remaining ? 0u : 0x80u
		};

	count = (uint8_t)(c + 0x80u - current_offset);
	if (remaining < 0x100u && (uint8_t)remaining < count)
		count = (uint8_t)remaining;
	put16(wTotalNumTiles_ADDR, (uint16_t)(remaining - count));

	GetTileOffsetPointerAndSwitchVRAM_Tiles0ToTiles2();
	destination = state16(wVRAMPointer_ADDR);
	{
		uint16_t source = state16(wTempPointer_ADDR);
		uint16_t copy_destination = destination;
		CopyGfxDataFromTempBank(&source, &copy_destination, count, TILE_SIZE);
		put16(wTempPointer_ADDR, source);
	}

	next_offset = (uint8_t)(current_offset + 0x80u);
	wVRAMTileOffset = (uint8_t)(next_offset & 0x80u);
	if (next_offset < 0x80u)
		wWhichVRAMBank = (uint8_t)(current_bank + 1u);

	remaining = state16(wTotalNumTiles_ADDR);
	return (LoadTilesetChunkResult){
		(uint8_t)remaining, remaining ? 0u : 0x80u
	};
}

void Func_803b9(void)
{
	uint16_t hl = GetMapDataPointer(wCurTilemap, GFX_TABLE_TILEMAPS).hl;
	LoadGraphicsPointerFromHL(&hl);
	wCurTileset = gb_read8(hl);
}

void LoadBGPalette(uint8_t a)
{
	LoadPaletteDataToBuffer(a);
	{
		uint8_t *p = wLoadedPalData_PTR;
		if (*p)
			SetBGP(p[1]);
		p += 2;
		if (*p)
			LoadPaletteDataFromHL((uint16_t)(wLoadedPalData_ADDR + 3u),
					      wWhichBGPalIndex, *p);
	}
}

void LoadPaletteDataFromHL(uint16_t hl, uint8_t b, uint8_t c)
{
	uint16_t dst;
	uint16_t n;
	if (b >= 24u || c >= 9u)
		return;
	dst = (uint16_t)(wBackgroundPalettesCGB_ADDR + (uint16_t)b * 8u);
	n = c ? (uint16_t)c * 8u : 0x100u;
	if (n == 0x100u) {
		uint16_t i;
		for (i = 0; i < n; i++)
			gb_write8((uint16_t)(dst + i), gb_read8((uint16_t)(hl + i)));
	} else {
		CopyDataHLtoDE(&hl, &dst, n);
	}
	FlushAllPalettes();
}

void LoadOBPalette(uint8_t a)
{
	LoadPaletteDataToBuffer(a);
	{
		uint8_t *p = wLoadedPalData_PTR;
		uint8_t count = *p++;
		if (count && wWhichOBP != 1u) {
			SetOBP0(*p++);
			count--;
		}
		if (count) {
			SetOBP1(*p++);
			count--;
		}
		if (count)
			p++;
		if (*p)
			LoadPaletteDataFromHL(
				(uint16_t)(p - wLoadedPalData_PTR + wLoadedPalData_ADDR),
				(uint8_t)(wWhichOBPalIndex | 8u), *p);
	}
}

void LoadPaletteDataToBuffer(uint8_t a)
{
	uint16_t hl = GetMapDataPointer(a, GFX_TABLE_PALETTES).hl;
	uint8_t size;
	uint16_t count;
	uint16_t de = wLoadedPalData_ADDR;
	uint8_t saved;
	LoadGraphicsPointerFromHL(&hl);
	size = gb_read8(hl++);
	count = (uint16_t)((size & 0x0fu) + 1u)
	      + (uint16_t)((size & 0xf0u) >> 1)
	      + 1u;
	saved = hBankROM;
	BankswitchROM(wTempPointerBank);
	CopyBankedDataToDE(count, de);
	BankswitchROM(saved);
}
