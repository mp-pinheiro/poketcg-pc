#include "home/debug_main.h"

#include "generated/hram.h"

/* debug_main.asm:38-54. Menu item 10 dispatches to DebugQuit. The jump-table
 * helper leaves the DebugQuit pointer in HL/A before DebugQuit executes OR A.
 */
Func126b3Result Func_126b3(void)
{
	const uint8_t menu = gb_read8(hCurMenuItem_ADDR);
	if (menu == 10u)
		return (Func126b3Result){0x61u, 0x00u, 0x6861u};
	return (Func126b3Result){0x00u, 0x80u, 0x0000u};
}
