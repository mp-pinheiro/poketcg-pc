#include "home/play_area.h"

#include "generated/wram.h"
#include "home/objects.h"
#include "mem.h"

void ZeroObjectPositionsAndToggleOAMCopy_Bank6(void)
{
	ZeroObjectPositions();
	gb_write8(wVBlankOAMCopyToggle_ADDR, 1);
}
