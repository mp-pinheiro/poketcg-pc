#include "home/legendary_zapdos.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory AIDoTurn_LegendaryZapdos */
static void adapt_AIDoTurn_LegendaryZapdos(ProbeState *s)
{
	AIDoTurn_LegendaryZapdosResult result = AIDoTurn_LegendaryZapdos(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->f = result.f;
}
/* <<< factory AIDoTurn_LegendaryZapdos */

const ProbeEntry probe_entries_legendary_zapdos[] = {
	{ "AIDoTurn_LegendaryZapdos", adapt_AIDoTurn_LegendaryZapdos },
	{ NULL, NULL },
};
