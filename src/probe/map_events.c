#include "home/map_events.h"
#include "probe.h"

static void adapt_ClearOWMapEvents(ProbeState *s)
{
	(void)s;
	ClearOWMapEvents();
}

const ProbeEntry probe_entries_map_events[] = {
	{ "ClearOWMapEvents", adapt_ClearOWMapEvents },
	{ NULL, NULL },
};
