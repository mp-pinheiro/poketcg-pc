#include "home/special_attacks.h"
#include "probe.h"

static void adapt_CheckIfAnyBasicPokemonInDeck(ProbeState *s)
{
	BasicPokemonDeckResult r = CheckIfAnyBasicPokemonInDeck();
	s->a = r.a;
	s->e = r.e;
	s->f = r.f;
	s->hl = r.hl;
}

/* >>> factory CheckWhetherToSwitchToFirstAttack */
static void adapt_CheckWhetherToSwitchToFirstAttack(ProbeState *s)
{
	(void)s;
	CheckWhetherToSwitchToFirstAttack();
}
/* <<< factory CheckWhetherToSwitchToFirstAttack */

const ProbeEntry probe_entries_special_attacks[] = {
	{"CheckIfAnyBasicPokemonInDeck", adapt_CheckIfAnyBasicPokemonInDeck},
	{ "CheckWhetherToSwitchToFirstAttack", adapt_CheckWhetherToSwitchToFirstAttack },
	{NULL, NULL},
};
