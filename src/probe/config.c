#include "home/config.h"
#include "probe.h"

static void adapt_DrawConfigMenuCursor(ProbeState *s)
{
	DrawConfigMenuCursor(s->a, s->c);
}

const ProbeEntry probe_entries_config[] = {
	{ "DrawConfigMenuCursor", adapt_DrawConfigMenuCursor },
	{ NULL, NULL },
};
