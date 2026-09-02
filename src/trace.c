#include "trace.h"

#include <signal.h>
#include <stdio.h>
#include <string.h>

#include "bank_guard.h"

#define TRACE_CAPACITY 20000000u
#define TRACE_MAGIC "PTCGTRC1"

/* Every function here must stay uninstrumented, or __cyg_profile_func_enter
 * recurses into itself on the first call. */
#define NOTRACE __attribute__((no_instrument_function))

typedef struct {
	uint32_t frame;
	uint32_t callee;
	uint32_t caller;
} TraceRecord;

#ifdef POKETCG_TRACE
/* 229 MiB of BSS, so it exists only in the instrumented lane. The entry hook
 * itself is always compiled because the bank guard rides on it. */
static TraceRecord g_records[TRACE_CAPACITY];
#endif
static size_t g_count;
static uint32_t g_frame;
static int g_overflow;

/* Offsets are taken against this translation unit's own entry point so the
 * dump survives ASLR and can be resolved with `nm` offline. */
NOTRACE static uintptr_t trace_base(void)
{
	return (uintptr_t)(void *)trace_set_frame;
}

NOTRACE void trace_set_frame(uint32_t frame)
{
	g_frame = frame;
}

NOTRACE void trace_reset(void)
{
	g_count = 0;
	g_overflow = 0;
}

NOTRACE size_t trace_count(void)
{
	return g_count;
}

NOTRACE int trace_overflowed(void)
{
	return g_overflow;
}

NOTRACE void __cyg_profile_func_enter(void *this_fn, void *call_site)
{
	bank_guard_enter(this_fn);
#ifdef POKETCG_TRACE
	if (g_count >= TRACE_CAPACITY) {
		g_overflow = 1;
		return;
	}
	TraceRecord *record = &g_records[g_count++];
	record->frame = g_frame;
	record->callee = (uint32_t)((uintptr_t)this_fn - trace_base());
	record->caller = (uint32_t)((uintptr_t)call_site - trace_base());
#else
	(void)call_site;
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
	uint64_t count = (uint64_t)g_count;
	uint32_t overflow = (uint32_t)g_overflow;
	uint32_t record_size = (uint32_t)sizeof(TraceRecord);
	int ok = fwrite(TRACE_MAGIC, 8, 1, file) == 1
	      && fwrite(&base, sizeof base, 1, file) == 1
	      && fwrite(&count, sizeof count, 1, file) == 1
	      && fwrite(&overflow, sizeof overflow, 1, file) == 1
	      && fwrite(&record_size, sizeof record_size, 1, file) == 1;
	if (ok && g_count)
		ok = fwrite(g_records, sizeof *g_records, g_count, file) == g_count;
	if (fclose(file) != 0)
		ok = 0;
	return ok ? 0 : -1;
#endif
}
