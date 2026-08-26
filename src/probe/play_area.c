#include "generated/wram.h"
#include "home/play_area.h"
#include "probe.h"

static void adapt_ZeroObjectPositionsAndToggleOAMCopy_Bank6(ProbeState *s)
{
	ZeroObjectPositionsAndToggleOAMCopy_Bank6();
	s->a = 1;
	s->f = 0xC0;
	s->c = 0;
	s->hl = (uint16_t)(wOAM_ADDR + 160u);
}

/* >>> factory OpenInPlayAreaScreen_HandleInput */
static void adapt_OpenInPlayAreaScreen_HandleInput(ProbeState *s)
{
	OpenInPlayAreaScreenHandleInputResult r = OpenInPlayAreaScreen_HandleInput();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory OpenInPlayAreaScreen_HandleInput */

/* >>> factory OpenInPlayAreaScreen_TurnHolderPlayArea */
static void adapt_OpenInPlayAreaScreen_TurnHolderPlayArea(ProbeState *s)
{
	(void)s;
	OpenInPlayAreaScreen_TurnHolderPlayArea();
}
/* <<< factory OpenInPlayAreaScreen_TurnHolderPlayArea */

/* >>> factory OpenInPlayAreaScreen_NonTurnHolderPlayArea */
static void adapt_OpenInPlayAreaScreen_NonTurnHolderPlayArea(ProbeState *s)
{
	(void)s;
	OpenInPlayAreaScreen_NonTurnHolderPlayArea();
}
/* <<< factory OpenInPlayAreaScreen_NonTurnHolderPlayArea */

/* >>> factory OpenInPlayAreaScreen_TurnHolderDiscardPile */
static void adapt_OpenInPlayAreaScreen_TurnHolderDiscardPile(ProbeState *s)
{
	OpenInPlayAreaScreen_TurnHolderDiscardPile(s->c);
}
/* <<< factory OpenInPlayAreaScreen_TurnHolderDiscardPile */

const ProbeEntry probe_entries_play_area[] = {
	{ "ZeroObjectPositionsAndToggleOAMCopy_Bank6", adapt_ZeroObjectPositionsAndToggleOAMCopy_Bank6 },
	{ "OpenInPlayAreaScreen_HandleInput", adapt_OpenInPlayAreaScreen_HandleInput },
	{ "OpenInPlayAreaScreen_TurnHolderPlayArea", adapt_OpenInPlayAreaScreen_TurnHolderPlayArea },
	{ "OpenInPlayAreaScreen_NonTurnHolderPlayArea", adapt_OpenInPlayAreaScreen_NonTurnHolderPlayArea },
	{ "OpenInPlayAreaScreen_TurnHolderDiscardPile", adapt_OpenInPlayAreaScreen_TurnHolderDiscardPile },
	{ NULL, NULL },
};
