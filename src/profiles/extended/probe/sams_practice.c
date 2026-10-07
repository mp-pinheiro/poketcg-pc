/* >>> part includes */
#include "home/sams_practice.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory IsAIPracticeScriptedTurn */
static void adapt_IsAIPracticeScriptedTurn(ProbeState *s)
{
	SamsPracticeResult r = IsAIPracticeScriptedTurn(s->a, s->f, s->b, s->c,
							 s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory IsAIPracticeScriptedTurn */

/* >>> factory SetSamsStartingPlayArea */
static void adapt_SetSamsStartingPlayArea(ProbeState *s)
{
	SamsPracticeResult r = SetSamsStartingPlayArea(s->a, s->f, s->b, s->c,
							      s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory SetSamsStartingPlayArea */

/* >>> factory GetPlayAreaLocationOfRaticateOrRattata */
static void adapt_GetPlayAreaLocationOfRaticateOrRattata(ProbeState *s)
{
	GetPlayAreaLocationOfRaticateOrRattata();
	(void)s;
}
/* <<< factory GetPlayAreaLocationOfRaticateOrRattata */

/* >>> factory AIPerformScriptedTurn */
static void adapt_AIPerformScriptedTurn(ProbeState *s)
{
	SamsPracticeResult result = AIPerformScriptedTurn(s->a, s->f, s->b, s->c,
						s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AIPerformScriptedTurn */

/* >>> part probe_entries_sams_practice */
const ProbeEntry probe_entries_sams_practice[] = {
	{"IsAIPracticeScriptedTurn", adapt_IsAIPracticeScriptedTurn},
	{"SetSamsStartingPlayArea", adapt_SetSamsStartingPlayArea},
	{ "GetPlayAreaLocationOfRaticateOrRattata", adapt_GetPlayAreaLocationOfRaticateOrRattata },
	{ "AIPerformScriptedTurn", adapt_AIPerformScriptedTurn },
	{NULL, NULL},
};
/* <<< part probe_entries_sams_practice */
