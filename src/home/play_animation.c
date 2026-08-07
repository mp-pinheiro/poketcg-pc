#include "home/play_animation.h"

#include "generated/wram.h"
#include "mem.h"

#define ANIMATION_QUEUE_LENGTH 7u
#define rQUEUE 0xD423u

AnimationStatusResult CheckAnyAnimationPlaying(void)
{
	uint8_t value = (uint8_t)(gb_read8(wActiveScreenAnim_ADDR) & gb_read8(wd4c0_ADDR));
	for (uint8_t i = 0; i < ANIMATION_QUEUE_LENGTH; i++)
		value = (uint8_t)(value & gb_read8((uint16_t)(rQUEUE + i)));

	uint8_t flags = 0x40u;
	if (value == 0xffu)
		flags |= 0x80u;
	else {
		flags |= 0x10u;
		if ((value & 0x0fu) < 0x0fu)
			flags |= 0x20u;
	}
	return (AnimationStatusResult){value, flags};
}
FrameFunctionResult SetDoFrameFunction(uint16_t hl)
{
	gb_write8(wDoFrameFunction_ADDR, (uint8_t)hl);
	gb_write8(wDoFrameFunction_ADDR + 1u, (uint8_t)(hl >> 8));
	return (FrameFunctionResult){(uint8_t)(hl >> 8), (uint8_t)((hl >> 8) ? 0 : 0x80), hl};
}

FrameFunctionResult ResetDoFrameFunction(uint16_t hl)
{
	SetDoFrameFunction(0);
	return (FrameFunctionResult){0, 0x80, hl};
}
