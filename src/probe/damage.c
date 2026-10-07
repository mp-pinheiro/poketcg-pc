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

/* >>> factory SubtractFromDamage */
static void adapt_SubtractFromDamage(ProbeState *s)
{
	SubtractFromDamage(s->a);
}
/* <<< factory SubtractFromDamage */

/* >>> part probe_entries_damage */
const ProbeEntry probe_entries_damage[] = {
	{ "AddToDamage", adapt_AddToDamage },
	{ "SubtractFromDamage", adapt_SubtractFromDamage },
	{ NULL, NULL },
};
/* <<< part probe_entries_damage */
