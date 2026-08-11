#include "home/challenge_hall.h"
#include "probe.h"

static void adapt_Func_f5db(ProbeState *s)
{
	(void)s;
	Func_f5db();
}

static void adapt_Func_f5e9(ProbeState *s)
{
	FuncF5E9Result result = Func_f5e9(s->c);
	s->b = result.b;
	s->hl = result.hl;
}

static void adapt_Script_Host(ProbeState *s)
{
	(void)s;
	Script_Host();
}

const ProbeEntry probe_entries_challenge_hall[] = {
	{"Func_f5db", adapt_Func_f5db},
	{"Func_f5e9", adapt_Func_f5e9},
	{"Script_Host", adapt_Script_Host},
	{NULL, NULL},
};
