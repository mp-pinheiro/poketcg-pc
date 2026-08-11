#include "home/switch_sram.h"
#include "probe.h"

static void adapt_BankswitchSRAM(ProbeState *s)
{
	BankswitchSRAM(s->a);
}

static void adapt_EnableSRAM(ProbeState *s)
{
	EnableSRAM();
}

static void adapt_DisableSRAM(ProbeState *s)
{
	DisableSRAM();
}


const ProbeEntry probe_entries_sram[] = {
	{ "BankswitchSRAM", adapt_BankswitchSRAM },
	{ "EnableSRAM", adapt_EnableSRAM },
	{ "DisableSRAM", adapt_DisableSRAM },
	{ NULL, NULL },
};
