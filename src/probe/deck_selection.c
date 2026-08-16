#include "home/deck_selection.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory GetPointerToDeckCards */
static void adapt_GetPointerToDeckCards(ProbeState *s)
{
	s->hl = GetPointerToDeckCards();
}
/* <<< factory GetPointerToDeckCards */

/* >>> factory ResetCheckMenuCursorPositionAndBlink */
static void adapt_ResetCheckMenuCursorPositionAndBlink(ProbeState *s)
{
	ResetCheckMenuCursorPositionAndBlinkResult r = ResetCheckMenuCursorPositionAndBlink();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ResetCheckMenuCursorPositionAndBlink */

const ProbeEntry probe_entries_deck_selection[] = {
	{ "GetPointerToDeckCards", adapt_GetPointerToDeckCards },
	{ "ResetCheckMenuCursorPositionAndBlink", adapt_ResetCheckMenuCursorPositionAndBlink },
	{ NULL, NULL },
};
