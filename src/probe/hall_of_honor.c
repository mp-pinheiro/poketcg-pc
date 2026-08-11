#include "home/hall_of_honor.h"
#include "probe.h"

static void adapt_HallOfHonorLoadMap(ProbeState *s)
{
	(void)s;
	HallOfHonorLoadMap();
}

const ProbeEntry probe_entries_hall_of_honor[] = {
	{ "HallOfHonorLoadMap", adapt_HallOfHonorLoadMap },
	{ NULL, NULL },
};
