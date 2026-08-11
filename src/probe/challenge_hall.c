#include "home/challenge_hall.h"
#include "probe.h"

static void adapt_Func_f5db(ProbeState *s)
{
	ChallengeHallClearResult out = Func_f5db();
	s->a = out.a;
	s->f = out.f;
}

static void adapt_Func_f5e9(ProbeState *s)
{
	ChallengeHallBitResult out = Func_f5e9(s->c);
	s->b = out.b;
	s->hl = out.hl;
}

static void adapt_Script_Host(ProbeState *s)
{
	(void)s;
	Script_Host();
}

const ProbeEntry probe_entries_challenge_hall[] = {
	{ "Func_f5db", adapt_Func_f5db },
	{ "Func_f5e9", adapt_Func_f5e9 },
	{ "Script_Host", adapt_Script_Host },
	{ NULL, NULL },
};
