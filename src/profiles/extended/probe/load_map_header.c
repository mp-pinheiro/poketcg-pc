#include "home/load_map_header.h"
#include "probe.h"

static void adapt_LoadMapHeader(ProbeState *s)
{
	(void)s;
	LoadMapHeader();
}

const ProbeEntry probe_entries_load_map_header[] = {
	{"LoadMapHeader", adapt_LoadMapHeader},
	{NULL, NULL},
};
