#ifndef POKETCG_TRACE_H
#define POKETCG_TRACE_H

#include <stddef.h>
#include <stdint.h>

/* Frame-tagged function-entry trace, the native counterpart of the reference
 * routine-entry stream that tools/completion/refstream.py records from the ROM.
 * Comparing per-routine call counts per frame is the only way to answer how
 * often the port runs periodic work relative to the hardware interrupts and
 * command cascades the ROM drives.
 *
 * The hooks are always compiled; they only fire when the gbmem target is built
 * with -finstrument-functions (cmake -DPOKETCG_TRACE=ON). */

void trace_set_frame(uint32_t frame);
void trace_reset(void);
size_t trace_count(void);
int trace_overflowed(void);

/* Raw records, resolved to routine names offline by
 * tools/completion/native_trace.py against the same binary's symbol table. */
int trace_write_raw(const char *path);

/* Writes the trace if the run aborts, so a failed run is still measurable. */
void trace_flush_on_abort(const char *path);

/* Stops the probe at a routine's entry instead of at its caller's return.
 * A routine whose asm never returns under a probe seed -- the duel entry runs
 * an interactive arena choice the 16-frame input timeline cannot satisfy --
 * has no reachable `ret` for the oracle's `pre-ret` pc to match, so the only
 * boundary both lanes can stop at is somewhere inside it. The reference stops
 * on a pc; the native lane has no pc, so it stops when this function is
 * entered. `hit` must not return.
 *
 * The entry hook is compiled in every lane because the bank guard rides on it,
 * so this works without -finstrument-functions recording. */
void trace_set_stop(const void *fn, void (*hit)(void));

#endif /* POKETCG_TRACE_H */
