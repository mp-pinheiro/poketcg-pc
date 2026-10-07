/* >>> part includes */
#include "home/diary.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory _PauseMenu_Diary */
static void adapt__PauseMenu_Diary(ProbeState *s)
{
	(void)s;
	_PauseMenu_Diary();
}
/* <<< factory _PauseMenu_Diary */

/* >>> part probe_entries_diary */
const ProbeEntry probe_entries_diary[] = {
	{ "_PauseMenu_Diary", adapt__PauseMenu_Diary },
	{ NULL, NULL },
};
/* <<< part probe_entries_diary */
