#include "home/deck_check.h"
#include "probe.h"

static void adapt_DrawCheckMenuCursor(ProbeState *s)
{
	DrawCheckMenuCursor(s->a);
}

static void adapt_PlaySFXConfirmOrCancel(ProbeState *s)
{
	PlaySFXConfirmOrCancel(s->a);
}

const ProbeEntry probe_entries_deck_check[] = {
	{ "DrawCheckMenuCursor", adapt_DrawCheckMenuCursor },
	{ "PlaySFXConfirmOrCancel", adapt_PlaySFXConfirmOrCancel },
	{ NULL, NULL },
};
