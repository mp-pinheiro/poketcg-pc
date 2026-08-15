#include "home/sfx.h"
#include "probe.h"

static void adapt_SFX_PlaySFX(ProbeState *s)
{
	SFX_Play(s->a);
}

static void adapt_SFX_UpdateSFX(ProbeState *s)
{
	(void)s;
	SFX_Update();
}

/* >>> factory Func_fc105 */
static void adapt_Func_fc105(ProbeState *s)
{
	s->hl = Func_fc105((uint16_t)(s->b << 8 | s->c), (uint16_t)(s->d << 8 | s->e));
}
/* <<< factory Func_fc105 */

const ProbeEntry probe_entries_sfx[] = {
	{ "SFX_PlaySFX", adapt_SFX_PlaySFX },
	{ "SFX_UpdateSFX", adapt_SFX_UpdateSFX },
	{ "Func_fc105", adapt_Func_fc105 },
	{ NULL, NULL },
};
