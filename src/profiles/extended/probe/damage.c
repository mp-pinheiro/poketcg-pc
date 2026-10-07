/* >>> part includes */
#include "home/damage.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory AddToDamage */
static void adapt_AddToDamage(ProbeState *s)
{
	AddToDamage(s->a);
}
/* <<< factory AddToDamage */

/* >>> part probe_entries_damage */
const ProbeEntry probe_entries_damage[] = {
	{ "AddToDamage", adapt_AddToDamage },
	{ NULL, NULL },
};
/* <<< part probe_entries_damage */
