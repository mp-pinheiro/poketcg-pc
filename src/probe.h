#ifndef POKETCG_PROBE_H
#define POKETCG_PROBE_H

#include <stddef.h>
#include <stdint.h>

/* Register-level view of one call, mirroring what the PyBoy oracle captures.
 * An adapter reads the fields its routine takes as input and writes the fields
 * its routine produces. Fields the asm contract calls "preserved" must be left
 * untouched, so the diff catches a C body that clobbers them. */
typedef struct {
	uint8_t a, f, b, c, d, e;
	uint16_t hl;
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
