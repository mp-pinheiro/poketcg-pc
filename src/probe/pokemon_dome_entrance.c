#include "home/pokemon_dome_entrance.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory PokemonDomeEntranceLoadMap */
static void adapt_PokemonDomeEntranceLoadMap(ProbeState *s)
{
	PokemonDomeEntranceLoadMapResult r = PokemonDomeEntranceLoadMap();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory PokemonDomeEntranceLoadMap */

/* >>> factory PokemonDomeEntranceCloseTextBox */
static void adapt_PokemonDomeEntranceCloseTextBox(ProbeState *s)
{
	(void)s;
	PokemonDomeEntranceCloseTextBox();
}
/* <<< factory PokemonDomeEntranceCloseTextBox */

const ProbeEntry probe_entries_pokemon_dome_entrance[] = {
	{ "PokemonDomeEntranceLoadMap", adapt_PokemonDomeEntranceLoadMap },
	{ "PokemonDomeEntranceCloseTextBox", adapt_PokemonDomeEntranceCloseTextBox },
	{ NULL, NULL },
};
