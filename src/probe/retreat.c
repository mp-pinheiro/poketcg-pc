#include "home/retreat.h"
#include "probe.h"

static void adapt_SetAIRetreatFlags(ProbeState *s)
{
	SetAIRetreatFlagsResult r = SetAIRetreatFlags();
	s->a = r.a;
	s->f = r.f;
}

/* >>> factory AITryToRetreat */
static void adapt_AITryToRetreat(ProbeState *s)
{
	AITryToRetreatResult r = AITryToRetreat(s->a, s->f);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AITryToRetreat */

const ProbeEntry probe_entries_retreat[] = {
	{ "SetAIRetreatFlags", adapt_SetAIRetreatFlags },
	{ "AITryToRetreat", adapt_AITryToRetreat },
	{ NULL, NULL },
};
