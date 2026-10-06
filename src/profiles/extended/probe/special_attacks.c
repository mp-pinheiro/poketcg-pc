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

/* >>> factory HandleSpecialAIAttacks */
static void adapt_HandleSpecialAIAttacks(ProbeState *s)
{
	HandleSpecialAIAttacksResult r = HandleSpecialAIAttacks();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandleSpecialAIAttacks */

const ProbeEntry probe_entries_special_attacks[] = {
	{"CheckIfAnyBasicPokemonInDeck", adapt_CheckIfAnyBasicPokemonInDeck},
	{ "CheckWhetherToSwitchToFirstAttack", adapt_CheckWhetherToSwitchToFirstAttack },
	{ "HandleSpecialAIAttacks", adapt_HandleSpecialAIAttacks },
	{NULL, NULL},
};
