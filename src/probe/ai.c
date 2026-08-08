#include "home/ai.h"
#include "probe.h"

static void adapt_LoadOpponentDeck(ProbeState *s)
{
	DeckLoadResult r = LoadOpponentDeck();
	s->a = r.a;
	s->hl = r.hl;
}

const ProbeEntry probe_entries_ai[] = {
	{ "LoadOpponentDeck", adapt_LoadOpponentDeck },
	{ NULL, NULL },
};
