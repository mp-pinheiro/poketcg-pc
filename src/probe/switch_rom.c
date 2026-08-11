#include "home/switch_rom.h"
#include "probe.h"

static void adapt_BankswitchROM(ProbeState *s)
{
	BankswitchROM(s->a);
}

const ProbeEntry probe_entries_switch_rom[] = {
	{ "BankswitchROM", adapt_BankswitchROM },
	{ NULL, NULL },
};
