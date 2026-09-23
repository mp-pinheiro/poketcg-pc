#include "runtime.h"

#include "home/frames.h"

#include <limits.h>

static RuntimeEvent g_terminal_event;
static uint32_t g_event_mask;
static uint32_t g_event_count;

void runtime_events_reset(void)
{
	g_terminal_event = RUNTIME_EVENT_NONE;
	g_event_mask = 0u;
	g_event_count = 0u;
}

static void record_event(RuntimeEvent event)
{
	if (event == RUNTIME_EVENT_NONE)
		return;
	uint32_t bit = 1u << (unsigned)event;
	if ((g_event_mask & bit) == 0u) {
		g_event_mask |= bit;
		g_event_count++;
	}
}

void runtime_mark_event(RuntimeEvent event)
{
	record_event(event);
	if (event != RUNTIME_EVENT_NONE)
		g_terminal_event = event;
}

void runtime_record_event(RuntimeEvent event)
{
	record_event(event);
}

RuntimeEvent runtime_terminal_event(void)
{
	return g_terminal_event;
}

uint32_t runtime_event_mask(void)
{
	return g_event_mask;
}

uint32_t runtime_event_count(void)
{
	return g_event_count;
}

static struct {
	const uint16_t *counts;
	size_t count;
	uint32_t interval;
	unsigned used;
} g_serial = {NULL, 0, UINT32_MAX, 0};

void runtime_serial_track(const uint16_t *serial, size_t count)
{
	g_serial.counts = serial;
	g_serial.count = serial ? count : 0;
	g_serial.interval = UINT32_MAX;
	g_serial.used = 0;
}

unsigned runtime_serial_budget(void)
{
	if (!g_serial.counts)
		return UINT_MAX;
	uint32_t interval = frame_boundary_doframe_ordinal();
	if (interval >= g_serial.count)
		return 0;
	if (g_serial.interval != interval) {
		g_serial.interval = interval;
		g_serial.used = 0;
	}
	unsigned recorded = g_serial.counts[interval];
	return recorded > g_serial.used ? recorded - g_serial.used : 0;
}

void runtime_serial_consume(unsigned steps)
{
	if (g_serial.counts)
		g_serial.used += steps;
}
