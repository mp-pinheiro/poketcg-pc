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

/* >>> factory DrawPlayAreaToPlacePrizeCards */
static void adapt_DrawPlayAreaToPlacePrizeCards(ProbeState *s)
{
	(void)s;
	DrawPlayAreaToPlacePrizeCards();
}
/* <<< factory DrawPlayAreaToPlacePrizeCards */

const ProbeEntry probe_entries_duel_menus[] = {
	{ "DrawPlayersPrizeAndBenchCards", adapt_DrawPlayersPrizeAndBenchCards },
	{ "DrawPlayAreaToPlacePrizeCards", adapt_DrawPlayAreaToPlacePrizeCards },
	{ NULL, NULL },
};
