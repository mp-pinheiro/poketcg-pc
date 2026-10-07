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

/* >>> factory HandleMoveModeAPress */
static void adapt_HandleMoveModeAPress(ProbeState *s)
{
	HandleMoveModeAPressResult r = HandleMoveModeAPress(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory HandleMoveModeAPress */

/* >>> factory RunOverworldScript */
static void adapt_RunOverworldScript(ProbeState *s)
{
	RunOverworldScriptResult r = RunOverworldScript(
		s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory RunOverworldScript */


const ProbeEntry probe_entries_script[] = {
	{ "GetMapScriptPointer", adapt_GetMapScriptPointer },
	{ "ResetAnimationQueue", adapt_ResetAnimationQueue },
	{ "FinishQueuedAnimations", adapt_FinishQueuedAnimations },
	{ "HandleMoveModeAPress", adapt_HandleMoveModeAPress },
	{ "RunOverworldScript", adapt_RunOverworldScript },
	{ NULL, NULL },
};
