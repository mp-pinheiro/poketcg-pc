#include "home/scroll.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/copy.h"
#include "mem.h"


#define rLCDC 0xFF40u
#define rSTAT 0xFF41u
#define rLYC  0xFF45u
#define rWX   0xFF4Bu
#define rIE   0xFFFFu

#define LCDC_OBJS 0x02u
#define STAT_LYC  0x40u
#define IE_STAT   0x02u

/* BGScrollData, scroll.asm:112, read live from bank 0. */
#define BGSCROLL_DATA 0x3EF8u

void Func_3e44(void)
{
	uint8_t guard = gb_read8(wd657_ADDR);
	if (guard & 0x01)
		return;
	gb_write8(wd657_ADDR, (uint8_t)(guard | 0x01));

	uint8_t idx = gb_read8(wd658_ADDR);
	gb_write8(wd658_ADDR, (uint8_t)(idx + 1));

	uint8_t wx = gb_read8((uint16_t)(wd64b_ADDR + idx));
	gb_write8(rWX, wx);
	uint8_t lcdc = gb_read8(rLCDC);
	if (wx >= 0xa7)
		gb_write8(rLCDC, (uint8_t)(lcdc | LCDC_OBJS));
	else
		gb_write8(rLCDC, (uint8_t)(lcdc & (uint8_t)~LCDC_OBJS));

	uint8_t scroll = gb_read8((uint16_t)(wd651_ADDR + idx));
	if (scroll >= 0x8f) {
		if (gb_read8(wd665_ADDR) != 0) {
			uint16_t src = wd659_ADDR, dst = wd64b_ADDR;
			CopyDataHLtoDE(&src, &dst, 6);
			src = wd65f_ADDR;
			dst = wd651_ADDR;
			CopyDataHLtoDE(&src, &dst, 6);
		}
		gb_write8(wd665_ADDR, 0);
		gb_write8(wd658_ADDR, 0);
		scroll = 0;
	}
	gb_write8(rLYC, scroll);
	gb_write8(wd657_ADDR, (uint8_t)(guard & (uint8_t)~0x01u));
}

uint8_t GetNextBackgroundScroll(uint8_t a)
{
	uint8_t idx = (uint8_t)((a + gb_read8(wVBlankCounter_ADDR)) & 0x3f);
	uint8_t v = gb_read8((uint16_t)(BGSCROLL_DATA + idx));
	uint8_t mod = gb_read8(wBGScrollMod_ADDR);
	unsigned shifts = (mod == 1) ? 0 : (mod == 2) ? 1 : (mod == 3) ? 2 : 3;
	while (shifts--)
		v = (uint8_t)((v >> 1) | (v & 0x80)); /* sra a */
	return v;
}

void EnableInt_LYCoincidence(void)
{
	gb_write8(rSTAT, (uint8_t)(gb_read8(rSTAT) | STAT_LYC));
	gb_write8(rIE, (uint8_t)(gb_read8(rIE) | IE_STAT));
}

void DisableInt_LYCoincidence(void)
{
	gb_write8(rSTAT, (uint8_t)(gb_read8(rSTAT) & (uint8_t)~STAT_LYC));
	gb_write8(rIE, (uint8_t)(gb_read8(rIE) & (uint8_t)~IE_STAT));
}

void ApplyBackgroundScroll(void)
{
	DisableInt_LYCoincidence();
	gb_write8(rSTAT, (uint8_t)(gb_read8(rSTAT) & (uint8_t)~0x04u));
	if (gb_read8(wApplyBGScroll_ADDR) != 0)
		return;

	gb_write8(wApplyBGScroll_ADDR, 1);
	gb_write8(wNextScrollLY_ADDR, 0);
	while (gb_read8(0xFF44u) < 0x60u) {
		uint8_t target = gb_read8(wNextScrollLY_ADDR);
		while (gb_read8(0xFF44u) < target)
			;
		uint8_t scroll = GetNextBackgroundScroll(target);
		while (gb_read8(rSTAT) & 0x02u)
			;
		gb_write8(0xFF43u, scroll);
		gb_write8(wNextScrollLY_ADDR, (uint8_t)(gb_read8(0xFF44u) + 1u));
	}
	gb_write8(0xFF43u, 0);
	gb_write8(rLYC, 0);
	gb_write8(hSCX_ADDR, GetNextBackgroundScroll(0));
	gb_write8(wApplyBGScroll_ADDR, 0);
	EnableInt_LYCoincidence();
}
