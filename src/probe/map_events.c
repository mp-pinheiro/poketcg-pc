#include "home/map_events.h"
#include "probe.h"

static void adapt_ClearOWMapEvents(ProbeState *s)
{
	(void)s;
	ClearOWMapEvents();
}

/* >>> factory SetOWMapEvent_SRAMOrVRAM */
static void adapt_SetOWMapEvent_SRAMOrVRAM(ProbeState *s)
{
	s->a = SetOWMapEvent_SRAMOrVRAM(s->a);
}
/* <<< factory SetOWMapEvent_SRAMOrVRAM */

const ProbeEntry probe_entries_map_events[] = {
	{ "ClearOWMapEvents", adapt_ClearOWMapEvents },
	{ "SetOWMapEvent_SRAMOrVRAM", adapt_SetOWMapEvent_SRAMOrVRAM },
	{ NULL, NULL },
};
