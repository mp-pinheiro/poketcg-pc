#include "home/credits.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define R_STAT        0xFF41u
#define R_IE          0xFFFFu
#define STAT_LYC_MASK 0x40u
#define IE_STAT_MASK  0x02u

#define WX_OFS 0x07u
#define B_LCDC_OBJS 0x01u
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
