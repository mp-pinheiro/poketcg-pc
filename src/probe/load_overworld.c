/* >>> part includes */
#include "home/load_overworld.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

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
	(void)s;
	ReloadMapAfterTextClose();
}
/* <<< factory ReloadMapAfterTextClose */

/* >>> factory LoadMapGfxAndPermissions */
static void adapt_LoadMapGfxAndPermissions(ProbeState *s)
{
	(void)s;
	LoadMapGfxAndPermissions();
}
/* <<< factory LoadMapGfxAndPermissions */

/* >>> part probe_entries_load_overworld */
const ProbeEntry probe_entries_load_overworld[] = {
	{ "LoadMapTilesAndPals", adapt_LoadMapTilesAndPals },
	{ "ReloadMapAfterTextClose", adapt_ReloadMapAfterTextClose },
	{ "LoadMapGfxAndPermissions", adapt_LoadMapGfxAndPermissions },
	{ NULL, NULL },
};
/* <<< part probe_entries_load_overworld */
