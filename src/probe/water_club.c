#include "home/water_club.h"
#include "probe.h"

static void adapt_PreloadAmy(ProbeState *s)
{
	PreloadAmyResult result = Preload_Amy();
	s->a = result.a;
	s->f = result.f;
}

const ProbeEntry probe_entries_water_club[] = {
	{"Preload_Amy", adapt_PreloadAmy},
	{NULL, NULL},
};
