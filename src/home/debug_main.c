#include "home/debug_main.h"

#include "generated/hram.h"

/* debug_main.asm:38-41. The only returning table target is DebugQuit,
 * selected by menu item 10; it implements `or a` and returns. */
Func126b3Result Func_126b3(void)
{
	uint8_t a = hCurMenuItem;
	return (Func126b3Result){a, a == 0 ? 0x80u : 0x00u};
}
