#ifndef POKETCG_DUEL_ANIMATION_CORE_H
#define POKETCG_DUEL_ANIMATION_CORE_H
/* >>> part includes */
#include <stdint.h>
/* <<< part includes */
/* >>> part DuelAnimationResult */
typedef struct { uint8_t a; uint8_t f; } DuelAnimationResult;
/* <<< part DuelAnimationResult */
/* >>> part DuelAnimationUpdateResult */
typedef struct { uint8_t a; uint8_t c; uint16_t hl; } DuelAnimationUpdateResult;
/* <<< part DuelAnimationUpdateResult */
/* >>> factory _ResetAnimationQueue */
void _ResetAnimationQueue(void);
/* <<< factory _ResetAnimationQueue */
/* >>> factory PlayLoadedDuelAnimation */
void PlayLoadedDuelAnimation(void);
/* <<< factory PlayLoadedDuelAnimation */
/* >>> factory LoadDuelAnimationToBuffer */
uint8_t LoadDuelAnimationToBuffer(void);
/* <<< factory LoadDuelAnimationToBuffer */
/* >>> factory _UpdateQueuedAnimations */
DuelAnimationUpdateResult _UpdateQueuedAnimations(uint8_t entry_c, uint16_t entry_hl);
/* <<< factory _UpdateQueuedAnimations */
/* >>> factory ClearAndDisableQueuedAnimations */
DuelAnimationResult ClearAndDisableQueuedAnimations(void);
/* <<< factory ClearAndDisableQueuedAnimations */
#endif
