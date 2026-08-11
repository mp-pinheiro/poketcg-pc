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

const ProbeEntry probe_entries_special_attacks[] = {
	{"CheckIfAnyBasicPokemonInDeck", adapt_CheckIfAnyBasicPokemonInDeck},
	{NULL, NULL},
};
