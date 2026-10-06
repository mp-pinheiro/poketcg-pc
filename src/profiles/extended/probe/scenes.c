#include "home/scenes.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory SetBoosterLogoOAM */
static void adapt_SetBoosterLogoOAM(ProbeState *s)
{
	(void)s;
	SetBoosterLogoOAM();
}
/* <<< factory SetBoosterLogoOAM */

/* >>> factory _DrawPortrait */
static void adapt__DrawPortrait(ProbeState *s)
{
	_DrawPortrait(s->b, s->c);
}
/* <<< factory _DrawPortrait */

/* >>> factory _LoadScene */
static void adapt__LoadScene(ProbeState *s)
{
	_LoadScene(s->a, s->b, s->c);
}
/* <<< factory _LoadScene */

/* >>> factory LoadBoosterGfx */
static void adapt_LoadBoosterGfx(ProbeState *s)
{
	s->a = LoadBoosterGfx(s->a, s->b, s->c);
}
/* <<< factory LoadBoosterGfx */

const ProbeEntry probe_entries_scenes[] = {
	{ "SetBoosterLogoOAM", adapt_SetBoosterLogoOAM },
	{ "_DrawPortrait", adapt__DrawPortrait },
	{ "_LoadScene", adapt__LoadScene },
	{ "LoadBoosterGfx", adapt_LoadBoosterGfx },
	{ NULL, NULL },
};
