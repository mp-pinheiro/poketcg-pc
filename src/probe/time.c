#include "home/time.h"
#include "probe.h"

static void adapt_IncrementPlayTimeCounter(ProbeState *s)
{
	(void)s;
	IncrementPlayTimeCounter();
}

static void adapt_CheckForCGB(ProbeState *s)
{
	s->f = CheckForCGB();
}

const ProbeEntry probe_entries_time[] = {
	{ "IncrementPlayTimeCounter", adapt_IncrementPlayTimeCounter },
	{ "CheckForCGB", adapt_CheckForCGB },
	{ NULL, NULL },
};
