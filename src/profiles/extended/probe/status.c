/* >>> part includes */
#include "home/status.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory _PauseMenu_Status */
static void adapt__PauseMenu_Status(ProbeState *s)
{
	(void)s;
	_PauseMenu_Status();
}
/* <<< factory _PauseMenu_Status */

/* >>> part probe_entries_status */
const ProbeEntry probe_entries_status[] = {
	{ "_PauseMenu_Status", adapt__PauseMenu_Status },
	{ NULL, NULL },
};
/* <<< part probe_entries_status */
