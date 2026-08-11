#include "home/pokemon_dome.h"
#include "probe.h"

static void adapt_Func_f762(ProbeState *s)
{
	s->f = Func_f762(s->f);
}

static void adapt_PlacePokemonDomeOpponentAtDuelTable(ProbeState *s)
{
	s->f = PlacePokemonDomeOpponentAtDuelTable(s->f);
}

static void adapt_Func_f782(ProbeState *s)
{
	s->f = Func_f782(s->b, s->c, s->f);
}

const ProbeEntry probe_entries_pokemon_dome[] = {
	{ "PlacePokemonDomeOpponentAtDuelTable", adapt_PlacePokemonDomeOpponentAtDuelTable },
	{ "Func_f762", adapt_Func_f762 },
	{ "Func_f782", adapt_Func_f782 },
	{ NULL, NULL },
};
