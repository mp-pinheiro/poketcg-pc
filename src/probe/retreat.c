#include "home/retreat.h"
#include "probe.h"

static void adapt_SetAIRetreatFlags(ProbeState *s)
{
	SetAIRetreatFlagsResult r = SetAIRetreatFlags();
	s->a = r.a;
	s->f = r.f;
}

const ProbeEntry probe_entries_retreat[] = {
	{ "SetAIRetreatFlags", adapt_SetAIRetreatFlags },
	{ NULL, NULL },
};
