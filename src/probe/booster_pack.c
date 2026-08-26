#include "home/booster_pack.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory _OpenBoosterPack */
static void adapt__OpenBoosterPack(ProbeState *s)
{
	_OpenBoosterPack();
}
/* <<< factory _OpenBoosterPack */

const ProbeEntry probe_entries_booster_pack[] = {
	{ "_OpenBoosterPack", adapt__OpenBoosterPack },
	{ NULL, NULL },
};
