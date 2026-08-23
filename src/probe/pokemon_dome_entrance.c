#include "home/pokemon_dome_entrance.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory PokemonDomeEntranceCloseTextBox */
static void adapt_PokemonDomeEntranceCloseTextBox(ProbeState *s)
{
	(void)s;
	PokemonDomeEntranceCloseTextBox();
}
/* <<< factory PokemonDomeEntranceCloseTextBox */

const ProbeEntry probe_entries_pokemon_dome_entrance[] = {
	{ "PokemonDomeEntranceCloseTextBox", adapt_PokemonDomeEntranceCloseTextBox },
	{ NULL, NULL },
};
