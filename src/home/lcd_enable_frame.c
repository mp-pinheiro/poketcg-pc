/* >>> part includes */
#include "home/lcd_enable_frame.h"

#include "home/frames.h"
#include "mem.h"
/* <<< part includes */

/* >>> part rLCDC */
#define rLCDC 0xFF40u
#define LCDC_ON 0x80u
/* <<< part rLCDC */

/* >>> factory DoFrameIfLCDEnabled */
void DoFrameIfLCDEnabled(void)
{
	if (gb_read8(rLCDC) & LCDC_ON)
		DoFrame();
}
/* <<< factory DoFrameIfLCDEnabled */
