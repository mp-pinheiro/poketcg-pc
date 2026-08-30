#include "home/credits.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/credits_sequence_commands.h"
#include "home/masters_beaten_list.h"
#include "home/music1.h"
#include "home/play_song.h"
#include "home/wait_keys.h"
#include "home/lcd_enable_frame.h"
#include "home/sound.h"


/* >>> factory statics */
#define R_STAT        0xFF41u
#define R_IE          0xFFFFu
#define STAT_LYC_MASK 0x40u
#define IE_STAT_MASK  0x02u

#define WX_OFS 0x07u
#define B_LCDC_OBJS 0x01u

#include "home/tiles.h"

#include "home/lcd.h"
#include "home/load_animation.h"
#include "home/credits.h"
#include "home/init_menu.h"
#include "home/color.h"
#include "home/play_animation.h"
#include "generated/wram.h"
#include "mem.h"

#define R_LYC 0xFF45u
#define FUNC_3E31 0x3E31u
#define FUNC_3E44 0x3E44u
/* <<< factory statics */

/* >>> factory Func_1d758 */
/* credits.asm:79-86 */
void Func_1d758(void)
{
	gb_write8(R_STAT, (uint8_t)(gb_read8(R_STAT) & (uint8_t)~STAT_LYC_MASK));
	gb_write8(R_IE, (uint8_t)(gb_read8(R_IE) & (uint8_t)~IE_STAT_MASK));
}
/* <<< factory Func_1d758 */

/* >>> factory Func_1d765 */
/* credits.asm:88-224 */
uint8_t Func_1d765(void)
{
	uint16_t hl = wd659_ADDR;
	uint16_t de = wd65f_ADDR;
	uint8_t a;
	uint8_t c;

	hWY = 0x00u;

	if (gb_read8(wd648_ADDR) == 0x00u) {
		a = (uint8_t)(0xA0u + WX_OFS);
		hWX = a;
		gb_write8(hl, a);
		hl = (uint16_t)(hl + 1u);
		wLCDC = (uint8_t)(wLCDC | (uint8_t)(1u << B_LCDC_OBJS));
	} else {
		a = gb_read8(wd647_ADDR);
		if (a != 0x00u) {
			a = (uint8_t)(a - 1u);
			gb_write8(de, a);
			de = (uint16_t)(de + 1u);
			a = (uint8_t)(0xA0u + WX_OFS);
			hWX = a;
			gb_write8(hl, a);
			hl = (uint16_t)(hl + 1u);
			wLCDC = (uint8_t)(wLCDC | (uint8_t)(1u << B_LCDC_OBJS));
			a = 0x07u;
		} else {
			a = WX_OFS;
			hWX = a;
			wLCDC = (uint8_t)(wLCDC & (uint8_t)~(1u << B_LCDC_OBJS));
		}

		gb_write8(hl, a);
		hl = (uint16_t)(hl + 1u);

		c = (uint8_t)(gb_read8(wd647_ADDR) - 1u);
		c = (uint8_t)(gb_read8(wd648_ADDR) + c);
		a = (uint8_t)(gb_read8(wd649_ADDR) - 1u);

		if (a > c) {
			gb_write8(de, c);
			de = (uint16_t)(de + 1u);
			gb_write8(hl, 0xA7u);
			hl = (uint16_t)(hl + 1u);

			if (gb_read8(wd64a_ADDR) != 0x00u) {
				a = (uint8_t)(gb_read8(wd649_ADDR) - 1u);
				gb_write8(de, a);
				de = (uint16_t)(de + 1u);
				gb_write8(hl, 0x07u);
				hl = (uint16_t)(hl + 1u);
			}
		}

		c = (uint8_t)(gb_read8(wd649_ADDR) - 1u);
		a = (uint8_t)(gb_read8(wd64a_ADDR) + c);
		gb_write8(de, a);
		de = (uint16_t)(de + 1u);
		gb_write8(hl, 0xA7u);
		hl = (uint16_t)(hl + 1u);
	}

	gb_write8(de, 0xFFu);
	wd665 = 0x01u;
	return 0x01u;
}
/* <<< factory Func_1d765 */

/* >>> factory Func_1d7ee */
void Func_1d7ee(void)
{
	FillRectangle(0x00u, 20u, 18u, 0x0020u, 0x0000u);
}
/* <<< factory Func_1d7ee */

/* >>> factory Func_1d705 */
void Func_1d705(void)
{
	DisableLCD();
	LoadConsolePaletteData();
	EnableAndClearSpriteAnimations();
	(void)InitMenuScreen();
	Func_1d7ee();
	(void)SetDoFrameFunction(FUNC_3E31);

	wd647 = 0x91u;
	wd649 = 0x91u;
	wd648 = 0x01u;
	wd64a = 0x01u;
	Func_1d765();
	SetWindowOn();

	wd657 = 0x00u;
	gb_write8(wLCDCFunctionTrampoline_ADDR + 1u, (uint8_t)FUNC_3E44);
	gb_write8(wLCDCFunctionTrampoline_ADDR + 2u, (uint8_t)(FUNC_3E44 >> 8));
	gb_write8(R_STAT, (uint8_t)(gb_read8(R_STAT) | STAT_LYC_MASK));
	gb_write8(R_LYC, 0x00u);
	gb_write8(R_IE, (uint8_t)(gb_read8(R_IE) | IE_STAT_MASK));
}

/* <<< factory Func_1d705 */
/* >>> factory PlayCreditsSequence */
PlayCreditsSequenceResult PlayCreditsSequence(void)
{
	uint8_t f = 0u;
	gb_write8((uint16_t)(wOWMapEvents_ADDR + 1u), 0u);
	gb_write8(wCurSongID_ADDR, 0x12u);
	return (PlayCreditsSequenceResult){0u, f, 0u};
}
/* <<< factory PlayCreditsSequence */
