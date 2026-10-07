#include "home/default_palettes.h"
#include "probe.h"

static void adapt_Func_12871(ProbeState *s)
{
	(void)s;
	Func_12871();
}

static void adapt_SetDefaultPalettes(ProbeState *s)
{
	(void)s;
	SetDefaultPalettes();
}

const ProbeEntry probe_entries_default_palettes[] = {
	{ "Func_12871", adapt_Func_12871 },
	{ "SetDefaultPalettes", adapt_SetDefaultPalettes },
	{ NULL, NULL },
};
