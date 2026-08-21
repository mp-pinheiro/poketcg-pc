#include "home/print_stats.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory DrawPauseMenuPlayerPortrait */
static void adapt_DrawPauseMenuPlayerPortrait(ProbeState *s)
{
	(void)s;
	DrawPauseMenuPlayerPortrait();
}
/* <<< factory DrawPauseMenuPlayerPortrait */

const ProbeEntry probe_entries_print_stats[] = {
	{ "DrawPauseMenuPlayerPortrait", adapt_DrawPauseMenuPlayerPortrait },
	{ NULL, NULL },
};
