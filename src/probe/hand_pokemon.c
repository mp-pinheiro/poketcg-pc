#include "home/hand_pokemon.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory AIDecideSpecialEvolutions */
static void adapt_AIDecideSpecialEvolutions(ProbeState *s)
{
	(void)s;
	AIDecideSpecialEvolutions();
}
/* <<< factory AIDecideSpecialEvolutions */

/* >>> factory AIDecideEvolution */
static void adapt_AIDecideEvolution(ProbeState *s)
{
	s->a = AIDecideEvolution();
	s->f = 0u;
}
/* <<< factory AIDecideEvolution */

/* >>> factory AIDecidePlayLegendaryBirds */
static void adapt_AIDecidePlayLegendaryBirds(ProbeState *s)
{
	(void)s;
	AIDecidePlayLegendaryBirds();
}
/* <<< factory AIDecidePlayLegendaryBirds */

/* >>> factory AIDecidePlayPokemonCard */
static void adapt_AIDecidePlayPokemonCard(ProbeState *s)
{
	(void)s;
	AIDecidePlayPokemonCard();
}
/* <<< factory AIDecidePlayPokemonCard */

const ProbeEntry probe_entries_hand_pokemon[] = {
	{ "AIDecideSpecialEvolutions", adapt_AIDecideSpecialEvolutions },
	{ "AIDecideEvolution", adapt_AIDecideEvolution },
	{ "AIDecidePlayLegendaryBirds", adapt_AIDecidePlayLegendaryBirds },
	{ "AIDecidePlayPokemonCard", adapt_AIDecidePlayPokemonCard },
	{ NULL, NULL },
};
