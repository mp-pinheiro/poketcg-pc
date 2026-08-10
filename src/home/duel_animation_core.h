#ifndef POKETCG_DUEL_ANIMATION_CORE_H
#define POKETCG_DUEL_ANIMATION_CORE_H
#include <stdint.h>
typedef struct { uint8_t a; uint8_t f; } DuelAnimationResult;
typedef struct { uint8_t a; } DuelAnimationUpdateResult;
void _ResetAnimationQueue(void);
void PlayLoadedDuelAnimation(void);
uint8_t LoadDuelAnimationToBuffer(void);
DuelAnimationUpdateResult _UpdateQueuedAnimations(void);
DuelAnimationResult ClearAndDisableQueuedAnimations(void);
#endif
