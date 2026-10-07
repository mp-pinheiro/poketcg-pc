#ifndef POKETCG_HOME_SCRIPT_DISPATCH_H
#define POKETCG_HOME_SCRIPT_DISPATCH_H

/* >>> part includes */
#include <stddef.h>
/* <<< part includes */

/* >>> part ScriptDispatchState */
typedef struct {
	uint8_t a, f, b, c, d, e;
	uint16_t hl;
	uint16_t stack[4];
	uint8_t stack_count;
	uint8_t post_call_byte;
} ScriptDispatchState;
/* <<< part ScriptDispatchState */

/* >>> part ScriptDispatchFn */
typedef void (*ScriptDispatchFn)(ScriptDispatchState *state);
/* <<< part ScriptDispatchFn */

/* >>> part ScriptDispatchLookupOpcode */
ScriptDispatchFn ScriptDispatchLookupOpcode(uint8_t opcode);
/* <<< part ScriptDispatchLookupOpcode */

#endif
