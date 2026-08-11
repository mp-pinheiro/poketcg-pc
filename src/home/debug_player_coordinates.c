#include "home/debug_player_coordinates.h"

#include "generated/wram.h"
#include "mem.h"

#define LCDC_WIN_ON 0x20u

void JumpSetWindowOff(void)
{
	gb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) & (uint8_t)~LCDC_WIN_ON));
}
