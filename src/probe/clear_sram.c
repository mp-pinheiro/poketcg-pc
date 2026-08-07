#include "home/clear_sram.h"
#include "probe.h"

static void adapt_ClearSRAMBank(ProbeState *s)
{
	ClearSRAMBank(s->a);
}

static void adapt_RestartSRAM(ProbeState *s)
{
	(void)s;
	RestartSRAM();
}

const ProbeEntry probe_entries_clear_sram[] = {
	{ "ClearSRAMBank", adapt_ClearSRAMBank },
	{ "RestartSRAM", adapt_RestartSRAM },
	{ NULL, NULL },
};
