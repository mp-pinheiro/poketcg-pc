#include "home/debug_main.h"

#include "generated/hram.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "home/credits_sequence_commands.h"
#include "home/default_palettes.h"
#include "home/labels.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/load_animation.h"
#include "home/menus.h"
#include "home/process_text.h"
#include "home/tiles.h"

/* debug_main.asm:21 `ld hl, Unknown_128f7` (naming.asm:42). $12661 is bank 4
 * ($12661 - 4 * $4000 + $4000 = $6661), so the label's banked address is $68F7. */
#define UNKNOWN_128F7 0x68F7u
#define SINGLE_SPACED 0x01u
#define DOUBLE_SPACED 0x00u
/* <<< factory statics */

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

/* >>> factory Func_12661 */
/* debug_main.asm:2-36, the unreferenced debug menu. Rebuild the screen, run
 * the menu until a non-cancel item is confirmed, dispatch it through
 * Func_126b3, and rebuild again while the dispatched routine returns carry.
 * The final `ret` follows `jr c`, which touches nothing, so a/f/hl come back
 * exactly as Func_126b3 left them -- hence the callee's result type. */
Func126b3Result Func_12661(void)
{
	wDebugMenuSelection = 0u;
	wDebugBoosterSelection = 0u;
	wDebugSGBBorder = 3u;
	for (;;) {
		uint8_t item;

		DisableLCD();
		wTileMapFill = 0u;
		EmptyScreen();
		(void)LoadSymbolsFont();
		(void)SetupText(0x30u, 0x7Fu);
		EnableAndClearSpriteAnimations();
		Func_12871();
		wLineSeparation = SINGLE_SPACED;
		InitAndPrintMenu(UNKNOWN_128F7, wDebugMenuSelection);
		EnableLCD();
		for (;;) {
			HandleMenuInputResult input;

			DoFrameIfLCDEnabled();
			input = HandleMenuInput();
			if (!(input.f & 0x10u))
				continue;
			item = hCurMenuItem;
			if (!(item & 0x80u))
				break;
		}
		wDebugMenuSelection = item;
		wLineSeparation = DOUBLE_SPACED;
		Func126b3Result result = Func_126b3();

		if (!(result.f & 0x10u))
			return result;
	}
}
/* <<< factory Func_12661 */
