/* >>> part includes */
#include "home/duel_animation_core.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory _ResetAnimationQueue */
static void adapt_ResetAnimationQueue(ProbeState *s)
{
    _ResetAnimationQueue();
    (void)s;
}
/* <<< factory _ResetAnimationQueue */

/* >>> factory PlayLoadedDuelAnimation */
static void adapt_PlayLoadedDuelAnimation(ProbeState *s)
{
    PlayLoadedDuelAnimation();
    (void)s;
}
/* <<< factory PlayLoadedDuelAnimation */

/* >>> factory LoadDuelAnimationToBuffer */
static void adapt_LoadDuelAnimationToBuffer(ProbeState *s)
{
    s->a = LoadDuelAnimationToBuffer();
}
/* <<< factory LoadDuelAnimationToBuffer */

/* >>> factory _UpdateQueuedAnimations */
static void adapt_UpdateQueuedAnimations(ProbeState *s)
{
    DuelAnimationUpdateResult result = _UpdateQueuedAnimations(s->c, s->hl);
    s->a = result.a;
    s->c = result.c;
    s->hl = result.hl;
}
/* <<< factory _UpdateQueuedAnimations */

/* >>> factory ClearAndDisableQueuedAnimations */
static void adapt_ClearAndDisableQueuedAnimations(ProbeState *s)
{
    uint8_t f = s->f;
    DuelAnimationResult result = ClearAndDisableQueuedAnimations();
    s->a = result.a;
    s->f = (uint8_t)((f & 0xefu) | (result.f & 0x10u));
}
/* <<< factory ClearAndDisableQueuedAnimations */

/* >>> part probe_entries_duel_animation_core */
const ProbeEntry probe_entries_duel_animation_core[] = {
    { "_ResetAnimationQueue", adapt_ResetAnimationQueue },
    { "PlayLoadedDuelAnimation", adapt_PlayLoadedDuelAnimation },
    { "LoadDuelAnimationToBuffer", adapt_LoadDuelAnimationToBuffer },
    { "_UpdateQueuedAnimations", adapt_UpdateQueuedAnimations },
    { "ClearAndDisableQueuedAnimations", adapt_ClearAndDisableQueuedAnimations },
    { NULL, NULL },
};
/* <<< part probe_entries_duel_animation_core */
