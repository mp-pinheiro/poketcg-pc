#include "home/tiles.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/copy.h"
#include "home/menus.h"
#include "home/random.h"
#include "home/switch_rom.h"
#include "mem.h"
#include "ppu.h"

static uint16_t bg_map0_address(uint16_t xy)
{
	uint8_t x = (uint8_t)(xy >> 8);
	uint8_t y = (uint8_t)xy;
	return (uint16_t)(0x9800u + (uint16_t)y * TILEMAP_W + x);
}

void FillRectangle(uint8_t a, uint8_t b, uint8_t c, uint16_t de, uint16_t hl)
{
	uint16_t dst = bg_map0_address(de);
	uint8_t row_tile = a;
	uint32_t rows = c ? c : 0x100;
	uint32_t cols = b ? b : 0x100;
	uint8_t col_step = (uint8_t)(hl >> 8);
	uint8_t row_step = (uint8_t)hl;

	do {
		uint8_t tile = row_tile;
		uint16_t pos = dst;
		uint32_t n = cols;

		do {
			gb_write8(pos++, tile);
			tile = (uint8_t)(tile + col_step);
		} while (--n);
		dst = (uint16_t)(dst + TILEMAP_W);
		row_tile = (uint8_t)(row_tile + row_step);
	} while (--rows);
}

void Copy1bppTiles(uint16_t *hl, uint16_t *de)
{
	uint16_t src = *de;
	uint16_t dst = *hl;
	uint32_t n = 128u * 8u;

	do {
		uint8_t value = gb_read8(src++);
		gb_write8(dst++, value);
		gb_write8(dst++, value);
	} while (--n);

	*de = src;
	*hl = dst;
}

#define BANK_FONTS 0x1du
#define TILE_SIZE 16u
#define CONSOLE_CGB 0x02u

#define V0_TILES0 0x8000u
#define V0_TILES1 0x8800u
#define V0_TILES2 0x9000u
#define S_GFX_BUFFER1 0xA400u
#define S_GFX_BUFFER4 0xB000u

/* Bank:addr pairs below are taken directly from poketcg.sym; DuelOtherGraphics
 * and DuelBoxMessages live one bank past BANK_FONTS (0x1e), the rest share
 * BANK_FONTS (0x1d) with the far-pointer offset already subtracted, matching
 * how each caller in tiles.asm encodes them (see CopyFontsOrDuelGraphicsTiles). */
#define DUEL_OTHER_GFX 0x4008u
#define DUEL_BOX_MESSAGES 0x4318u
#define SYMBOLS_FONT_FAR 0x2968u
#define SYMBOLS_FONT_TILES 0x38u
#define DUEL_CARD_HEADER_GFX_FAR 0x2ce8u
#define DUEL_DMG_SGB_SYMBOL_GFX_FAR 0x2fe8u
#define DUEL_CGB_SYMBOL_GFX_FAR 0x37f8u
#define LOAD_CARD_SET2_TILES_TABLE 0x2085u
#define LOAD_FULL_WIDTH_FONT_TILES_SRC 0x1e60u

static uint16_t far_ptr_bank(uint16_t hl, uint8_t *bank)
{
	*bank = (uint8_t)(BANK_FONTS + ((hl >> 14) & 3u));
	return (uint16_t)((hl & 0x3FFFu) | 0x4000u);
}

void CopyFontsOrDuelGraphicsTiles(uint16_t *hl, uint16_t *de, uint8_t b)
{
	uint8_t bank;
	uint16_t src = far_ptr_bank(*hl, &bank);
	uint8_t saved = hBankROM;

	BankswitchROM(bank);
	CopyGfxData(&src, de, b, TILE_SIZE);
	BankswitchROM(saved);
	*hl = src;
}

TileCopyResult LoadSymbolsFont(void)
{
	uint16_t hl = SYMBOLS_FONT_FAR;
	uint16_t de = V0_TILES2;

	CopyFontsOrDuelGraphicsTiles(&hl, &de, SYMBOLS_FONT_TILES);
	return (TileCopyResult){hl, de};
}

static const uint8_t kCardSet2TileOffsets[8] = {
	0xFFu, 0x00u, 0x40u, 0xFFu, 0xFFu, 0xFFu, 0xFFu, 0x80u
};

TileCopyResult LoadCardSet2Tiles(uint8_t a)
{
	uint8_t idx = (uint8_t)(a & 7u);
	uint8_t off = kCardSet2TileOffsets[idx];
	uint16_t hl, de;

	if (off == 0xFFu)
		return (TileCopyResult){(uint16_t)(LOAD_CARD_SET2_TILES_TABLE + idx), idx};

	hl = (uint16_t)(DUEL_OTHER_GFX + 0x1D0u + off);
	de = (uint16_t)(V0_TILES1 + 0x7C0u);
	CopyFontsOrDuelGraphicsTiles(&hl, &de, 4u);
	return (TileCopyResult){hl, de};
}

TileCopyResult LoadDuelDrawCardsScreenTiles(void)
{
	uint16_t hl = (uint16_t)(DUEL_OTHER_GFX + 0x290u);
	uint16_t de = (uint16_t)(V0_TILES1 + 0x740u);

	CopyFontsOrDuelGraphicsTiles(&hl, &de, 8u);
	return (TileCopyResult){hl, de};
}

TileCopyResult LoadCardOrDuelMenuBorderTiles(void)
{
	uint16_t hl = (uint16_t)(DUEL_OTHER_GFX + 0x150u);
	uint16_t de = (uint16_t)(V0_TILES1 + 0x500u);

	CopyFontsOrDuelGraphicsTiles(&hl, &de, 8u);
	return (TileCopyResult){hl, de};
}

TileCopyResult LoadCardTypeHeaderTiles(uint8_t a)
{
	uint16_t hl = (uint16_t)(DUEL_CARD_HEADER_GFX_FAR + ((uint16_t)a << 8));
	uint16_t de = (uint16_t)(V0_TILES1 + 0x600u);

	CopyFontsOrDuelGraphicsTiles(&hl, &de, 0x10u);
	return (TileCopyResult){hl, de};
}

TileCopyResult LoadDuelCardSymbolTiles(void)
{
	uint16_t hl = (uint16_t)(wConsole == CONSOLE_CGB
		? DUEL_CGB_SYMBOL_GFX_FAR : DUEL_DMG_SGB_SYMBOL_GFX_FAR);
	uint16_t de = (uint16_t)(V0_TILES1 + 0x500u);

	CopyFontsOrDuelGraphicsTiles(&hl, &de, 0x30u);
	return (TileCopyResult){hl, de};
}

TileCopyResult LoadDuelCardSymbolTiles2(void)
{
	uint16_t hl = (uint16_t)((wConsole == CONSOLE_CGB
		? DUEL_CGB_SYMBOL_GFX_FAR : DUEL_DMG_SGB_SYMBOL_GFX_FAR) + 0x40u);
	uint16_t de = (uint16_t)(V0_TILES1 + 0x540u);

	CopyFontsOrDuelGraphicsTiles(&hl, &de, 0x0Cu);
	return (TileCopyResult){hl, de};
}

static TileCopyResult load_duel_check_pokemon_tiles(uint8_t b)
{
	uint16_t hl = (uint16_t)((wConsole == CONSOLE_CGB
		? DUEL_CGB_SYMBOL_GFX_FAR : DUEL_DMG_SGB_SYMBOL_GFX_FAR) + 0x300u);
	uint16_t de = (uint16_t)(V0_TILES1 + 0x500u);

	CopyFontsOrDuelGraphicsTiles(&hl, &de, b);
	return (TileCopyResult){hl, de};
}

TileCopyResult LoadDuelFaceDownCardTiles(void)
{
	return load_duel_check_pokemon_tiles(0x10u);
}

TileCopyResult LoadDuelCheckPokemonScreenTiles(void)
{
	return load_duel_check_pokemon_tiles(0x24u);
}

static TileCopyResult load_deck_and_discard_pile_icons(void)
{
	uint16_t hl = (uint16_t)((wConsole == CONSOLE_CGB
		? DUEL_CGB_SYMBOL_GFX_FAR : DUEL_DMG_SGB_SYMBOL_GFX_FAR) + 0x540u);
	uint16_t de = (uint16_t)(V0_TILES1 + 0x500u);

	CopyFontsOrDuelGraphicsTiles(&hl, &de, 0x30u);
	return (TileCopyResult){hl, de};
}

TileCopyResult LoadDeckAndDiscardPileIcons(void)
{
	return load_deck_and_discard_pile_icons();
}

TileCopyResult LoadPlacingThePrizesScreenTiles(void)
{
	uint16_t hl = DUEL_OTHER_GFX;
	uint16_t de = (uint16_t)(V0_TILES1 + 0x200u);

	CopyFontsOrDuelGraphicsTiles(&hl, &de, 0x0Du);
	return load_deck_and_discard_pile_icons();
}

TileCopyResult LoadDuelCoinTossResultTiles(void)
{
	uint16_t hl = (uint16_t)(DUEL_OTHER_GFX + 0xD0u);
	uint16_t de = (uint16_t)(V0_TILES2 + 0x300u);

	CopyFontsOrDuelGraphicsTiles(&hl, &de, 8u);
	return (TileCopyResult){hl, de};
}

TileCopyResult Func_212f(void)
{
	uint16_t hl = SYMBOLS_FONT_FAR;
	uint16_t de = S_GFX_BUFFER1;
	uint8_t id, offset;

	CopyFontsOrDuelGraphicsTiles(&hl, &de, 0x30u);

	hl = (uint16_t)(DUEL_OTHER_GFX + 0x150u);
	de = (uint16_t)(S_GFX_BUFFER1 + 0x300u);
	CopyFontsOrDuelGraphicsTiles(&hl, &de, 8u);

	id = GetCardSymbolData();
	offset = (uint8_t)(id - 0xD0u);
	hl = (uint16_t)(DUEL_DMG_SGB_SYMBOL_GFX_FAR + (uint16_t)offset * TILE_SIZE);
	de = (uint16_t)(S_GFX_BUFFER1 + 0x380u);
	CopyFontsOrDuelGraphicsTiles(&hl, &de, 4u);

	hl = DUEL_DMG_SGB_SYMBOL_GFX_FAR;
	de = (uint16_t)(S_GFX_BUFFER4 + 0x100u);
	CopyFontsOrDuelGraphicsTiles(&hl, &de, 0x30u);

	return (TileCopyResult){hl, de};
}

void DrawDuelBoxMessage(uint8_t a)
{
	uint16_t hl = HtimesL((uint16_t)((0xA0u << 8) | a));
	uint16_t de = (uint16_t)(V0_TILES1 + 0x200u);

	hl = (uint16_t)((uint16_t)(hl << 2) + DUEL_BOX_MESSAGES);
	CopyFontsOrDuelGraphicsTiles(&hl, &de, 40u);
	FillRectangle(0xA0u, 10u, 4u, 0x0504u, 0x010Au);
}

void LoadFullWidthFontTiles(void)
{
	uint8_t bank;
	uint16_t canonical = far_ptr_bank(LOAD_FULL_WIDTH_FONT_TILES_SRC, &bank);
	uint8_t saved = hBankROM;
	uint16_t src, dst;

	BankswitchROM(bank);

	src = canonical;
	dst = V0_TILES0;
	Copy1bppTiles(&dst, &src);

	src = canonical;
	dst = V0_TILES2;
	Copy1bppTiles(&dst, &src);

	dst = V0_TILES1;
	Copy1bppTiles(&dst, &src);

	BankswitchROM(saved);
}
