#include "home/legendary_articuno.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory ScoreLegendaryArticunoCards */
static void adapt_ScoreLegendaryArticunoCards(ProbeState *s)
{
	(void)s;
	ScoreLegendaryArticunoCards();
}
/* <<< factory ScoreLegendaryArticunoCards */

const ProbeEntry probe_entries_legendary_articuno[] = {
	{ "ScoreLegendaryArticunoCards", adapt_ScoreLegendaryArticunoCards },
	{ NULL, NULL },
};
