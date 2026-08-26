#include "home/status.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory _PauseMenu_Status */
static void adapt__PauseMenu_Status(ProbeState *s)
{
	(void)s;
	_PauseMenu_Status();
}
/* <<< factory _PauseMenu_Status */

const ProbeEntry probe_entries_status[] = {
	{ "_PauseMenu_Status", adapt__PauseMenu_Status },
	{ NULL, NULL },
};
