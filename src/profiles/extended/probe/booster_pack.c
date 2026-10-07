/* >>> part includes */
#include "home/booster_pack.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory _OpenBoosterPack */
static void adapt__OpenBoosterPack(ProbeState *s)
{
	(void)s;
	_OpenBoosterPack();
}
/* <<< factory _OpenBoosterPack */

/* >>> part probe_entries_booster_pack */
const ProbeEntry probe_entries_booster_pack[] = {
	{ "_OpenBoosterPack", adapt__OpenBoosterPack },
	{ NULL, NULL },
};
/* <<< part probe_entries_booster_pack */
