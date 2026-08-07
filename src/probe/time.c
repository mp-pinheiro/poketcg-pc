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

static void adapt_SetupTimer(ProbeState *s)
{
	TimerSetupResult result = SetupTimer();
	s->a = result.a;
	s->b = result.b;
	s->f = result.f;
}

const ProbeEntry probe_entries_time[] = {
	{ "IncrementPlayTimeCounter", adapt_IncrementPlayTimeCounter },
	{ "CheckForCGB", adapt_CheckForCGB },
	{ "SetupTimer", adapt_SetupTimer },
	{ NULL, NULL },
};
