#include "home/setup.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/palettes.h"
#include "mem.h"

#define rSCY 0xFF42u
#define rSCX 0xFF43u
#define rWY  0xFF4Au
#define rWX  0xFF4Bu
#define rWBK 0xFF70u
#define rBGP  0xFF47u
#define rOBP0 0xFF48u
#define rOBP1 0xFF49u

#define CONSOLE_DMG 0x00u
#define CONSOLE_CGB 0x02u
#define BOOTUP_A_CGB 0x11u

#define LCDC_BG_OBJ_WIN 0x47u /* LCDC_BG_ON | LCDC_OBJ_ON | LCDC_OBJ_16 | LCDC_WIN_9C00 */

#define V0TILES0 0x8000u
#define V0BGMAP0 0x9800u
#define BGMAP_SIZE 0x0400u          /* v0BGMap1 - v0BGMap0 == v1BGMap1 - v1BGMap0 */
#define TILE_AREA_SIZE 0x1800u      /* v0BGMap0 - v0Tiles0 */

#define PAL_SIZE 8u

/* poketcg.sym (bank 0, fixed for this disassembly): the two ROM addresses the
 * asm bakes into its self-modifying trampoline/copy code. */
#define NOOP_ADDR 0x0348u
#define INITIAL_PALETTE_ADDR 0x0399u

void NoOp(void)
{
}

DetectConsoleResult DetectConsole(uint8_t a)
{
	uint8_t console = (a == BOOTUP_A_CGB) ? CONSOLE_CGB : CONSOLE_DMG;

	gb_write8(wConsole_ADDR, console);
	if (console != CONSOLE_CGB)
		return (DetectConsoleResult){console, console};

	gb_write8(rWBK, 0x01u);
	/* SwitchToCGBDoubleSpeed deleted per Phase 1 (double_speed.asm); the
	 * timer rate-compensates instead of running the CPU at double speed. */
	return (DetectConsoleResult){0x01u, console};
}

SetupPalettesResult SetupPalettes(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	uint8_t a = 0xE4u; /* ldgbpal a, SHADE_WHITE, SHADE_LIGHT, SHADE_DARK, SHADE_BLACK */

	gb_write8(rBGP, a);
	gb_write8(wBGP_ADDR, a);
	gb_write8(rOBP0, a);
	gb_write8(rOBP1, a);
	gb_write8(wOBP0_ADDR, a);
	gb_write8(wOBP1_ADDR, a);
	gb_write8(wFlushPaletteFlags_ADDR, 0);

	if (gb_read8(wConsole_ADDR) != CONSOLE_CGB)
		return (SetupPalettesResult){b, c, d, e, 0xCABEu};

	uint16_t de = wBackgroundPalettesCGB_ADDR;
	for (uint8_t i = 16; i != 0; i--) {
		for (uint8_t j = 0; j < PAL_SIZE; j++)
			gb_write8(de++, gb_read8((uint16_t)(INITIAL_PALETTE_ADDR + j)));
	}
	FlushAllCGBPalettesResult r = FlushAllCGBPalettes();
	return (SetupPalettesResult){r.b, r.c, r.d, r.e, r.hl};
}

uint16_t FillTileMap(void)
{
	uint16_t hl = V0BGMAP0;
	uint16_t bc = BGMAP_SIZE;

	hBankVRAM = 0;
	gb_write8(0xFF4Fu, 0);
	do {
		gb_write8(hl++, gb_read8(wTileMapFill_ADDR));
	} while (--bc);

	if (gb_read8(wConsole_ADDR) != CONSOLE_CGB)
		return hl;

	hBankVRAM = 1;
	gb_write8(0xFF4Fu, 1);
	hl = V0BGMAP0; /* v1BGMap0 -- same CPU address, bank-1 window now selected */
	bc = BGMAP_SIZE;
	do {
		gb_write8(hl++, 0);
	} while (--bc);
	hBankVRAM = 0;
	gb_write8(0xFF4Fu, 0);
	return hl;
}

static uint16_t clear_tiles(void)
{
	uint16_t hl = V0TILES0;
	uint16_t bc = TILE_AREA_SIZE;

	do {
		gb_write8(hl++, 0);
	} while (--bc);
	return hl;
}

uint16_t SetupVRAM(void)
{
	FillTileMap();

	if (gb_read8(wConsole_ADDR) == CONSOLE_CGB) {
		hBankVRAM = 1;
		gb_write8(0xFF4Fu, 1);
		clear_tiles();
		hBankVRAM = 0;
		gb_write8(0xFF4Fu, 0);
	}
	return clear_tiles();
}

uint16_t SetupRegisters(void)
{
	gb_write8(rSCY, 0);
	gb_write8(rSCX, 0);
	gb_write8(rWY, 0);
	gb_write8(rWX, 0);
	gb_write8(wcab0_ADDR, 0);
	gb_write8(wcab1_ADDR, 0);
	gb_write8(wcab2_ADDR, 0);
	gb_write8(hSCX_ADDR, 0);
	gb_write8(hSCY_ADDR, 0);
	gb_write8(hWX_ADDR, 0);
	gb_write8(hWY_ADDR, 0);
	gb_write8(wReentrancyFlag_ADDR, 0);
	gb_write8(wLCDCFunctionTrampoline_ADDR, 0xC3u);
	gb_write8(wVBlankFunctionTrampoline_ADDR, 0xC3u);

	uint16_t hl = (uint16_t)(wVBlankFunctionTrampoline_ADDR + 1);
	gb_write8(hl, (uint8_t)(NOOP_ADDR & 0xFFu));
	hl++;
	gb_write8(hl, (uint8_t)(NOOP_ADDR >> 8));

	gb_write8(wLCDC_ADDR, LCDC_BG_OBJ_WIN);
	gb_write8(0x6000u, 0x01u); /* rRTCLATCH: MBC5 has no RTC on this cart, no-op */
	gb_write8(0x0000u, 0x0Au); /* RAMG_SRAM_ENABLE */
	return hl;
}

ZeroRAMResult ZeroRAM(void)
{
	uint16_t hl = 0xC000u;
	uint16_t bc = 0x2000u; /* SIZEOF(WRAM0) */

	do {
		gb_write8(hl++, 0);
	} while (--bc);

	uint8_t c = 0x80u; /* LOW(STARTOF("HRAM")) */
	uint8_t b = 0x70u; /* SIZEOF("HRAM") -- the section stops at $FFEF, not $FFFF */
	uint8_t a = 0;

	do {
		gb_write8((uint16_t)(0xFF00u + c), a);
		c++;
	} while (--b);

	return (ZeroRAMResult){a, b, c, hl};
}
