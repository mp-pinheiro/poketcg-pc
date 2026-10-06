#include "home/legendary_moltres.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory AIDoTurn_LegendaryMoltres */
static void adapt_AIDoTurn_LegendaryMoltres(ProbeState *s)
{
	AIDoTurn_LegendaryMoltresResult result = AIDoTurn_LegendaryMoltres(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->f = result.f;
}
/* <<< factory AIDoTurn_LegendaryMoltres */

const ProbeEntry probe_entries_legendary_moltres[] = {
	{ "AIDoTurn_LegendaryMoltres", adapt_AIDoTurn_LegendaryMoltres },
	{ NULL, NULL },
};
