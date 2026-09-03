#include "trace.h"

#include <signal.h>
#include <stdio.h>
#include <string.h>

#include "bank_guard.h"

/* The gate consumes one count and one first frame per routine, never the call
 * sequence, so the tracer aggregates instead of logging. A 20,000,000-record
 * log was 229 MiB of BSS and, worse, silently capped a full-movie replay
 * mid-run: both a raw-movie and an aligned-movie gate run filled it exactly,
 * so reached_ordinal was reporting the buffer's size rather than where the port
 * stopped tracking the ROM. This table is bounded by the number of ported
 * routines instead of the number of calls. */
#define TRACE_SLOTS 16384u
#define TRACE_MAGIC "PTCGTRC2"

/* Every function here must stay uninstrumented, or __cyg_profile_func_enter
 * recurses into itself on the first call. */
#define NOTRACE __attribute__((no_instrument_function))

typedef struct {
	uint32_t callee;
	uint32_t first_frame;
	uint64_t calls;
} TraceRecord;

#ifdef POKETCG_TRACE
/* The entry hook itself is always compiled because the bank guard rides on it. */
static TraceRecord g_records[TRACE_SLOTS];
static uint32_t g_used;
#endif
static uint64_t g_count;
static uint32_t g_frame;
static int g_overflow;

#ifdef POKETCG_TRACE
/* Offsets are taken against this translation unit's own entry point so the
 * dump survives ASLR and can be resolved with `nm` offline. */
NOTRACE static uintptr_t trace_base(void)
{
	return (uintptr_t)(void *)trace_set_frame;
}
#endif

NOTRACE void trace_set_frame(uint32_t frame)
{
	g_frame = frame;
}

NOTRACE void trace_reset(void)
{
	g_count = 0;
	g_overflow = 0;
#ifdef POKETCG_TRACE
	memset(g_records, 0, sizeof g_records);
	g_used = 0;
#endif
}

NOTRACE size_t trace_count(void)
{
	return (size_t)g_count;
}

NOTRACE int trace_overflowed(void)
{
	return g_overflow;
}

static const void *g_stop_fn;
static void (*g_stop_hit)(void);

NOTRACE void trace_set_stop(const void *fn, void (*hit)(void))
{
	g_stop_fn = fn;
	g_stop_hit = hit;
}

NOTRACE void __cyg_profile_func_enter(void *this_fn, void *call_site)
{
	bank_guard_enter(this_fn);
	(void)call_site;
	if (this_fn == g_stop_fn && g_stop_hit)
		g_stop_hit();
#ifdef POKETCG_TRACE
	uint32_t callee = (uint32_t)((uintptr_t)this_fn - trace_base());
	/* Open addressing on the callee offset. Every offset is a multiple of the
	 * function alignment, so the low bits carry no entropy; mix them out. */
	uint32_t slot = (callee ^ (callee >> 13)) & (TRACE_SLOTS - 1u);

	g_count++;
	for (uint32_t probe = 0; probe < TRACE_SLOTS; probe++) {
		TraceRecord *record = &g_records[slot];
		if (record->calls == 0u) {
			record->callee = callee;
			record->first_frame = g_frame;
			record->calls = 1u;
			g_used++;
			return;
		}
		if (record->callee == callee) {
			record->calls++;
			return;
		}
		slot = (slot + 1u) & (TRACE_SLOTS - 1u);
	}
	g_overflow = 1;
#endif
}

NOTRACE void __cyg_profile_func_exit(void *this_fn, void *call_site)
{
	bank_guard_exit(this_fn);
	(void)call_site;
}

/* A whole-game run that aborts -- an unported script entry, a data-pack miss --
 * still executed everything up to that point, and the gate needs that trace to
 * report how far the port got. abort() raises SIGABRT, so the handler writes
 * the records and re-raises with the disposition restored. */
static const char *g_abort_path;

NOTRACE static void flush_on_abort(int signal_number)
{
	if (g_abort_path)
		(void)trace_write_raw(g_abort_path);
	signal(signal_number, SIG_DFL);
	raise(signal_number);
}

NOTRACE void trace_flush_on_abort(const char *path)
{
	g_abort_path = path;
	if (path)
		signal(SIGABRT, flush_on_abort);
}

NOTRACE int trace_write_raw(const char *path)
{
#ifndef POKETCG_TRACE
	(void)path;
	return -1;
#else
	if (!path)
		return -1;
	FILE *file = fopen(path, "wb");
	if (!file)
		return -1;
	uint64_t base = (uint64_t)trace_base();
	uint64_t calls = g_count;
	uint32_t overflow = (uint32_t)g_overflow;
	uint32_t record_size = (uint32_t)sizeof(TraceRecord);
	uint64_t used = (uint64_t)g_used;
	int ok = fwrite(TRACE_MAGIC, 8, 1, file) == 1
	      && fwrite(&base, sizeof base, 1, file) == 1
	      && fwrite(&used, sizeof used, 1, file) == 1
	      && fwrite(&overflow, sizeof overflow, 1, file) == 1
	      && fwrite(&record_size, sizeof record_size, 1, file) == 1
	      && fwrite(&calls, sizeof calls, 1, file) == 1;
	for (uint32_t slot = 0; ok && slot < TRACE_SLOTS; slot++) {
		if (g_records[slot].calls == 0u)
			continue;
		ok = fwrite(&g_records[slot], sizeof g_records[slot], 1, file) == 1;
	}
	if (fclose(file) != 0)
		ok = 0;
	return ok ? 0 : -1;
#endif
}
