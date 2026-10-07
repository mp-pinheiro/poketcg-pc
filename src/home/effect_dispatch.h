#ifndef POKETCG_HOME_EFFECT_DISPATCH_H
#define POKETCG_HOME_EFFECT_DISPATCH_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part EFFECT_DISPATCH_MAX_STACK_WORDS */
#define EFFECT_DISPATCH_MAX_STACK_WORDS 4
/* <<< part EFFECT_DISPATCH_MAX_STACK_WORDS */

/* >>> part EffectDispatchState */
typedef struct {
	uint8_t a, f, b, c, d, e;
	uint16_t hl;
	uint16_t stack[EFFECT_DISPATCH_MAX_STACK_WORDS];
	uint8_t stack_count;
	uint8_t post_call_byte;
} EffectDispatchState;
/* <<< part EffectDispatchState */

/* >>> part EffectDispatchFn */
typedef void (*EffectDispatchFn)(EffectDispatchState *state);
/* <<< part EffectDispatchFn */

/* >>> part EffectDispatchEntry */
typedef struct {
	const char *name;
	uint16_t address;
	EffectDispatchFn function;
} EffectDispatchEntry;
/* <<< part EffectDispatchEntry */

/* >>> part EffectDispatchLookupName */
EffectDispatchFn EffectDispatchLookupName(const char *name);
/* <<< part EffectDispatchLookupName */
/* >>> part EffectDispatchLookupAddress */
EffectDispatchFn EffectDispatchLookupAddress(uint16_t address);
/* <<< part EffectDispatchLookupAddress */

#endif /* POKETCG_HOME_EFFECT_DISPATCH_H */
