#ifndef POKETCG_HOME_SCRIPT_H
#define POKETCG_HOME_SCRIPT_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part MapScriptResult */
/* poketcg/src/home/script.asm */

typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} MapScriptResult;
/* <<< part MapScriptResult */

/* >>> factory GetMapScriptPointer */
MapScriptResult GetMapScriptPointer(uint8_t l);
/* <<< factory GetMapScriptPointer */

/* >>> factory ResetAnimationQueue */
void ResetAnimationQueue(void);
/* <<< factory ResetAnimationQueue */
/* >>> factory FinishQueuedAnimations */
void FinishQueuedAnimations(void);
/* <<< factory FinishQueuedAnimations */
/* >>> factory HandleMoveModeAPress */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} HandleMoveModeAPressResult;

HandleMoveModeAPressResult HandleMoveModeAPress(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory HandleMoveModeAPress */
/* >>> factory RunOverworldScript */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} RunOverworldScriptResult;

RunOverworldScriptResult RunOverworldScript(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c,
	uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory RunOverworldScript */
#endif
