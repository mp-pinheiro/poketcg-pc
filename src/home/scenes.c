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
