#include "runtime.h"

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
