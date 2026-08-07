#include "home/lcd_enable_frame.h"

#include "home/frames.h"
#include "mem.h"

#define rLCDC 0xFF40u
#define LCDC_ON 0x80u

void DoFrameIfLCDEnabled(void)
{
	if (gb_read8(rLCDC) & LCDC_ON)
		DoFrame();
}
