#include "home/play_animation.h"
#include "probe.h"

static void adapt_CheckAnyAnimationPlaying(ProbeState *s)
{
	AnimationStatusResult result = CheckAnyAnimationPlaying();
	s->a = result.a;
	s->f = result.f;
}

static void adapt_SetDoFrameFunction(ProbeState *s)
{
	uint8_t f = s->f;
	FrameFunctionResult result = SetDoFrameFunction(s->hl);
	s->a = result.a;
	s->f = f;
	s->hl = result.hl;
}

static void adapt_ResetDoFrameFunction(ProbeState *s)
{
	uint8_t f = s->f;
	FrameFunctionResult result = ResetDoFrameFunction(s->hl);
	s->a = result.a;
	s->f = f;
	s->hl = result.hl;
}

/* >>> factory PlayDuelAnimation */
static void adapt_PlayDuelAnimation(ProbeState *s)
{
	PlayDuelAnimationResult r = PlayDuelAnimation(s->a);
	s->a = r.a;
}
/* <<< factory PlayDuelAnimation */

/* >>> factory UpdateQueuedAnimations */
static void adapt_UpdateQueuedAnimations(ProbeState *s)
{
	uint8_t f = s->f;
	UpdateQueuedAnimationsResult result = UpdateQueuedAnimations(s->hl);
	s->a = result.a;
	s->f = f;
	s->hl = result.hl;
}
/* <<< factory UpdateQueuedAnimations */

const ProbeEntry probe_entries_play_animation[] = {
	{ "CheckAnyAnimationPlaying", adapt_CheckAnyAnimationPlaying },
	{ "SetDoFrameFunction", adapt_SetDoFrameFunction },
	{ "ResetDoFrameFunction", adapt_ResetDoFrameFunction },
	{ "PlayDuelAnimation", adapt_PlayDuelAnimation },
	{ "UpdateQueuedAnimations", adapt_UpdateQueuedAnimations },
	{ NULL, NULL },
};
