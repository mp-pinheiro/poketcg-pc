#include "home/pokemon_dome.h"
#include "probe.h"

static void adapt_Func_f762(ProbeState *s)
{
	PokemonDomeResult result = Func_f762();
	s->a = result.a;
	s->f = result.f;
}

static void adapt_Func_f782(ProbeState *s)
{
	PokemonDomeResult result = Func_f782(s->b, s->c, s->f);
	s->a = result.a;
	s->f = result.f;
}

static void adapt_PlacePokemonDomeOpponentAtDuelTable(ProbeState *s)
{
	PokemonDomeResult result = PlacePokemonDomeOpponentAtDuelTable(s->f);
	s->a = result.a;
	s->f = result.f;
}

/* >>> factory Func_f77d */
static void adapt_Func_f77d(ProbeState *s)
{
	PokemonDomeResult result = Func_f77d(s->b, s->c, s->f);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Func_f77d */

const ProbeEntry probe_entries_pokemon_dome[] = {
	{"Func_f762", adapt_Func_f762},
	{"Func_f782", adapt_Func_f782},
	{"PlacePokemonDomeOpponentAtDuelTable", adapt_PlacePokemonDomeOpponentAtDuelTable},
	{ "Func_f77d", adapt_Func_f77d },
	{NULL, NULL},
};
