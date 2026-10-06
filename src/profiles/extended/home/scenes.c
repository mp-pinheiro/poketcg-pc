#include "home/scenes.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/decompress.h"
#include "home/empty_screen.h"
#include "home/load_gfx.h"
#include "home/palettes.h"
#include "home/map.h"
#include "home/memory.h"
#include "home/objects.h"
#include "home/switch_rom.h"
#include "home/sprite_animations.h"

#define GFX_TABLE_POINTERS_BANK 0x20u
#define GFX_TABLE_POINTERS_ADDR 0x4B5Du
#define GFXTABLE_PALETTES 0x08u
#define GFXTABLE_PORTRAITS 0x0Au
#define PORTRAIT_PLAYER 0u
#define PORTRAIT_SLOT_1 0xD0u
#define PORTRAIT_TILE_COUNT 36u
#define TILE_SIZE 16u
#define TILEMAP_WIDTH 32u
#define VRAM_BANK_REGISTER 0xFF4Fu
#define PORTRAIT_PAL_BASE 0x97u
#define SPRITE_BOOSTER_PACK_OAM 0x69u
#define SPRITE_ANIM_COORD_X 0x02u
static const uint8_t booster_logo_oam[] = {
	0x20u,
	0x00u, 0x00u, 0x00u, 0x00u,
	0x00u, 0x08u, 0x01u, 0x00u,
	0x00u, 0x10u, 0x02u, 0x00u,
	0x00u, 0x18u, 0x03u, 0x00u,
	0x00u, 0x20u, 0x04u, 0x00u,
	0x00u, 0x28u, 0x05u, 0x00u,
	0x00u, 0x30u, 0x06u, 0x00u,
	0x00u, 0x38u, 0x07u, 0x00u,
	0x08u, 0x00u, 0x10u, 0x00u,
	0x08u, 0x08u, 0x11u, 0x00u,
	0x08u, 0x10u, 0x12u, 0x00u,
	0x08u, 0x18u, 0x13u, 0x00u,
	0x08u, 0x20u, 0x14u, 0x00u,
	0x08u, 0x28u, 0x15u, 0x00u,
	0x08u, 0x30u, 0x16u, 0x00u,
	0x08u, 0x38u, 0x17u, 0x00u,
	0x10u, 0x00u, 0x08u, 0x00u,
	0x10u, 0x08u, 0x09u, 0x00u,
	0x10u, 0x10u, 0x0Au, 0x00u,
	0x10u, 0x18u, 0x0Bu, 0x00u,
	0x10u, 0x20u, 0x0Cu, 0x00u,
	0x10u, 0x28u, 0x0Du, 0x00u,
	0x10u, 0x30u, 0x0Eu, 0x00u,
	0x10u, 0x38u, 0x0Fu, 0x00u,
	0x18u, 0x00u, 0x18u, 0x00u,
	0x18u, 0x08u, 0x19u, 0x00u,
	0x18u, 0x10u, 0x1Au, 0x00u,
	0x18u, 0x18u, 0x1Bu, 0x00u,
	0x18u, 0x20u, 0x1Cu, 0x00u,
	0x18u, 0x28u, 0x1Du, 0x00u,
	0x18u, 0x30u, 0x1Eu, 0x00u,
	0x18u, 0x38u, 0x1Fu, 0x00u
};

static uint16_t extended_gfx_entry(uint8_t table, uint8_t index)
{
	uint8_t saved_bank = hBankROM;
	uint16_t table_ptr;

	BankswitchROM(GFX_TABLE_POINTERS_BANK);
	table_ptr = (uint16_t)(gb_read8((uint16_t)(GFX_TABLE_POINTERS_ADDR + table)) |
		((uint16_t)gb_read8((uint16_t)(GFX_TABLE_POINTERS_ADDR + table + 1u)) << 8));
	BankswitchROM(saved_bank);
	return (uint16_t)(table_ptr + (uint16_t)index * 4u);
}

static void load_extended_palette_data(uint8_t palette)
{
	uint8_t saved_bank = hBankROM;
	BankswitchROM(GFX_TABLE_POINTERS_BANK);
	uint16_t entry = extended_gfx_entry(GFXTABLE_PALETTES, palette);
	LoadGraphicsPointerFromHL(&entry);
	uint8_t count = gb_read8(entry);
	BankswitchROM(saved_bank);
	CopyBankedDataToDE((uint16_t)((uint16_t)count * 8u + 1u), wLoadedPalData_ADDR);
}

/* <<< factory statics */

/* >>> factory SetBoosterLogoOAM */
/* scenes.asm:135-181 */
void SetBoosterLogoOAM(void)
{
	uint8_t i;
	uint8_t count = booster_logo_oam[0];

	wWhichVRAMBank = 0u;
	wVRAMTileOffset = 0u;
	(void)LoadSpriteGfx(SPRITE_BOOSTER_PACK_OAM);
	ZeroObjectPositions();

	for (i = 0u; i < count; i++) {
		const uint8_t *entry = &booster_logo_oam[1u + (uint8_t)(i * 4u)];
		uint8_t e = (uint8_t)(wSceneBaseY - hSCY + entry[0]);
		uint8_t d = (uint8_t)(wSceneBaseX - hSCX + entry[1]);
		uint8_t c = (uint8_t)(wd61f + entry[2]);
		uint8_t b = entry[3];

		SetOneObjectAttributes(e, d, c, b);
	}

	wVBlankOAMCopyToggle = (uint8_t)(wVBlankOAMCopyToggle + 1u);
}
/* <<< factory SetBoosterLogoOAM */

/* >>> factory _DrawPortrait */
void _DrawPortrait(uint8_t b, uint8_t c)
{
	uint16_t entry = extended_gfx_entry(GFXTABLE_PORTRAITS, wCurPortrait);
	LoadGraphicsPointerFromHL(&entry);

	uint16_t source = (uint16_t)(wTempPointer |
		((uint16_t)gb_read8((uint16_t)(wTempPointer_ADDR + 1u)) << 8));
	uint8_t emotion = wPortraitEmotion;
	uint16_t emotion_offset = emotion == 0u ? 0u :
		(emotion == 1u ? 0x0240u : 0x0480u);
	source = (uint16_t)(source + emotion_offset);

	uint8_t swapped_slot = (uint8_t)((wPortraitSlot << 4) | (wPortraitSlot >> 4));
	uint16_t destination = (uint16_t)(((uint16_t)(swapped_slot | 0x80u)) << 8);
	CopyGfxDataFromTempBank(&source, &destination, PORTRAIT_TILE_COUNT, TILE_SIZE);

	uint16_t bg_map = BCCoordToBGMap0Address(b, c);
	uint16_t row = bg_map;
	uint8_t tile = wPortraitSlot;
	for (uint8_t y = 0u; y < 6u; y++) {
		for (uint8_t x = 0u; x < 6u; x++) {
			gb_write8((uint16_t)(row + x), tile++);
		}
		row = (uint16_t)(row + TILEMAP_WIDTH);
	}

	uint16_t attr_source = (uint16_t)(wTempPointer |
		((uint16_t)gb_read8((uint16_t)(wTempPointer_ADDR + 1u)) << 8));
	attr_source = (uint16_t)(attr_source +
		(wCurPortrait == PORTRAIT_PLAYER ? PORTRAIT_TILE_COUNT * TILE_SIZE :
			PORTRAIT_TILE_COUNT * 3u * TILE_SIZE));
	InitDataDecompression(attr_source, (uint8_t)(wDecompressionSecondaryBuffer_ADDR >> 8));
	wBGMapCGBMode = 1u;
	wd291 = wPortraitSlot == PORTRAIT_SLOT_1 ? 2u : 5u;
	for (uint8_t i = 0u; i <= emotion; i++)
		DecompressDataFromBank(PORTRAIT_TILE_COUNT, wDecompressionBuffer_ADDR);
	FuncEightZeroOneFourEight(wDecompressionBuffer_ADDR, PORTRAIT_TILE_COUNT);

	hBankVRAM = 1u;
	gb_write8(VRAM_BANK_REGISTER, 1u);
	row = bg_map;
	uint16_t source_attr = wDecompressionBuffer_ADDR;
	for (uint8_t y = 0u; y < 6u; y++) {
		for (uint8_t x = 0u; x < 6u; x++) {
			gb_write8((uint16_t)(row + x), (uint8_t)(gb_read8(source_attr++) + 1u));
		}
		row = (uint16_t)(row + TILEMAP_WIDTH);
	}
	hBankVRAM = 0u;
	gb_write8(VRAM_BANK_REGISTER, 0u);

	load_extended_palette_data((uint8_t)(PORTRAIT_PAL_BASE + wCurPortrait));
	LoadPaletteDataFromHL(wLoadedPalData_ADDR,
		wPortraitSlot == PORTRAIT_SLOT_1 ? 2u : 5u, 3u);
}
/* <<< factory _DrawPortrait */

/* >>> factory _LoadScene */
void _LoadScene(uint8_t a, uint8_t b, uint8_t c)
{
	uint8_t saved_tilemap = gb_read8(wCurTilemap_ADDR);
	uint8_t saved_d291 = gb_read8(wd291_ADDR);
	uint8_t base_x = (uint8_t)((uint8_t)(b << 3) + 0x08u);
	uint8_t base_y = (uint8_t)((uint8_t)(c << 3) + 0x10u);

	gb_write8(wSceneBaseX_ADDR, base_x);
	gb_write8(wSceneBaseY_ADDR, base_y);

	const uint8_t *ptr_entry = rom_ptr(4u,
		(uint16_t)(0x6B5Du + (uint16_t)a * 2u));
	uint16_t scene_ptr = (uint16_t)(ptr_entry[0] |
		((uint16_t)ptr_entry[1] << 8));
	const uint8_t *scene = rom_ptr(4u, scene_ptr);
	uint16_t index = 0u;

	uint8_t palette = scene[index++];
	wWhichOBP = 0u;
	wWhichBGPalIndex = scene[index];
	wd291 = scene[index++];
	LoadBGPalette(palette);

	wCurTilemap = scene[index++];
	LoadTilemap_ToVRAM(b, c);

	wVRAMTileOffset = scene[index++];
	wWhichVRAMBank = scene[index++];
	LoadTilesetGfx();

	for (;;) {
		uint8_t sprite = scene[index++];
		if (sprite == 0u)
			break;
		wSceneSprite = sprite;
		uint8_t sprite_palette = scene[index++];
		wWhichOBP = 0u;
		wWhichOBPalIndex = scene[index++];
		LoadOBPalette(sprite_palette);

		for (;;) {
			uint8_t animation = scene[index++];
			if (animation == 0u)
				break;
			wSceneSpriteAnimation = animation;
			(void)CreateSpriteAndAnimBufferEntry(wSceneSprite, 0u);
			wSceneSpriteIndex = wWhichSprite;
			uint16_t coords = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
			gb_write8(coords, (uint8_t)(wSceneBaseX + scene[index++]));
			gb_write8((uint16_t)(coords + 1u),
				(uint8_t)(wSceneBaseY + scene[index++]));
			if (wSceneSpriteAnimation != 0xFFu)
				StartSpriteAnimation(wSceneSpriteAnimation);
		}
	}

	wd291 = saved_d291;
	wCurTilemap = saved_tilemap;
}
/* <<< factory _LoadScene */

/* >>> factory LoadBoosterGfx */
uint8_t LoadBoosterGfx(uint8_t a, uint8_t b, uint8_t c)
{
	uint8_t saved_tilemap = wCurTilemap;
	_LoadScene(a, b, c);
	FlushAllPalettes();
	SetBoosterLogoOAM();
	wCurTilemap = saved_tilemap;
	return wCurTilemap;
}
/* <<< factory LoadBoosterGfx */
