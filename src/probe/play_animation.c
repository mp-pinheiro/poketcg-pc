#include "home/play_animation.h"
#include "home/screen_effects.h"
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

/* >>> factory Func_3bb5 */
static void probe_no_effect(void) { }

/* hl is the effect routine `CallHL2` runs: one of Func_1ce03's .pointer_table
 * targets on every live entry, a no-op for the bare cases that seed none. */
static void adapt_Func_3bb5(ProbeState *s)
{
	void (*effect)(void) = ScreenEffectForAddress(s->hl);
	Func_3bb5(effect ? effect : probe_no_effect);
	s->a = 0x80u;
	s->f = 0x80u;
}
/* <<< factory Func_3bb5 */

const ProbeEntry probe_entries_play_animation[] = {
	{ "CheckAnyAnimationPlaying", adapt_CheckAnyAnimationPlaying },
	{ "SetDoFrameFunction", adapt_SetDoFrameFunction },
	{ "ResetDoFrameFunction", adapt_ResetDoFrameFunction },
	{ "PlayDuelAnimation", adapt_PlayDuelAnimation },
	{ "UpdateQueuedAnimations", adapt_UpdateQueuedAnimations },
	{ "Func_3bb5", adapt_Func_3bb5 },
	{ NULL, NULL },
};
