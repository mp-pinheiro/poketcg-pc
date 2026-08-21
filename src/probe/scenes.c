#include "home/scenes.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory SetBoosterLogoOAM */
static void adapt_SetBoosterLogoOAM(ProbeState *s)
{
	SetBoosterLogoOAM();
}
/* <<< factory SetBoosterLogoOAM */

/* >>> factory _DrawPortrait */
static void adapt__DrawPortrait(ProbeState *s)
{
	(void)s;
	_DrawPortrait();
}
/* <<< factory _DrawPortrait */

const ProbeEntry probe_entries_scenes[] = {
	{ "SetBoosterLogoOAM", adapt_SetBoosterLogoOAM },
	{ "_DrawPortrait", adapt__DrawPortrait },
	{ NULL, NULL },
};
