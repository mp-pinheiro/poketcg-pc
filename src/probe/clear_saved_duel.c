/* >>> part includes */
#include "home/clear_saved_duel.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory ClearSavedDuel */
/* Nothing is written back. The asm's exit a/f/hl ($00/$80/$BC02) are constants no
 * caller reads -- both callsites bank1call this purely for the SRAM writes -- so they
 * are not part of the callable contract, and asserting them here would only hardcode
 * an output. b, c, d, e are never referenced by the asm; leaving them untouched makes
 * a C body that clobbers one show up as a diff. */
static void adapt_ClearSavedDuel(ProbeState *s)
{
	(void)s;
	ClearSavedDuel();
}
/* <<< factory ClearSavedDuel */

/* >>> part probe_entries_clear_saved_duel */
const ProbeEntry probe_entries_clear_saved_duel[] = {
	{ "ClearSavedDuel", adapt_ClearSavedDuel },
	{ NULL, NULL },
};
/* <<< part probe_entries_clear_saved_duel */
