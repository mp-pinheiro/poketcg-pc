#include "home/frames.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/input.h"
#include "mem.h"

#define PAD_CTRL_PAD 0xF0u
#define PAD_BUTTONS 0x0Fu

void HandleDPadRepeat(void)
{
	uint8_t keys = gb_read8(hKeysHeld_ADDR);

	gb_write8(hDPadHeld_ADDR, keys);
	if (keys & PAD_CTRL_PAD) {
		if (gb_read8(hKeysPressed_ADDR) & PAD_CTRL_PAD) {
			gb_write8(hDPadRepeat_ADDR, 24);
			return;
		}
		uint8_t repeat = (uint8_t)(gb_read8(hDPadRepeat_ADDR) - 1u);

		gb_write8(hDPadRepeat_ADDR, repeat);
		if (repeat != 0)
			return;
		gb_write8(hDPadRepeat_ADDR, 6);
		return;
	}
	gb_write8(hDPadHeld_ADDR,
	          (uint8_t)(gb_read8(hKeysPressed_ADDR) & PAD_BUTTONS));
}

void DoFrame(void)
{
	gb_write8(wVBlankCounter_ADDR,
	          (uint8_t)(gb_read8(wVBlankCounter_ADDR) + 1u));
	ReadJoypad();
	HandleDPadRepeat();
}

void DoAFrames(uint8_t a)
{
	uint16_t count = a ? a : 0x100u;

	while (count--)
		DoFrame();
}
