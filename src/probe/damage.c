#include "home/damage.h"
#include "probe.h"

static void adapt_AddToDamage(ProbeState *s)
{
	AddToDamage(s->a);
}

static void adapt_SubtractFromDamage(ProbeState *s)
{
	SubtractFromDamage(s->a);
}

const ProbeEntry probe_entries_damage[] = {
	{ "AddToDamage", adapt_AddToDamage },
	{ "SubtractFromDamage", adapt_SubtractFromDamage },
	{ NULL, NULL },
};
