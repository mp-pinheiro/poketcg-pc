#include "home/auto_deck_machines.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory ReadAutoDeckConfiguration */
static void adapt_ReadAutoDeckConfiguration(ProbeState *s)
{
	(void)s;
	ReadAutoDeckConfiguration();
}
/* <<< factory ReadAutoDeckConfiguration */

const ProbeEntry probe_entries_auto_deck_machines[] = {
	{ "ReadAutoDeckConfiguration", adapt_ReadAutoDeckConfiguration },
	{ NULL, NULL },
};
