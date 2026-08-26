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

/* >>> factory ReloadMapAfterTextClose */
static void adapt_ReloadMapAfterTextClose(ProbeState *s)
{
	ReloadMapAfterTextClose();
}
/* <<< factory ReloadMapAfterTextClose */

/* >>> factory LoadMapGfxAndPermissions */
static void adapt_LoadMapGfxAndPermissions(ProbeState *s)
{
	LoadMapGfxAndPermissions();
}
/* <<< factory LoadMapGfxAndPermissions */

const ProbeEntry probe_entries_load_overworld[] = {
	{ "LoadMapTilesAndPals", adapt_LoadMapTilesAndPals },
	{ "ReloadMapAfterTextClose", adapt_ReloadMapAfterTextClose },
	{ "LoadMapGfxAndPermissions", adapt_LoadMapGfxAndPermissions },
	{ NULL, NULL },
};
