#include "home/math.h"
#include "probe.h"

static void adapt_ATimes10(ProbeState *s)
{
	s->a = ATimes10(s->a);
}

const ProbeEntry probe_entries_math[] = {
	{ "ATimes10", adapt_ATimes10 },
	{ NULL, NULL },
};
