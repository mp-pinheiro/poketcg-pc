#include "home/legendary_dragonite.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory AIDoTurn_LegendaryDragonite */
static void adapt_AIDoTurn_LegendaryDragonite(ProbeState *s)
{
	AIDoTurn_LegendaryDragoniteResult result = AIDoTurn_LegendaryDragonite(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->f = result.f;
}
/* <<< factory AIDoTurn_LegendaryDragonite */

const ProbeEntry probe_entries_legendary_dragonite[] = {
	{ "AIDoTurn_LegendaryDragonite", adapt_AIDoTurn_LegendaryDragonite },
	{ NULL, NULL },
};
