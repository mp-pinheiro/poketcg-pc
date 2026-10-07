/* >>> part includes */
#include "home/math.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory ATimes10 */
static void adapt_ATimes10(ProbeState *s)
{
	s->a = ATimes10(s->a);
}
/* <<< factory ATimes10 */

/* >>> part probe_entries_math */
const ProbeEntry probe_entries_math[] = {
	{ "ATimes10", adapt_ATimes10 },
	{ NULL, NULL },
};
/* <<< part probe_entries_math */
