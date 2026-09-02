#include "home/setup.h"
#include "home/time.h"

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
	/* The reference runs the real CGB boot ROM; by the time Start hands off
	 * with a=$11 these registers hold bootrom leftovers (gbrt.c's
	 * post-boot model minus KEY1, whose raw byte the bootrom never writes).
	 * Applied once per process, here, so DMG probe worlds keep pristine io
	 * and a soft reset (which re-runs Start but never the bootrom) does not
	 * resurrect boot-era register values the game has since rewritten. */
	static int g_boot_io_applied;
	if (!g_boot_io_applied) {
		g_boot_io_applied = 1;
		g_io[0x00] = 0xCFu;  /* JOYP */
		g_io[0x02] = 0x7Fu;  /* SC */
		g_io[0x07] = 0xF8u;  /* TAC: timer disabled at boot */
		g_io[0x0F] = 0xE1u;  /* IF */
		g_io[0x10] = 0x80u;  /* NR10 */
		g_io[0x11] = 0xBFu;  /* NR11 */
		g_io[0x12] = 0xF3u;  /* NR12 */
		g_io[0x13] = 0xFFu;  /* NR13 */
		g_io[0x14] = 0xBFu;  /* NR14 */
		g_io[0x16] = 0x3Fu;  /* NR21 */
		g_io[0x17] = 0x00u;  /* NR22 */
		g_io[0x18] = 0xFFu;  /* NR23 */
		g_io[0x19] = 0xBFu;  /* NR24 */
		g_io[0x1A] = 0x7Fu;  /* NR30 */
		g_io[0x1B] = 0xFFu;  /* NR31 */
		g_io[0x1C] = 0x9Fu;  /* NR32 */
		g_io[0x1D] = 0xFFu;  /* NR33 */
		g_io[0x1E] = 0xBFu;  /* NR34 */
		g_io[0x20] = 0xFFu;  /* NR41 */
		g_io[0x24] = 0x77u;  /* NR50 */
		g_io[0x25] = 0xF3u;  /* NR51 */
		g_io[0x26] = 0xF1u;  /* NR52 */
		g_io[0x4F] = 0xFEu;  /* VBK */
		g_io[0x51] = 0xFFu;  /* HDMA1 */
		g_io[0x52] = 0xFFu;  /* HDMA2 */
		g_io[0x53] = 0xFFu;  /* HDMA3 */
		g_io[0x54] = 0xFFu;  /* HDMA4 */
		g_io[0x55] = 0xFFu;  /* HDMA5 */
		g_io[0x56] = 0x3Eu;  /* RP */
		g_io[0x68] = 0xC0u;  /* BGPI */
		g_io[0x6A] = 0xC0u;  /* OBPI */
		g_io[0x6C] = 0xFEu;  /* OPRI */
		g_io[0x70] = 0xF8u;  /* SVBK */
	}
	gb_write8(rWBK, 0x01u);
	/* setup.asm:51 -- on CGB the boot switches to double speed. The STOP
	 * itself is modeled by mem_cgb_speed_switch_stop (inside the switch);
	 * only the speed flag and KEY1/TMA state are observable in this port. */
	SwitchToCGBDoubleSpeed();
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
