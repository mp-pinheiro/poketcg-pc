#include "home/retreat.h"
#include "probe.h"

static void adapt_SetAIRetreatFlags(ProbeState *s)
{
	SetAIRetreatFlagsResult r = SetAIRetreatFlags();
	s->a = r.a;
	s->f = r.f;
}

/* >>> factory AITryToRetreat */
static void adapt_AITryToRetreat(ProbeState *s)
{
	AITryToRetreatResult r = AITryToRetreat(s->a, s->f);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory AITryToRetreat */

/* >>> factory AIDecideBenchPokemonToSwitchTo */
static void adapt_AIDecideBenchPokemonToSwitchTo(ProbeState *s)
{
	AIDecideBenchPokemonToSwitchToResult r = AIDecideBenchPokemonToSwitchTo(s->d);
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
}
/* <<< factory AIDecideBenchPokemonToSwitchTo */

/* >>> factory AIDecideWhetherToRetreat */
/* >>> factory AIDecideWhetherToRetreat */
static void adapt_AIDecideWhetherToRetreat(ProbeState *s)
{
	AIDecideWhetherToRetreatResult r = AIDecideWhetherToRetreat(s->d);
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
}
/* <<< factory AIDecideWhetherToRetreat */

const ProbeEntry probe_entries_retreat[] = {
	{ "SetAIRetreatFlags", adapt_SetAIRetreatFlags },
	{ "AITryToRetreat", adapt_AITryToRetreat },
	{ "AIDecideBenchPokemonToSwitchTo", adapt_AIDecideBenchPokemonToSwitchTo },
	{ "AIDecideWhetherToRetreat", adapt_AIDecideWhetherToRetreat },
	{ NULL, NULL },
};
