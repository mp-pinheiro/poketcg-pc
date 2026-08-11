#ifndef POKETCG_DUEL_ANIMATION_CORE_H
#define POKETCG_DUEL_ANIMATION_CORE_H
#include <stdint.h>
typedef struct { uint8_t a; uint8_t f; } DuelAnimationResult;
typedef struct { uint8_t a; uint16_t hl; } DuelAnimationUpdateResult;
void _ResetAnimationQueue(void);
void PlayLoadedDuelAnimation(void);
uint8_t LoadDuelAnimationToBuffer(void);
DuelAnimationUpdateResult _UpdateQueuedAnimations(uint16_t entry_hl);
DuelAnimationResult ClearAndDisableQueuedAnimations(void);
#endif
