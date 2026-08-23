#include "home/start.h"

#include "generated/wram.h"
#include "home/menus.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "home/text_box.h"
/* >>> factory statics */
#include "home/start.h"
#include "home/save.h"
#include "home/core.h"
#include "generated/wram.h"
#define FALSE 0x00u
#define TRUE 0x01u
/* <<< factory statics */

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
	return 0x10u;
}

/* >>> factory CheckIfHasSaveData */
CheckIfHasSaveDataResult CheckIfHasSaveData(void)
{
	ValidateResult first = ValidateBackupGeneralSaveData();
	uint8_t has_save = (first.f & 0x10u) ? TRUE : FALSE;
	wHasSaveData = has_save;
	if (has_save != FALSE) {
		uint8_t flags = ValidateSavedNonLinkDuelData();
		wHasDuelSaveData = (flags & 0x10u) ? FALSE : TRUE;
	} else {
		wHasDuelSaveData = FALSE;
	}
	ValidateResult final = ValidateBackupGeneralSaveData();
	return (CheckIfHasSaveDataResult){final.a, final.f};
}
/* <<< factory CheckIfHasSaveData */
