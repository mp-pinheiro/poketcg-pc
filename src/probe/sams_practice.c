#include "home/sams_practice.h"
#include "probe.h"

static void adapt_IsAIPracticeScriptedTurn(ProbeState *s)
{
	IsAIPracticeScriptedTurnResult r = IsAIPracticeScriptedTurn();
	s->a = r.a;
	s->f = r.f;
}

static void adapt_SetSamsStartingPlayArea(ProbeState *s)
{
	SamsPracticeResult r = SetSamsStartingPlayArea(s->c, s->b, s->d, s->e, s->hl);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

const ProbeEntry probe_entries_sams_practice[] = {
	{"IsAIPracticeScriptedTurn", adapt_IsAIPracticeScriptedTurn},
	{"SetSamsStartingPlayArea", adapt_SetSamsStartingPlayArea},
	{NULL, NULL},
};
