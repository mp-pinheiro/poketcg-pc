#include "home/init.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory InitAIDuelVars */
static void adapt_InitAIDuelVars(ProbeState *s)
{
	InitAIDuelVars();
	(void)s;
}
/* <<< factory InitAIDuelVars */

const ProbeEntry probe_entries_init[] = {
	{ "InitAIDuelVars", adapt_InitAIDuelVars },
	{ NULL, NULL },
};
