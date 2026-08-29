#ifndef POKETCG_HOME_EFFECT_DISPATCH_H
#define POKETCG_HOME_EFFECT_DISPATCH_H

#include <stdint.h>

#define EFFECT_DISPATCH_MAX_STACK_WORDS 4

typedef struct {
	uint8_t a, f, b, c, d, e;
	uint16_t hl;
	uint16_t stack[EFFECT_DISPATCH_MAX_STACK_WORDS];
	uint8_t stack_count;
	uint8_t post_call_byte;
} EffectDispatchState;

typedef void (*EffectDispatchFn)(EffectDispatchState *state);

typedef struct {
	const char *name;
	uint16_t address;
	EffectDispatchFn function;
} EffectDispatchEntry;

EffectDispatchFn EffectDispatchLookupName(const char *name);
EffectDispatchFn EffectDispatchLookupAddress(uint16_t address);

#endif /* POKETCG_HOME_EFFECT_DISPATCH_H */
