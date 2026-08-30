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

/* >>> factory GetNPCDuelConfigurations */
static void adapt_GetNPCDuelConfigurations(ProbeState *s)
{
	GetNPCDuelConfigurationsResult result = GetNPCDuelConfigurations(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory GetNPCDuelConfigurations */

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

/* >>> factory Func_3b11 */
static void adapt_Func_3b11(ProbeState *s)
{
	(void)s;
	Func_3b11();
}
/* <<< factory Func_3b11 */

const ProbeEntry probe_entries_script[] = {
	{ "GetMapScriptPointer", adapt_GetMapScriptPointer },
	{ "ResetAnimationQueue", adapt_ResetAnimationQueue },
	{ "FinishQueuedAnimations", adapt_FinishQueuedAnimations },
	{ "GetNPCDuelConfigurations", adapt_GetNPCDuelConfigurations },
	{ "HandleMoveModeAPress", adapt_HandleMoveModeAPress },
	{ "Func_3b11", adapt_Func_3b11 },
	{ NULL, NULL },
};
