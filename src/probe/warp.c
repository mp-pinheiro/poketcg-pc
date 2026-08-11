#include "home/warp.h"
#include "probe.h"

static void adapt_HandleMapWarp(ProbeState *s)
{
	HandleMapWarpResult result = _HandleMapWarp();
	s->a = result.a;
	s->f = result.f;
}

const ProbeEntry probe_entries_warp[] = {
	{ "_HandleMapWarp", adapt_HandleMapWarp },
	{ NULL, NULL },
};
