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

/* >>> factory AIDoAction_ForcedSwitch */
static void adapt_AIDoAction_ForcedSwitch(ProbeState *s)
{
	s->a = AIDoAction_ForcedSwitch();
}
/* <<< factory AIDoAction_ForcedSwitch */

const ProbeEntry probe_entries_ai[] = {
	{ "LoadOpponentDeck", adapt_LoadOpponentDeck },
	{ "AIDoAction", adapt_AIDoAction },
	{ "AIDoAction_ForcedSwitch", adapt_AIDoAction_ForcedSwitch },
	{ NULL, NULL },
};
