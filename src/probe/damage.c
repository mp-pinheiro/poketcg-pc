#include "home/damage.h"
#include "probe.h"

static void adapt_AddToDamage(ProbeState *s)
{
	AddToDamage(s->a);
}

const ProbeEntry probe_entries_damage[] = {
	{ "AddToDamage", adapt_AddToDamage },
	{ NULL, NULL },
};
