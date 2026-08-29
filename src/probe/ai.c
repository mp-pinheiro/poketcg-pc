#include "home/ai.h"
#include "probe.h"

static void adapt_LoadOpponentDeck(ProbeState *s)
{
	DeckLoadResult r = LoadOpponentDeck();
	s->a = r.a;
	s->hl = r.hl;
}

/* >>> factory AIDoAction */
static void adapt_AIDoAction(ProbeState *s)
{
	s->a = AIDoAction(s->a);
}
/* <<< factory AIDoAction */

const ProbeEntry probe_entries_ai[] = {
	{ "LoadOpponentDeck", adapt_LoadOpponentDeck },
	{ "AIDoAction", adapt_AIDoAction },
	{ NULL, NULL },
};
