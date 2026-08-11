#include "home/debug.h"

#include "generated/wram.h"
#include "home/lcd.h"
#include "home/tiles.h"
#include "home/wait_keys.h"
#include "mem.h"

DebugResult DebugSGBFrame(void)
{
	uint8_t border;

	DisableLCD();
	border = gb_read8(wDebugSGBBorder_ADDR);
	border++;
	if (border >= 4)
		border = 0;
	gb_write8(wDebugSGBBorder_ADDR, border);
	return (DebugResult){border, 0x10};
}

DebugResult DebugStandardBGCharacter(void)
{
	WaitKeysResult keys;

	FillRectangle(0x80, 16, 16, 0, 0x0110);
	keys = WaitUntilKeysArePressed(0xff);
	return (DebugResult){keys.a, (uint8_t)(keys.f | 0x10)};
}

DebugResult DebugQuit(uint8_t a)
{
	return (DebugResult){a, a ? 0 : 0x80};
}
