#include "home/duel_animation_core.h"
#include "probe.h"

static void adapt_ResetAnimationQueue(ProbeState *s)
{
    _ResetAnimationQueue();
    (void)s;
}

static void adapt_PlayLoadedDuelAnimation(ProbeState *s)
{
    PlayLoadedDuelAnimation();
    (void)s;
}

static void adapt_LoadDuelAnimationToBuffer(ProbeState *s)
{
    s->a = LoadDuelAnimationToBuffer();
}

static void adapt_UpdateQueuedAnimations(ProbeState *s)
{
    DuelAnimationUpdateResult result = _UpdateQueuedAnimations();
    s->a = result.a;
}

static void adapt_ClearAndDisableQueuedAnimations(ProbeState *s)
{
    uint8_t f = s->f;
    DuelAnimationResult result = ClearAndDisableQueuedAnimations();
    s->a = result.a;
    s->f = (uint8_t)((f & 0xefu) | (result.f & 0x10u));
}

const ProbeEntry probe_entries_duel_animation_core[] = {
    { "_ResetAnimationQueue", adapt_ResetAnimationQueue },
    { "PlayLoadedDuelAnimation", adapt_PlayLoadedDuelAnimation },
    { "LoadDuelAnimationToBuffer", adapt_LoadDuelAnimationToBuffer },
    { "_UpdateQueuedAnimations", adapt_UpdateQueuedAnimations },
    { "ClearAndDisableQueuedAnimations", adapt_ClearAndDisableQueuedAnimations },
    { NULL, NULL },
};
