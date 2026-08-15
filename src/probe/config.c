#include "home/config.h"
#include "probe.h"

static void adapt_DrawConfigMenuCursor(ProbeState *s)
{
	DrawConfigMenuCursor(s->a, s->c);
}

/* >>> factory GetConfigCursorPositions */
static void adapt_GetConfigCursorPositions(ProbeState *s)
{
	(void)s;
	GetConfigCursorPositions();
}
/* <<< factory GetConfigCursorPositions */

/* >>> factory SaveConfigSettings */
static void adapt_SaveConfigSettings(ProbeState *s)
{
	(void)s;
	SaveConfigSettings();
}
/* <<< factory SaveConfigSettings */

const ProbeEntry probe_entries_config[] = {
	{ "DrawConfigMenuCursor", adapt_DrawConfigMenuCursor },
	{ "GetConfigCursorPositions", adapt_GetConfigCursorPositions },
	{ "SaveConfigSettings", adapt_SaveConfigSettings },
	{ NULL, NULL },
};
