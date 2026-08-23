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

/* >>> factory ShowConfigMenuCursor */
static void adapt_ShowConfigMenuCursor(ProbeState *s)
{
	ShowConfigMenuCursorResult r = ShowConfigMenuCursor(s->a, s->b, s->c);
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory ShowConfigMenuCursor */

/* >>> factory HideConfigMenuCursor */
static void adapt_HideConfigMenuCursor(ProbeState *s)
{
	HideConfigMenuCursorResult r = HideConfigMenuCursor(s->a, s->b, s->c);
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory HideConfigMenuCursor */

/* >>> factory ConfigScreenDPadLeft */
static void adapt_ConfigScreenDPadLeft(ProbeState *s)
{
	ConfigScreenDPadLeft();
	s->a = 0x00u;
	s->f = 0x80u;
}
/* <<< factory ConfigScreenDPadLeft */

/* >>> factory ConfigScreenDPadRight */
static void adapt_ConfigScreenDPadRight(ProbeState *s)
{
	ConfigScreenDPadRight();
	s->a = 0x00u;
	s->f = 0x80u;
}
/* <<< factory ConfigScreenDPadRight */

const ProbeEntry probe_entries_config[] = {
	{ "DrawConfigMenuCursor", adapt_DrawConfigMenuCursor },
	{ "GetConfigCursorPositions", adapt_GetConfigCursorPositions },
	{ "SaveConfigSettings", adapt_SaveConfigSettings },
	{ "ShowConfigMenuCursor", adapt_ShowConfigMenuCursor },
	{ "HideConfigMenuCursor", adapt_HideConfigMenuCursor },
	{ "ConfigScreenDPadLeft", adapt_ConfigScreenDPadLeft },
	{ "ConfigScreenDPadRight", adapt_ConfigScreenDPadRight },
	{ NULL, NULL },
};
