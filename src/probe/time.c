/* >>> part includes */
#include "home/time.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory IncrementPlayTimeCounter */
static void adapt_IncrementPlayTimeCounter(ProbeState *s)
{
	(void)s;
	IncrementPlayTimeCounter();
}
/* <<< factory IncrementPlayTimeCounter */

/* >>> factory CheckForCGB */
static void adapt_CheckForCGB(ProbeState *s)
{
	s->f = CheckForCGB();
}
/* <<< factory CheckForCGB */

/* >>> part SwitchToCGBNormalSpeed */
static void adapt_SwitchToCGBNormalSpeed(ProbeState *s)
{
	(void)s;
	SwitchToCGBNormalSpeed();
}
/* <<< part SwitchToCGBNormalSpeed */


/* >>> part SwitchToCGBDoubleSpeed */
static void adapt_SwitchToCGBDoubleSpeed(ProbeState *s)
{
	(void)s;
	SwitchToCGBDoubleSpeed();
}
/* <<< part SwitchToCGBDoubleSpeed */


/* >>> factory SetupTimer */
static void adapt_SetupTimer(ProbeState *s)
{
	TimerSetupResult result = SetupTimer();
	s->a = result.a;
	s->b = result.b;
	s->f = result.f;
}
/* <<< factory SetupTimer */

/* >>> factory TimerHandler */
static void adapt_TimerHandler(ProbeState *s)
{
	(void)s;
	TimerHandler();
}
/* <<< factory TimerHandler */

/* >>> part probe_entries_time */
const ProbeEntry probe_entries_time[] = {
	{ "IncrementPlayTimeCounter", adapt_IncrementPlayTimeCounter },
	{ "CheckForCGB", adapt_CheckForCGB },
	{ "SwitchToCGBDoubleSpeed", adapt_SwitchToCGBDoubleSpeed },
	{ "SwitchToCGBNormalSpeed", adapt_SwitchToCGBNormalSpeed },
	{ "SetupTimer", adapt_SetupTimer },
	{ "TimerHandler", adapt_TimerHandler },
	{ NULL, NULL },
};
/* <<< part probe_entries_time */
