#ifndef POKETCG_HOME_SCRIPT_DISPATCH_H
#define POKETCG_HOME_SCRIPT_DISPATCH_H

#include <stddef.h>

typedef struct {
	uint8_t a, f, b, c, d, e;
	uint16_t hl;
	uint16_t stack[4];
	uint8_t stack_count;
	uint8_t post_call_byte;
} ScriptDispatchState;

typedef void (*ScriptDispatchFn)(ScriptDispatchState *state);

ScriptDispatchFn ScriptDispatchLookupOpcode(uint8_t opcode);

#endif
