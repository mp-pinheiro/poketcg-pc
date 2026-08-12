#ifndef POKETCG_HOME_SCRIPT_H
#define POKETCG_HOME_SCRIPT_H

#include <stdint.h>

/* poketcg/src/home/script.asm */

typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} MapScriptResult;

MapScriptResult GetMapScriptPointer(uint8_t l);

/* >>> factory ResetAnimationQueue */
void ResetAnimationQueue(void);
/* <<< factory ResetAnimationQueue */
/* >>> factory FinishQueuedAnimations */
void FinishQueuedAnimations(void);
/* <<< factory FinishQueuedAnimations */
#endif
