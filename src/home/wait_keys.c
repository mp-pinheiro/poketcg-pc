/* >>> part includes */
#include "home/wait_keys.h"

#include "generated/hram.h"
#include "home/lcd_enable_frame.h"
#include "mem.h"
/* <<< part includes */

/* >>> factory WaitUntilKeysArePressed */
WaitKeysResult WaitUntilKeysArePressed(uint8_t keys)
{
	uint8_t pressed;

	for (;;) {
		DoFrameIfLCDEnabled();
		pressed = (uint8_t)(gb_read8(hKeysPressed_ADDR) & keys);
		if (pressed != 0)
			return (WaitKeysResult){pressed, 0x20u};
	}
}
/* <<< factory WaitUntilKeysArePressed */
