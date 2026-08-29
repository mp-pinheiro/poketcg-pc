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

/* >>> factory AIDoAction_KOSwitch */
static void adapt_AIDoAction_KOSwitch(ProbeState *s)
{
	s->a = AIDoAction_KOSwitch();
}
/* <<< factory AIDoAction_KOSwitch */

/* >>> factory AIDoAction_StartDuel */
static void adapt_AIDoAction_StartDuel(ProbeState *s)
{
	s->a = AIDoAction_StartDuel();
}
/* <<< factory AIDoAction_StartDuel */

/* >>> factory AIDoAction_TakePrize */
static void adapt_AIDoAction_TakePrize(ProbeState *s)
{
	s->a = AIDoAction_TakePrize();
}
/* <<< factory AIDoAction_TakePrize */

const ProbeEntry probe_entries_ai[] = {
	{ "LoadOpponentDeck", adapt_LoadOpponentDeck },
	{ "AIDoAction", adapt_AIDoAction },
	{ "AIDoAction_ForcedSwitch", adapt_AIDoAction_ForcedSwitch },
	{ "AIDoAction_KOSwitch", adapt_AIDoAction_KOSwitch },
	{ "AIDoAction_StartDuel", adapt_AIDoAction_StartDuel },
	{ "AIDoAction_TakePrize", adapt_AIDoAction_TakePrize },
	{ NULL, NULL },
};
