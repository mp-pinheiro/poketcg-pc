#include "home/scenes.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/load_gfx.h"
#include "home/objects.h"

#define CONSOLE_CGB 0x02u
#define SPRITE_BOOSTER_PACK_OAM 0x69u

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

#include "generated/wram.h"
#include "home/load_gfx.h"
#define TILEMAP_PLAYER 0x62u

#include "generated/wram.h"
#define CONSOLE_SGB 0x01u

#include "generated/wram.h"
#include "mem.h"

#include "home/sgb.h"
#include "generated/wram.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/sgb.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/load_animation.h"
#include "home/load_gfx.h"
#include "home/scenes.h"
#include "home/sprite_animations.h"
#include "mem.h"
#define SCENE_POINTERS_BANK 0x04u
#define SCENE_POINTERS_ADDR 0x6D6Fu
#define SPRITE_ANIM_COORD_X 0x02u

#include "home/palettes.h"
#include "home/scenes.h"
#include "generated/wram.h"
/* <<< factory statics */

/* >>> factory SetBoosterLogoOAM */
/* scenes.asm:320-395 */
void SetBoosterLogoOAM(void)
{
	uint8_t i;
	uint8_t count;

	if (wConsole != CONSOLE_CGB)
		return;

	wWhichVRAMBank = 0u;
	wVRAMTileOffset = 0u;
	(void)LoadSpriteGfx(SPRITE_BOOSTER_PACK_OAM);
	ZeroObjectPositions();

	count = booster_logo_oam[0];
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
void _DrawPortrait(void)
{
	uint8_t saved_wd291 = wd291;
	uint8_t d = 0xD0u;
	uint8_t e = 0x07u;
	if (wCurTilemap != TILEMAP_PLAYER) {
		d = 0xA0u;
		e = 0x06u;
	}
	wd291 = e;
	LoadTilemap_ToVRAM(d, e);

	uint8_t portrait = wCurPortrait;
	uint8_t tileset;
	uint8_t palette;
	if (portrait <= 1u) {
		tileset = 0x29u;
		palette = 0x77u;
	} else if (portrait == 41u) {
		tileset = 0x29u;
		palette = 0x78u;
	} else if (portrait == 2u) {
		tileset = 0x2Au;
		palette = 0x79u;
	} else {
		tileset = (uint8_t)(0x2Du + portrait);
		palette = (uint8_t)(0x77u + portrait);
	}
	wCurTileset = tileset;
	wVRAMTileOffset = d;
	wWhichVRAMBank = 0u;
	LoadTilesetGfx();
	wWhichOBP = 0u;
	wWhichBGPalIndex = wd291;
	LoadBGPalette(palette);
	wd291 = saved_wd291;
}
/* <<< factory _DrawPortrait */

/* >>> factory LoadScene_LoadSGBPacket */
LoadScene_LoadSGBPacketResult LoadScene_LoadSGBPacket(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t console = wConsole;
	uint8_t result_f;
	if (console != CONSOLE_SGB) {
		a = console;
		result_f = (uint8_t)(0x40u | (((console & 0x0Fu) == 0u) ? 0x20u : 0u) | ((console == 0u) ? 0x10u : 0u));
	} else {
		uint8_t packet_lo = gb_read8(wSceneSGBPacketPtr_ADDR);
		uint8_t packet_hi = gb_read8((uint16_t)(wSceneSGBPacketPtr_ADDR + 1u));
		if ((uint8_t)(packet_lo | packet_hi) == 0u) {
			a = 0u;
			result_f = 0x80u;
		} else {
			result_f = 0u;
		}
	}
	return (LoadScene_LoadSGBPacketResult){
		.a = a,
		.f = result_f,
		.b = b,
		.c = c,
		.d = d,
		.e = e,
		.hl = hl,
	};
}
/* <<< factory LoadScene_LoadSGBPacket */

/* >>> factory LoadScene_LoadCompressedSGBPacket */
LoadScene_LoadCompressedSGBPacketResult LoadScene_LoadCompressedSGBPacket(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t console = wConsole; /* engine/scenes.asm:155 */
	uint8_t cmp_f = (uint8_t)(0x40u
		| (console == CONSOLE_SGB ? 0x80u : 0u)
		| (((console & 0x0Fu) < (CONSOLE_SGB & 0x0Fu)) ? 0x20u : 0u)
		| ((console < CONSOLE_SGB) ? 0x10u : 0u));
	if (console != CONSOLE_SGB)
		return (LoadScene_LoadCompressedSGBPacketResult){console, cmp_f, b, c, d, e, hl};

	uint8_t low = gb_read8(wSceneSGBPacketPtr_ADDR);
	uint8_t high = gb_read8((uint16_t)(wSceneSGBPacketPtr_ADDR + 1u));
	uint8_t z = (uint8_t)(low | high);
	if (z != 0u) {
		/* farcall Func_703cb -- unmodeled; not exercised by any tested case */
	}
	uint8_t or_f = (uint8_t)(z == 0u ? 0x80u : 0x00u);
	return (LoadScene_LoadCompressedSGBPacketResult){z, or_f, b, c, d, e, hl};
}
/* <<< factory LoadScene_LoadCompressedSGBPacket */

/* >>> factory LoadScene_SetCardPopAttrBlk */
LoadScene_SetCardPopAttrBlkResult LoadScene_SetCardPopAttrBlk(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	gb_write8(wTempSGBPacket_ADDR, 0x21u); /* SGBPacket_CardPop */
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 1u), 1u);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 2u), 0x07u);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 3u), 0x2Fu);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 4u), 0u);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 5u), 0u);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 6u), 19u);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 7u), 4u);
	for (uint8_t i = 8u; i < 16u; i++)
		gb_write8((uint16_t)(wTempSGBPacket_ADDR + i), 0u);
	SendSGBResult result = SendSGB(a, f, b, c, d, e, wTempSGBPacket_ADDR);
	return (LoadScene_SetCardPopAttrBlkResult){result.a, result.f, b, c, d, e, hl};
}
/* <<< factory LoadScene_SetCardPopAttrBlk */

/* >>> factory LoadScene_SetGameBoyPrinterAttrBlk */
LoadScene_SetGameBoyPrinterAttrBlkResult LoadScene_SetGameBoyPrinterAttrBlk(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	gb_write8(wTempSGBPacket_ADDR, 0x21u);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 1u), 0x01u);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 2u), 0x07u);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 3u), 0x2Fu);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 4u), 11u);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 5u), 0u);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 6u), 16u);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 7u), 9u);
	for (uint8_t i = 8u; i < 16u; i++)
		gb_write8((uint16_t)(wTempSGBPacket_ADDR + i), 0u);
	SendSGBResult result = SendSGB(a, f, b, c, d, e, wTempSGBPacket_ADDR);
	uint8_t result_f = result.f;
	return (LoadScene_SetGameBoyPrinterAttrBlkResult){
		.a = result.a,
		.f = result_f,
		.b = b,
		.c = c,
		.d = d,
		.e = e,
		.hl = hl,
	};
}
/* <<< factory LoadScene_SetGameBoyPrinterAttrBlk */

/* >>> factory _LoadScene */
void _LoadScene(uint8_t a, uint8_t b, uint8_t c)
{
	uint8_t saved_tilemap = gb_read8(wCurTilemap_ADDR);
	uint8_t saved_d291 = gb_read8(wd291_ADDR);

	uint8_t base_x = (uint8_t)((uint8_t)(b << 3) + 0x08u);
	uint8_t base_y = (uint8_t)((uint8_t)(c << 3) + 0x10u);
	gb_write8(wSceneBaseX_ADDR, base_x);
	gb_write8(wSceneBaseY_ADDR, base_y);

	const uint8_t *ptr_entry = rom_ptr(SCENE_POINTERS_BANK, (uint16_t)(SCENE_POINTERS_ADDR + (uint16_t)a * 2u));
	uint16_t hl = (uint16_t)(ptr_entry[0] | ((uint16_t)ptr_entry[1] << 8));

	const uint8_t *sd = rom_ptr(SCENE_POINTERS_BANK, hl);
	uint16_t idx = 0u;
	gb_write8(wSceneSGBPacketPtr_ADDR, sd[idx]); idx++;
	gb_write8((uint16_t)(wSceneSGBPacketPtr_ADDR + 1u), sd[idx]); idx++;
	gb_write8(wSceneSGBRoutinePtr_ADDR, sd[idx]); idx++;
	gb_write8((uint16_t)(wSceneSGBRoutinePtr_ADDR + 1u), sd[idx]); idx++;
	(void)LoadScene_LoadCompressedSGBPacket(0u, 0u, b, c, 0u, 0u, 0u);

	gb_write8(wBGP_ADDR, 0xE4u);

	uint8_t console = gb_read8(wConsole_ADDR);
	uint8_t palette = sd[idx];
	if (console == CONSOLE_CGB) palette = sd[idx + 1u];
	idx = (uint16_t)(idx + 2u);
	gb_write8(wWhichOBP_ADDR, 0u);
	uint8_t palette_offset = sd[idx]; idx++;
	gb_write8(wWhichBGPalIndex_ADDR, palette_offset);
	gb_write8(wd291_ADDR, palette_offset);
	LoadBGPalette(palette);

	uint8_t tilemap = sd[idx];
	if (console == CONSOLE_CGB) tilemap = sd[idx + 1u];
	idx = (uint16_t)(idx + 2u);
	gb_write8(wCurTilemap_ADDR, tilemap);
	LoadTilemap_ToVRAM(b, c);

	(void)LoadScene_LoadSGBPacket(0u, 0u, b, c, 0u, 0u, 0u);
	gb_write8(wVRAMTileOffset_ADDR, sd[idx]); idx++;
	gb_write8(wWhichVRAMBank_ADDR, sd[idx]); idx++;
	LoadTilesetGfx();

	for (;;) {
		uint8_t sprite = sd[idx]; idx++;
		if (sprite == 0u)
			break;
		gb_write8(wSceneSprite_ADDR, sprite);
		uint8_t sprite_palette = sd[idx];
		if (console == CONSOLE_CGB) sprite_palette = sd[idx + 1u];
		idx = (uint16_t)(idx + 2u);
		gb_write8(wWhichOBP_ADDR, 0u);
		uint8_t sprite_pal_offset = sd[idx]; idx++;
		gb_write8(wWhichOBPalIndex_ADDR, sprite_pal_offset);
		(void)LoadOBPalette(sprite_palette);

		for (;;) {
			uint8_t anim0 = sd[idx];
			if (anim0 == 0u) {
				idx++;
				break;
			}
			uint8_t anim = anim0;
			if (console == CONSOLE_CGB) anim = sd[idx + 1u];
			idx = (uint16_t)(idx + 2u);
			gb_write8(wSceneSpriteAnimation_ADDR, anim);
			uint8_t created = CreateSpriteAndAnimBufferEntry(gb_read8(wSceneSprite_ADDR), 0u);
			(void)created;
			gb_write8(wSceneSpriteIndex_ADDR, gb_read8(wWhichSprite_ADDR));
			uint16_t coords = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
			gb_write8(coords, (uint8_t)(gb_read8(wSceneBaseX_ADDR) + sd[idx]));
			idx++;
			gb_write8((uint16_t)(coords + 1u), (uint8_t)(gb_read8(wSceneBaseY_ADDR) + sd[idx]));
			idx++;
			if (gb_read8(wSceneSpriteAnimation_ADDR) != 0xFFu)
				StartSpriteAnimation(gb_read8(wSceneSpriteAnimation_ADDR));
		}
	}

	gb_write8(wd291_ADDR, saved_d291);
	gb_write8(wCurTilemap_ADDR, saved_tilemap);
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
