/* >>> part includes */
#include "home/switch_sram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory BankswitchSRAM */
static void adapt_BankswitchSRAM(ProbeState *s)
{
	BankswitchSRAM(s->a);
}
/* <<< factory BankswitchSRAM */

/* >>> part probe_entries_sram */
const ProbeEntry probe_entries_sram[] = {
	{ "BankswitchSRAM", adapt_BankswitchSRAM },
	{ NULL, NULL },
};
/* <<< part probe_entries_sram */
