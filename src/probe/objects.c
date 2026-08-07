#include "home/objects.h"
#include "probe.h"

static void adapt_SetOneObjectAttributes(ProbeState *s)
{
	SetOneObjectAttributes(s->e, s->d, s->c, s->b);
}

static void adapt_ZeroObjectPositions(ProbeState *s)
{
	(void)s;
	ZeroObjectPositions();
}

const ProbeEntry probe_entries_objects[] = {
	{ "SetOneObjectAttributes", adapt_SetOneObjectAttributes },
	{ "ZeroObjectPositions", adapt_ZeroObjectPositions },
	{ NULL, NULL },
};
