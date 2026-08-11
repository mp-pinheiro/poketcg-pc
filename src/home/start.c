#include "home/start.h"

#include "generated/wram.h"
#include "home/menus.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "home/text_box.h"

#define CONSOLE_CGB 0x02u
#define DISCLAIMER_TEXT_ID 0x0378u
#define SYM_CURSOR_D 0x2Fu
#define SYM_BOX_BOTTOM 0x1Du

uint8_t ShowCardPopCGBDisclaimer(void)
{
	uint16_t box = 0;
	if (wConsole == CONSOLE_CGB)
		return 0xC0u;

	DrawRegularTextBox(&box, 0, 20, 8, 0, 10);
	InitTextPrinting(1, 12);
	(void)PrintTextNoDelay(DISCLAIMER_TEXT_ID, 1, 12);
	(void)SetCursorParametersForTextBox(18, 17, SYM_CURSOR_D, SYM_BOX_BOTTOM);
	return WaitForButtonAorB().f;
}
