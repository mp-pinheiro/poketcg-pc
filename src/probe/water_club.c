#include "home/water_club.h"
#include "probe.h"

static void adapt_Preload_Amy(ProbeState *s)
{
	PreloadAmyResult r = Preload_Amy();
	s->a = r.a;
	s->f = r.f;
}

const ProbeEntry probe_entries_water_club[] = {
	{ "Preload_Amy", adapt_Preload_Amy },
	{ NULL, NULL },
};
