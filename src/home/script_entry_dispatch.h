#ifndef POKETCG_HOME_SCRIPT_ENTRY_DISPATCH_H
#define POKETCG_HOME_SCRIPT_ENTRY_DISPATCH_H

#include <stdint.h>

typedef void (*ScriptEntryFn)(void);

/* A script entry is reached by `jp hl` from EnterScript
 * (engine/overworld/overworld.asm:122-127) with hl read out of wNextScript, so
 * the target's own first opcode decides what runs. Deciding that at run time
 * would mean reading ROM code as data, which the product data pack cannot
 * serve, so the kind is resolved from poketcg.sym plus the ROM at build time by
 * tools/gen_script_entry_dispatch.py. */
typedef enum {
	/* Opens with the start_script macro (macros/scripts.asm:1-3), a lone
	 * `rst $20`, which pushes target+1 and enters RST20
	 * (engine/overworld/scripting.asm:549-551). */
	SCRIPT_ENTRY_BYTECODE = 0,
	/* Opens with ordinary instructions and is ported to C. */
	SCRIPT_ENTRY_ROUTINE = 1,
	/* Opens with ordinary instructions and has no C body yet. */
	SCRIPT_ENTRY_UNPORTED = 2,
} ScriptEntryKind;

typedef struct {
	uint16_t address;
	const char *name;
	ScriptEntryKind kind;
	ScriptEntryFn function;
} ScriptEntryRow;

const ScriptEntryRow *ScriptEntryLookup(uint16_t address);

/* Performs EnterScript's `jp hl`. Aborts on an address that is not a known
 * script entry, or one whose routine is unported, so a whole-game run fails
 * loudly instead of silently skipping a script. */
void ScriptEntryEnter(uint16_t target);

#endif
