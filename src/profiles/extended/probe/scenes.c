/* >>> part includes */
#include "home/scenes.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory SetBoosterLogoOAM */
static void adapt_SetBoosterLogoOAM(ProbeState *s)
{
	(void)s;
	SetBoosterLogoOAM();
}
/* <<< factory SetBoosterLogoOAM */


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

/* >>> part probe_entries_scenes */
const ProbeEntry probe_entries_scenes[] = {
	{ "SetBoosterLogoOAM", adapt_SetBoosterLogoOAM },
	{ "_LoadScene", adapt__LoadScene },
	{ "LoadBoosterGfx", adapt_LoadBoosterGfx },
	{ NULL, NULL },
};
/* <<< part probe_entries_scenes */
