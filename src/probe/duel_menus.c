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

/* >>> factory DrawYourOrOppPlayAreaScreen_Bank0 */
static void adapt_DrawYourOrOppPlayAreaScreen_Bank0(ProbeState *s)
{
	DrawYourOrOppPlayAreaScreen_Bank0(s->hl);
}
/* <<< factory DrawYourOrOppPlayAreaScreen_Bank0 */

/* >>> factory DrawAIPeekScreen */
static void adapt_DrawAIPeekScreen(ProbeState *s)
{
	DrawAIPeekScreenResult result = DrawAIPeekScreen(s->a, s->f);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory DrawAIPeekScreen */

/* >>> factory SelectPrizeCards */
static void adapt_SelectPrizeCards(ProbeState *s)
{
	SelectPrizeCards(s->a);
}
/* <<< factory SelectPrizeCards */

/* >>> factory HandlePeekSelection */
static void adapt_HandlePeekSelection(ProbeState *s)
{
	HandlePeekSelectionV2Result r = HandlePeekSelection(s->f);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandlePeekSelection */

const ProbeEntry probe_entries_duel_menus[] = {
	{ "DrawPlayersPrizeAndBenchCards", adapt_DrawPlayersPrizeAndBenchCards },
	{ "DrawPlayAreaToPlacePrizeCards", adapt_DrawPlayAreaToPlacePrizeCards },
	{ "DrawYourOrOppPlayAreaScreen_Bank0", adapt_DrawYourOrOppPlayAreaScreen_Bank0 },
	{ "DrawAIPeekScreen", adapt_DrawAIPeekScreen },
	{ "SelectPrizeCards", adapt_SelectPrizeCards },
	{ "HandlePeekSelection", adapt_HandlePeekSelection },
	{ NULL, NULL },
};
