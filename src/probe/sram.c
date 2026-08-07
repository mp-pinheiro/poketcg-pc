#include "home/switch_sram.h"
#include "probe.h"

static void adapt_BankswitchSRAM(ProbeState *s)
{
	BankswitchSRAM(s->a);
}

const ProbeEntry probe_entries_sram[] = {
	{ "BankswitchSRAM", adapt_BankswitchSRAM },
	{ NULL, NULL },
};
