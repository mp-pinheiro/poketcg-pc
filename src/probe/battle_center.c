#include "home/battle_center.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory Func_fc2b */
static void adapt_Func_fc2b(ProbeState *s)
{
	(void)s;
	Func_fc2b();
}
/* <<< factory Func_fc2b */

const ProbeEntry probe_entries_battle_center[] = {
	{ "Func_fc2b", adapt_Func_fc2b },
	{ NULL, NULL },
};
