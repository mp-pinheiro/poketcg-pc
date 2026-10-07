/* >>> part includes */
#include "home/unused_copyright.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory UnusedCopyrightScreen */
static void adapt_UnusedCopyrightScreen(ProbeState *s)
{
	(void)s;
	UnusedCopyrightScreen();
}
/* <<< factory UnusedCopyrightScreen */

/* >>> part probe_entries_unused_copyright */
const ProbeEntry probe_entries_unused_copyright[] = {
	{ "UnusedCopyrightScreen", adapt_UnusedCopyrightScreen },
	{ NULL, NULL },
};
/* <<< part probe_entries_unused_copyright */
