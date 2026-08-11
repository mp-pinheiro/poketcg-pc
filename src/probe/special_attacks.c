#include "home/special_attacks.h"
#include "probe.h"

static void adapt_CheckIfAnyBasicPokemonInDeck(ProbeState *s)
{
	CheckIfAnyBasicPokemonInDeckResult result =
		CheckIfAnyBasicPokemonInDeck(s->b, s->c, s->d);
	s->a = result.a;
	s->f = result.f;
	s->e = result.e;
	s->hl = result.hl;
}

const ProbeEntry probe_entries_special_attacks[] = {
	{ "CheckIfAnyBasicPokemonInDeck", adapt_CheckIfAnyBasicPokemonInDeck },
	{ NULL, NULL },
};
