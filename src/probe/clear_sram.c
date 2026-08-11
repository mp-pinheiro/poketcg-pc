#include "home/clear_sram.h"
#include "probe.h"

static void adapt_ClearSRAMBank(ProbeState *s)
{
	ClearSRAMResult result = ClearSRAMBank(s->a, s->f);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}

static void adapt_RestartSRAM(ProbeState *s)
{
	ClearSRAMResult result = RestartSRAM();
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}

const ProbeEntry probe_entries_clear_sram[] = {
	{ "ClearSRAMBank", adapt_ClearSRAMBank },
	{ "RestartSRAM", adapt_RestartSRAM },
	{ NULL, NULL },
};
