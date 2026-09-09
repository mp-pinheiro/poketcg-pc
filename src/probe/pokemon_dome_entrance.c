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

/* >>> factory Script_f631.ows_f63c */
static void adapt_Script_f631_ows_f63c(ProbeState *s)
{
	ScriptF631OwsF63cResult r = Script_f631_ows_f63c(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory Script_f631.ows_f63c */

const ProbeEntry probe_entries_pokemon_dome_entrance[] = {
	{ "PokemonDomeEntranceLoadMap", adapt_PokemonDomeEntranceLoadMap },
	{ "PokemonDomeEntranceCloseTextBox", adapt_PokemonDomeEntranceCloseTextBox },
	{ "Script_f631.ows_f63c", adapt_Script_f631_ows_f63c },
	{ NULL, NULL },
};
