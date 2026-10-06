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

static void adapt_SwitchToCGBNormalSpeed(ProbeState *s)
{
	(void)s;
	SwitchToCGBNormalSpeed();
}


static void adapt_SwitchToCGBDoubleSpeed(ProbeState *s)
{
	(void)s;
	SwitchToCGBDoubleSpeed();
}


static void adapt_SetupTimer(ProbeState *s)
{
	TimerSetupResult result = SetupTimer();
	s->a = result.a;
	s->b = result.b;
	s->f = result.f;
}

/* >>> factory TimerHandler */
static void adapt_TimerHandler(ProbeState *s)
{
	(void)s;
	TimerHandler();
}
/* <<< factory TimerHandler */

const ProbeEntry probe_entries_time[] = {
	{ "IncrementPlayTimeCounter", adapt_IncrementPlayTimeCounter },
	{ "CheckForCGB", adapt_CheckForCGB },
	{ "SwitchToCGBDoubleSpeed", adapt_SwitchToCGBDoubleSpeed },
	{ "SwitchToCGBNormalSpeed", adapt_SwitchToCGBNormalSpeed },
	{ "SetupTimer", adapt_SetupTimer },
	{ "TimerHandler", adapt_TimerHandler },
	{ NULL, NULL },
};
