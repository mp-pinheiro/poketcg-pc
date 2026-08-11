#include "home/give_booster_pack.h"
#include "probe.h"

/* _PauseMenu_Exit is a bare ret: all registers are preserved. */
static void adapt_PauseMenu_Exit(ProbeState *s)
{
	(void)s;
	_PauseMenu_Exit();
}

const ProbeEntry probe_entries_give_booster_pack[] = {
	{ "_PauseMenu_Exit", adapt_PauseMenu_Exit },
	{ NULL, NULL },
};
