/* >>> part includes */
#include "home/link_duel.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory _SetUpAndStartLinkDuel */
static void adapt__SetUpAndStartLinkDuel(ProbeState *s)
{
	(void)s;
	_SetUpAndStartLinkDuel();
}
/* <<< factory _SetUpAndStartLinkDuel */

/* >>> part probe_entries_link_duel */
const ProbeEntry probe_entries_link_duel[] = {
	{ "_SetUpAndStartLinkDuel", adapt__SetUpAndStartLinkDuel },
	{ NULL, NULL },
};
/* <<< part probe_entries_link_duel */
