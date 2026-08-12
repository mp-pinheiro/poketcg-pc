#include "home/deck_check.h"
#include "probe.h"

static void adapt_DrawCheckMenuCursor(ProbeState *s)
{
	DrawCheckMenuCursorResult result = DrawCheckMenuCursor(s->a);
	s->a = result.a;
	s->e = result.e;
	s->f = result.f;
}

static void adapt_PlaySFXConfirmOrCancel(ProbeState *s)
{
	PlaySFXConfirmOrCancel(s->a);
}

/* >>> factory EraseCheckMenuCursor */
static void adapt_EraseCheckMenuCursor(ProbeState *s)
{
	DrawCheckMenuCursorResult result = EraseCheckMenuCursor();
	s->a = result.a;
	s->e = result.e;
	s->f = result.f;
}
/* <<< factory EraseCheckMenuCursor */

/* >>> factory DisplayCheckMenuCursor */
static void adapt_DisplayCheckMenuCursor(ProbeState *s)
{
	DrawCheckMenuCursorResult result = DisplayCheckMenuCursor();
	s->a = result.a;
	s->e = result.e;
	s->f = result.f;
}
/* <<< factory DisplayCheckMenuCursor */

const ProbeEntry probe_entries_deck_check[] = {
	{"DrawCheckMenuCursor", adapt_DrawCheckMenuCursor},
	{"PlaySFXConfirmOrCancel", adapt_PlaySFXConfirmOrCancel},
	{ "EraseCheckMenuCursor", adapt_EraseCheckMenuCursor },
	{ "DisplayCheckMenuCursor", adapt_DisplayCheckMenuCursor },
	{NULL, NULL},
};
