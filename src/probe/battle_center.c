/* >>> part includes */
#include "home/battle_center.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory Func_fc2b */
static void adapt_Func_fc2b(ProbeState *s)
{
	(void)s;
	Func_fc2b();
}
/* <<< factory Func_fc2b */

/* >>> part probe_entries_battle_center */
const ProbeEntry probe_entries_battle_center[] = {
	{ "Func_fc2b", adapt_Func_fc2b },
	{ NULL, NULL },
};
/* <<< part probe_entries_battle_center */
