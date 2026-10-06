#include "home/pokemon_dome.h"
#include "probe.h"

/* >>> factory Preload_Courtney */
static void adapt_Preload_Courtney(ProbeState *s)
{
	PokemonDomeResult r = Preload_Courtney();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Courtney */

/* >>> factory Preload_Steve */
static void adapt_Preload_Steve(ProbeState *s)
{
	PokemonDomeResult r = Preload_Steve();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Steve */

/* >>> factory Preload_Jack */
static void adapt_Preload_Jack(ProbeState *s)
{
	PokemonDomeResult r = Preload_Jack();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Jack */

/* >>> factory Preload_Rod */
static void adapt_Preload_Rod(ProbeState *s)
{
	PokemonDomeResult r = Preload_Rod();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Rod */

/* >>> factory Preload_Ronald1InPokemonDome */
static void adapt_Preload_Ronald1InPokemonDome(ProbeState *s)
{
	PokemonDomeResult r = Preload_Ronald1InPokemonDome();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Ronald1InPokemonDome */

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

/* >>> factory PokemonDomeCloseTextBox */
static void adapt_PokemonDomeCloseTextBox(ProbeState *s)
{
	(void)s;
	PokemonDomeCloseTextBox();
}
/* <<< factory PokemonDomeCloseTextBox */

/* >>> factory PokemonDomeMovePlayer */
static void adapt_PokemonDomeMovePlayer(ProbeState *s)
{
	(void)s;
	PokemonDomeMovePlayer();
}
/* <<< factory PokemonDomeMovePlayer */

/* >>> factory PokemonDomeLoadMap */
static void adapt_PokemonDomeLoadMap(ProbeState *s)
{
	(void)s;
	PokemonDomeLoadMap();
}
/* <<< factory PokemonDomeLoadMap */

/* >>> factory PokemonDomeAfterDuel */
static void adapt_PokemonDomeAfterDuel(ProbeState *s)
{
	PokemonDomeAfterDuelResult r = PokemonDomeAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory PokemonDomeAfterDuel */

const ProbeEntry probe_entries_pokemon_dome[] = {
	{"Func_f762", adapt_Func_f762},
	{"Func_f782", adapt_Func_f782},
	{"PlacePokemonDomeOpponentAtDuelTable", adapt_PlacePokemonDomeOpponentAtDuelTable},
	{ "Func_f77d", adapt_Func_f77d },
	{ "PokemonDomeCloseTextBox", adapt_PokemonDomeCloseTextBox },
	{ "PokemonDomeMovePlayer", adapt_PokemonDomeMovePlayer },
	{ "PokemonDomeAfterDuel", adapt_PokemonDomeAfterDuel },
	{ "PokemonDomeLoadMap", adapt_PokemonDomeLoadMap },
	{"Preload_Courtney", adapt_Preload_Courtney},
	{"Preload_Steve", adapt_Preload_Steve},
	{"Preload_Jack", adapt_Preload_Jack},
	{"Preload_Rod", adapt_Preload_Rod},
	{"Preload_Ronald1InPokemonDome", adapt_Preload_Ronald1InPokemonDome},
	{NULL, NULL},
};
