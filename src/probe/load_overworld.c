#include "home/load_overworld.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory LoadMapTilesAndPals */
static void adapt_LoadMapTilesAndPals(ProbeState *s)
{
	LoadMapTilesAndPals();
	(void)s;
}
/* <<< factory LoadMapTilesAndPals */

const ProbeEntry probe_entries_load_overworld[] = {
	{ "LoadMapTilesAndPals", adapt_LoadMapTilesAndPals },
	{ NULL, NULL },
};
