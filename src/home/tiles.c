#include "home/tiles.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/copy.h"
#include "home/menus.h"
#include "home/random.h"
#include "home/switch_rom.h"
#include "mem.h"
#include "ppu.h"
/* >>> factory statics */
#include "home/bg_map.h"

#include "home/frames.h"
/* <<< factory statics */

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

/* >>> factory Func_2057 */
/* tiles.asm:200-211. Only reached by `jr` from Func_2051 (hl = sp+9) or
 * fallthrough from Func_2055 (hl = sp+8), both inside the not-yet-ported
 * Func_1f96 stack frame; `ld hl, sp+2` and `sp+6` there read two more bytes
 * of that same caller frame. In C the frame becomes explicit parameters --
 * frame_c (sp+2), frame_lo (sp+6), frame_hi (sp+7) -- that Func_1f96 will
 * pass from its own locals once it is ported. Returns the byte written,
 * which callers read back out of e. */
uint8_t Func_2057(uint16_t hl, uint8_t frame_c, uint8_t frame_lo, uint8_t frame_hi)
{
	uint8_t value = gb_read8(hl);
	uint8_t row = (uint8_t)(frame_c + frame_lo);

	HblankWriteByteToBGMap0(value, frame_hi, row);
	return value;
}
/* <<< factory Func_2057 */

/* >>> factory Func_2051 */
/* tiles.asm:192-194. `jr` tail call into Func_2057 with hl already set to
 * sp+9 -- an explicit stand-in for that not-yet-ported Func_1f96 local, same
 * convention as Func_2057's own frame_c/frame_lo/frame_hi (sp+2/sp+6/sp+7).
 * Once Func_1f96 is ported it passes its own locals for all four params. */
uint8_t Func_2051(uint16_t hl, uint8_t frame_c, uint8_t frame_lo, uint8_t frame_hi)
{
	return Func_2057(hl, frame_c, frame_lo, frame_hi);
}
/* <<< factory Func_2051 */

/* >>> factory Func_2055 */
/* tiles.asm:196-198. Falls through into Func_2057 with hl set to sp+8 --
 * same explicit-parameter convention as Func_2051/Func_2057: hl stands in
 * for the addressed Func_1f96 local, frame_c/frame_lo/frame_hi for its
 * sp+2/sp+6/sp+7 bytes, all forwarded unchanged. */
uint8_t Func_2055(uint16_t hl, uint8_t frame_c, uint8_t frame_lo, uint8_t frame_hi)
{
	return Func_2057(hl, frame_c, frame_lo, frame_hi);
}
/* <<< factory Func_2055 */

/* >>> factory Func_2046 */
/* tiles.asm:182-190. Falls through into the already-landed Func_2055 (bit 4
 * of the incremented counter clear) or Func_2051 (bit 4 set), which
 * themselves fall through into Func_2057 -- same explicit-parameter
 * convention as those three: counter_addr stands in for the not-yet-ported
 * Func_1f96 local at sp+3 (read-modify-write, incremented every call),
 * hl8 for the local at sp+8 (Func_2055's hl; Func_2051 wants sp+9, exactly
 * one byte further into the same not-yet-ported frame, so it is derived as
 * hl8+1 rather than taken as its own parameter), and frame_c/frame_lo/
 * frame_hi for sp+2/sp+6/sp+7, forwarded unchanged. Only every 16th call
 * (low nibble of the pre-increment counter is 0) reaches the write; real
 * callers discard every register Func_2046 leaves behind, so there is no
 * C return value. */
void Func_2046(uint16_t counter_addr, uint16_t hl8, uint8_t frame_c,
	uint8_t frame_lo, uint8_t frame_hi)
{
	uint8_t old = gb_read8(counter_addr);
	uint8_t new_val = (uint8_t)(old + 1u);

	gb_write8(counter_addr, new_val);
	if ((old & 0x0Fu) != 0u)
		return;
	if ((new_val & 0x10u) != 0u)
		Func_2051((uint16_t)(hl8 + 1u), frame_c, frame_lo, frame_hi);
	else
		Func_2055(hl8, frame_c, frame_lo, frame_hi);
}
/* <<< factory Func_2046 */

/* >>> factory Func_1f96 */
Func1f96Result Func_1f96(uint8_t a, uint8_t b, uint8_t c, uint16_t de, uint16_t hl)
{
	uint16_t table = de;
	uint8_t selected = a;
	uint8_t max = gb_read8(table);
	uint8_t frame_c = 0u;
	uint8_t frame_lo;
	uint8_t frame_hi;
	uint16_t raw_callback;
	uint16_t callback;
	uint8_t counter = 0u;

	(void)b;
	(void)c;
	(void)hl;
	frame_lo = gb_read8((uint16_t)(table + 3u));
	frame_hi = gb_read8((uint16_t)(table + 4u));
	frame_c = max;
	raw_callback = (uint16_t)(gb_read8((uint16_t)(table + 5u)) |
		((uint16_t)gb_read8((uint16_t)(table + 6u)) << 8));
	if (raw_callback != 0u)
		callback = (uint16_t)(raw_callback + (uint16_t)(table + 5u));
	else
		callback = 0u;

	for (;;) {
		uint8_t old_counter = counter;
		counter = (uint8_t)(counter + 1u);
		if ((old_counter & 0x0Fu) == 0u) {
			uint8_t value = (counter & 0x10u) != 0u
				? (uint8_t)(callback >> 8) : (uint8_t)callback;
			HblankWriteByteToBGMap0(value, frame_hi,
				(uint8_t)(frame_c + frame_lo));
		}

		DoFrame();
		{
			uint8_t keys = hKeysPressed;
			if ((keys & 0x09u) != 0u) {
				uint8_t value = (uint8_t)(callback >> 8);
				HblankWriteByteToBGMap0(value, frame_hi,
					(uint8_t)(frame_c + frame_lo));
				return (Func1f96Result){selected,
					selected == 0u ? 0x80u : 0x00u};
			}
			if ((keys & 0x06u) != 0u) {
				uint8_t value = (uint8_t)(callback >> 8);
				HblankWriteByteToBGMap0(value, frame_hi,
					(uint8_t)(frame_c + frame_lo));
				return (Func1f96Result){selected, 0x10u};
			}
			if ((keys & 0x40u) != 0u) {
				selected = (uint8_t)(selected - 1u);
				if ((selected & 0x80u) != 0u)
					selected = (uint8_t)(max - 1u);
				{
					uint8_t value = (uint8_t)(callback >> 8);
					HblankWriteByteToBGMap0(value, frame_hi,
						(uint8_t)(frame_c + frame_lo));
				}
			} else if ((keys & 0x80u) != 0u) {
				selected = (uint8_t)(selected + 1u);
				if (selected >= max)
					selected = 0u;
				{
					uint8_t value = (uint8_t)(callback >> 8);
					HblankWriteByteToBGMap0(value, frame_hi,
						(uint8_t)(frame_c + frame_lo));
				}
			}
		}
	}
}
/* <<< factory Func_1f96 */
