#include "home/legendary_articuno.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory ScoreLegendaryArticunoCards */
static void adapt_ScoreLegendaryArticunoCards(ProbeState *s)
{
	(void)s;
	ScoreLegendaryArticunoCards();
}
/* <<< factory ScoreLegendaryArticunoCards */

/* >>> factory AIDoTurn_LegendaryArticuno */
static void adapt_AIDoTurn_LegendaryArticuno(ProbeState *s)
{
	AIDoTurn_LegendaryArticunoResult result = AIDoTurn_LegendaryArticuno(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->f = result.f;
}
/* <<< factory AIDoTurn_LegendaryArticuno */

const ProbeEntry probe_entries_legendary_articuno[] = {
	{ "ScoreLegendaryArticunoCards", adapt_ScoreLegendaryArticunoCards },
	{ "AIDoTurn_LegendaryArticuno", adapt_AIDoTurn_LegendaryArticuno },
	{ NULL, NULL },
};
