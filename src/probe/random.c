/* >>> part includes */
#include "home/random.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory UpdateRNGSources */
static void adapt_UpdateRNGSources(ProbeState *s)
{
	/* bc/de/hl are left untouched so the diff catches a body that clobbers them. */
	s->a = UpdateRNGSources();
}
/* <<< factory UpdateRNGSources */

/* >>> factory HtimesL */
static void adapt_HtimesL(ProbeState *s)
{
	/* a is clobbered to 0 by the loop; the adapter leaves it alone rather than
	 * hardcoding that residue, and CONTRACT omits it. */
	s->hl = HtimesL(s->hl);
}
/* <<< factory HtimesL */

/* >>> factory Random */
static void adapt_Random(ProbeState *s)
{
	s->a = Random(s->a);
}
/* <<< factory Random */

/* >>> part probe_entries_random */
const ProbeEntry probe_entries_random[] = {
	{ "UpdateRNGSources", adapt_UpdateRNGSources },
	{ "HtimesL", adapt_HtimesL },
	{ "Random", adapt_Random },
	{ NULL, NULL },
};
/* <<< part probe_entries_random */
