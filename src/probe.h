#ifndef POKETCG_PROBE_H
#define POKETCG_PROBE_H

#include <stddef.h>
#include <stdint.h>

/* Register-level view of one call, mirroring what the PyBoy oracle captures.
 * An adapter reads the fields its routine takes as input and writes the fields
 * its routine produces. Fields the asm contract calls "preserved" must be left
 * untouched, so the diff catches a C body that clobbers them. */
#define PROBE_MAX_STACK_WORDS 4

typedef struct {
	uint8_t a, f, b, c, d, e;
	uint16_t hl;
	/* Words the caller pushed below this routine's return address, in push
	 * order: stack[stack_count - 1] is what the routine's first `pop` reads.
	 * Only routines entered mid-frame -- a `jp` target whose epilogue pops
	 * saves its own caller made -- declare these; other adapters ignore them. */
	uint16_t stack[PROBE_MAX_STACK_WORDS];
	uint8_t stack_count;
} ProbeState;

typedef void (*ProbeFn)(ProbeState *s);

typedef struct {
	const char *name; /* pret symbol, e.g. "DecompressData.Decompress" */
	ProbeFn fn;
} ProbeEntry;

/* Each adapter translation unit under src/probe exports
 * `const ProbeEntry probe_entries_<basename>[]`, NULL-name terminated. CMake globs
 * those files and generates probe_groups.h from the basenames. */
ProbeFn probe_lookup(const char *name);

#endif /* POKETCG_PROBE_H */
