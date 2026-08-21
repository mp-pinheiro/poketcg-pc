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

const ProbeEntry probe_entries_hand_pokemon[] = {
	{ "AIDecideSpecialEvolutions", adapt_AIDecideSpecialEvolutions },
	{ NULL, NULL },
};
