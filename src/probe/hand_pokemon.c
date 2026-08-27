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

const ProbeEntry probe_entries_hand_pokemon[] = {
	{ "AIDecideSpecialEvolutions", adapt_AIDecideSpecialEvolutions },
	{ "AIDecideEvolution", adapt_AIDecideEvolution },
	{ NULL, NULL },
};
