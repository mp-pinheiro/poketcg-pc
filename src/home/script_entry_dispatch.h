#ifndef POKETCG_HOME_SCRIPT_ENTRY_DISPATCH_H
#define POKETCG_HOME_SCRIPT_ENTRY_DISPATCH_H

#include <stdint.h>

/* A script entry inherits the caller's registers, because the asm reaches it by
 * `jp hl` rather than a call. Only b, c and hl are declared by any target, and
 * the targets that take them return them untouched without reading them, so the
 * dispatcher passes zero for each
 * and hl = the target address, which is what hl holds at the jump. */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} ScriptEntryRegs;

typedef ScriptEntryRegs (*ScriptEntryFn)(uint8_t b, uint8_t c, uint8_t d, uint8_t e,
                                         uint16_t hl);

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
	/* The entry runs with its own bank selected, because the asm reaches it by
	 * `jp hl` from code already executing there, and the bytecode interpreter
	 * reads its commands straight off that bank (home/script.asm:108-133). */
	uint8_t bank;
	ScriptEntryFn function;
} ScriptEntryRow;

const ScriptEntryRow *ScriptEntryLookup(uint16_t address);

/* Performs EnterScript's `jp hl` and returns the entry's exit flags, which the
 * jump makes the caller's: FindNPCOrObject tests carry after the PRESSED_A slot
 * (poketcg/src/home/script.asm:52-57). Aborts on an address that is not a known
 * script entry, or one whose routine is unported, so a whole-game run fails
 * loudly instead of silently skipping a script. */
ScriptEntryRegs ScriptEntryEnter(uint16_t target);
ScriptEntryRegs ScriptEntryEnterWith(uint16_t target, uint8_t f, uint8_t b, uint8_t c,
                                     uint8_t d, uint8_t e);

#endif
