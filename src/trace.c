#include "trace.h"

#include <stdio.h>
#include <string.h>

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

static TraceRecord g_records[TRACE_CAPACITY];
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
	if (g_count >= TRACE_CAPACITY) {
		g_overflow = 1;
		return;
	}
	TraceRecord *record = &g_records[g_count++];
	record->frame = g_frame;
	record->callee = (uint32_t)((uintptr_t)this_fn - trace_base());
	record->caller = (uint32_t)((uintptr_t)call_site - trace_base());
}

NOTRACE void __cyg_profile_func_exit(void *this_fn, void *call_site)
{
	(void)this_fn;
	(void)call_site;
}

NOTRACE int trace_write_raw(const char *path)
{
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
}
