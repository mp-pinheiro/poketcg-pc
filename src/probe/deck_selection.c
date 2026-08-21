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

/* >>> factory GetPointerToDeckName */
static void adapt_GetPointerToDeckName(ProbeState *s)
{
	s->a = 0;
	s->f = 0x80;
	s->hl = GetPointerToDeckName();
}
/* <<< factory GetPointerToDeckName */

/* >>> factory InitDeckBuildingParams */
static void adapt_InitDeckBuildingParams(ProbeState *s)
{
	InitDeckBuildingParamsResult r = InitDeckBuildingParams(&s->hl, s->f);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}
/* <<< factory InitDeckBuildingParams */

const ProbeEntry probe_entries_deck_selection[] = {
	{ "GetPointerToDeckCards", adapt_GetPointerToDeckCards },
	{ "ResetCheckMenuCursorPositionAndBlink", adapt_ResetCheckMenuCursorPositionAndBlink },
	{ "GetPointerToDeckName", adapt_GetPointerToDeckName },
	{ "InitDeckBuildingParams", adapt_InitDeckBuildingParams },
	{ NULL, NULL },
};
