#include "home/duel_menus.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory DrawPlayersPrizeAndBenchCards */
static void adapt_DrawPlayersPrizeAndBenchCards(ProbeState *s)
{
	(void)s;
	DrawPlayersPrizeAndBenchCards();
}
/* <<< factory DrawPlayersPrizeAndBenchCards */

const ProbeEntry probe_entries_duel_menus[] = {
	{ "DrawPlayersPrizeAndBenchCards", adapt_DrawPlayersPrizeAndBenchCards },
	{ NULL, NULL },
};
