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

const ProbeEntry probe_entries_play_area[] = {
	{ "ZeroObjectPositionsAndToggleOAMCopy_Bank6", adapt_ZeroObjectPositionsAndToggleOAMCopy_Bank6 },
	{ "OpenInPlayAreaScreen_HandleInput", adapt_OpenInPlayAreaScreen_HandleInput },
	{ "OpenInPlayAreaScreen_TurnHolderPlayArea", adapt_OpenInPlayAreaScreen_TurnHolderPlayArea },
	{ NULL, NULL },
};
