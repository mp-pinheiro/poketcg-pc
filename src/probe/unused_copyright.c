#include "home/unused_copyright.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory UnusedCopyrightScreen */
static void adapt_UnusedCopyrightScreen(ProbeState *s)
{
	UnusedCopyrightScreen();
}
/* <<< factory UnusedCopyrightScreen */

const ProbeEntry probe_entries_unused_copyright[] = {
	{ "UnusedCopyrightScreen", adapt_UnusedCopyrightScreen },
	{ NULL, NULL },
};
