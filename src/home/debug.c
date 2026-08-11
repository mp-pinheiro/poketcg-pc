#include "home/debug.h"

#include "generated/wram.h"
#include "home/lcd.h"
#include "home/tiles.h"
#include "home/wait_keys.h"

DebugSGBFrameResult DebugSGBFrame(uint8_t b, uint8_t c, uint8_t d,
	uint8_t e, uint16_t hl)
{
	uint8_t border = wDebugSGBBorder;
	DisableLCD();
	uint8_t next = (uint8_t)(border + 1u);
	uint8_t f;
	if (next >= 4u) {
		next = 0;
		f = 0x90u;
	} else {
		f = 0x10u;
	}
	wDebugSGBBorder = next;
	return (DebugSGBFrameResult){next, f, b, c, d, e, hl};
}

DebugStandardBGCharacterResult DebugStandardBGCharacter(uint8_t b, uint8_t c,
	uint8_t d, uint8_t e, uint16_t hl)
{
	(void)b;
	(void)c;
	(void)d;
	(void)e;
	(void)hl;
	FillRectangle(0x80u, 16u, 16u, 0, 0x0110u);
	WaitKeysResult result = WaitUntilKeysArePressed(0xFFu);
	return (DebugStandardBGCharacterResult){result.a, 0x10u, 0, 0};
}

DebugQuitResult DebugQuit(uint8_t a, uint8_t f)
{
	(void)f;
	return (DebugQuitResult){a, (uint8_t)(a == 0 ? 0x80u : 0)};
}
