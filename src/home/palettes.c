#include "home/palettes.h"

#include "generated/wram.h"
#include "mem.h"

#define rSTAT   0xFF41u
#define rBGP    0xFF47u
#define rOBP0   0xFF48u
#define rOBP1   0xFF49u

#define CONSOLE_CGB             0x02u
#define FLUSH_ONE_PAL           0x80u
#define FLUSH_ALL_PALS          0xC0u
#define PAL_SIZE                8u
#define NUM_BACKGROUND_PALETTES 8u
#define STAT_BUSY               0x02u

CopyCGBPalettesResult CopyCGBPalettes(uint8_t a, uint8_t b)
{
	uint8_t off = (uint8_t)(a * 8u);
	uint16_t hl = (uint16_t)(wBackgroundPalettesCGB_ADDR + off);
	uint8_t c = (uint8_t)((off & 0x40u) ? 0x6Au : 0x68u);
	uint8_t d = 0;
	uint8_t e = (uint8_t)(off & 0xBFu);
	uint8_t data = 0;

	do {
		gb_write8((uint16_t)(0xFF00u + c), e);
		c++;
		do {
			while (gb_read8(rSTAT) & STAT_BUSY)
				;
			data = gb_read8(hl);
			gb_write8((uint16_t)(0xFF00u + c), data);
			data = gb_read8((uint16_t)(0xFF00u + c));
		} while (data != gb_read8(hl));
		hl++;
		c--;
		e++;
	} while (--b);

	return (CopyCGBPalettesResult){data, b, c, d, e, hl};
}

/* Falls into FlushPalettesIfRequested.done in the asm, so clearing
 * wFlushPaletteFlags is this routine's own effect too, not just a caller's. */
FlushAllCGBPalettesResult FlushAllCGBPalettes(void)
{
	CopyCGBPalettes(0, (uint8_t)(8u * PAL_SIZE));
	CopyCGBPalettesResult r = CopyCGBPalettes(NUM_BACKGROUND_PALETTES, (uint8_t)(8u * PAL_SIZE));

	gb_write8(wFlushPaletteFlags_ADDR, 0);
	return (FlushAllCGBPalettesResult){r.b, r.c, r.d, r.e, r.hl};
}

void FlushPalettesIfRequested(void)
{
	uint8_t flags = gb_read8(wFlushPaletteFlags_ADDR);

	if (flags == 0)
		return;
	gb_write8(rBGP, gb_read8(wBGP_ADDR));
	gb_write8(rOBP0, gb_read8(wOBP0_ADDR));
	gb_write8(rOBP1, gb_read8(wOBP1_ADDR));
	if (gb_read8(wConsole_ADDR) == CONSOLE_CGB) {
		flags = gb_read8(wFlushPaletteFlags_ADDR);
		if (flags & FLUSH_ALL_PALS)
			FlushAllCGBPalettes();
		else
			CopyCGBPalettes(flags, PAL_SIZE);
	}
	gb_write8(wFlushPaletteFlags_ADDR, 0);
}

void FlushPalettes(uint8_t a)
{
	gb_write8(wFlushPaletteFlags_ADDR, a);
	if (gb_read8(wLCDC_ADDR) & 0x80u)
		return;
	FlushPalettesIfRequested();
}

void FlushPalette0(void)
{
	FlushPalettes(FLUSH_ONE_PAL);
}

void FlushAllPalettes(void)
{
	FlushPalettes(FLUSH_ALL_PALS);
}

void FlushPalette(uint8_t a)
{
	FlushPalettes((uint8_t)(a | FLUSH_ONE_PAL));
}

void SetBGP(uint8_t a)
{
	gb_write8(wBGP_ADDR, a);
	FlushPalette0();
}

void SetOBP0(uint8_t a)
{
	gb_write8(wOBP0_ADDR, a);
	FlushPalette0();
}

void SetOBP1(uint8_t a)
{
	gb_write8(wOBP1_ADDR, a);
	FlushPalette0();
}
