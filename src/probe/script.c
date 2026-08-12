#include "home/script.h"
#include "probe.h"

static void adapt_GetMapScriptPointer(ProbeState *s)
{
	MapScriptResult r = GetMapScriptPointer((uint8_t)s->hl);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}

/* >>> factory ResetAnimationQueue */
static void adapt_ResetAnimationQueue(ProbeState *s)
{
	(void)s;
	ResetAnimationQueue();
}
/* <<< factory ResetAnimationQueue */

/* >>> factory FinishQueuedAnimations */
static void adapt_FinishQueuedAnimations(ProbeState *s)
{
	(void)s;
	FinishQueuedAnimations();
}
/* <<< factory FinishQueuedAnimations */

const ProbeEntry probe_entries_script[] = {
	{ "GetMapScriptPointer", adapt_GetMapScriptPointer },
	{ "ResetAnimationQueue", adapt_ResetAnimationQueue },
	{ "FinishQueuedAnimations", adapt_FinishQueuedAnimations },
	{ NULL, NULL },
};
