#include "home/screen_effects.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory DecrementScreenAnimDuration */
static void adapt_DecrementScreenAnimDuration(ProbeState *s)
{
	DecrementDurResult r = DecrementScreenAnimDuration(s->f);
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory DecrementScreenAnimDuration */

/* >>> factory UpdateShakeOffset */
static void adapt_UpdateShakeOffset(ProbeState *s)
{
	UpdateShakeOffsetResult r = UpdateShakeOffset();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory UpdateShakeOffset */

/* >>> factory DefaultScreenAnimationUpdate */
static void adapt_DefaultScreenAnimationUpdate(ProbeState *s)
{
	DefaultScreenAnimationUpdate();
	(void)s;
}
/* <<< factory DefaultScreenAnimationUpdate */

const ProbeEntry probe_entries_screen_effects[] = {
	{ "DecrementScreenAnimDuration", adapt_DecrementScreenAnimDuration },
	{ "UpdateShakeOffset", adapt_UpdateShakeOffset },
	{ "DefaultScreenAnimationUpdate", adapt_DefaultScreenAnimationUpdate },
	{ NULL, NULL },
};
