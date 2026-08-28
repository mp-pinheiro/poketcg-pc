#include "home/legendary_ronald.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory AIDoTurn_LegendaryRonald */
static void adapt_AIDoTurn_LegendaryRonald(ProbeState *s)
{
	AIDoTurn_LegendaryRonaldResult result = AIDoTurn_LegendaryRonald(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->f = result.f;
}
/* <<< factory AIDoTurn_LegendaryRonald */

const ProbeEntry probe_entries_legendary_ronald[] = {
	{ "AIDoTurn_LegendaryRonald", adapt_AIDoTurn_LegendaryRonald },
	{ NULL, NULL },
};
