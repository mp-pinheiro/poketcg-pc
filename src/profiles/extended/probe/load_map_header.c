/* >>> part includes */
#include "home/load_map_header.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory LoadMapHeader */
static void adapt_LoadMapHeader(ProbeState *s)
{
	(void)s;
	LoadMapHeader();
}
/* <<< factory LoadMapHeader */

/* >>> part probe_entries_load_map_header */
const ProbeEntry probe_entries_load_map_header[] = {
	{"LoadMapHeader", adapt_LoadMapHeader},
	{NULL, NULL},
};
/* <<< part probe_entries_load_map_header */
