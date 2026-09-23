#include "isr.h"

#include <string.h>

#define ISR_SLOTS 1024u
#define ISR_SLOT_MASK (ISR_SLOTS - 1u)
#define ISR_SITE_EVENTS 8u

static const IsrTrack *g_track;
static IsrDeliver g_deliver;
static uint32_t g_interval = UINT32_MAX;
static size_t g_cursor;
static size_t g_end;
static uint8_t g_delivering;
static unsigned g_context;
static uint32_t g_placed;
static uint32_t g_unplaced;
static uint32_t g_site_counts[ISR_SITE_EVENTS];

static struct {
	const void *fn;
	uint32_t count;
} g_counts[ISR_SLOTS];
static uint16_t g_touched[ISR_SLOTS];
static uint16_t g_touched_count;

static void isr_clear_counts(void)
{
	for (uint16_t i = 0; i < g_touched_count; i++)
		g_counts[g_touched[i]].fn = NULL;
	g_touched_count = 0;
	memset(g_site_counts, 0, sizeof g_site_counts);
}

void isr_set_track(const IsrTrack *track, IsrDeliver deliver)
{
	g_track = track && track->count ? track : NULL;
	g_deliver = deliver;
	g_interval = UINT32_MAX;
	g_cursor = 0;
	g_end = 0;
	if (g_track) {
		g_placed = 0;
		g_unplaced = 0;
	}
	memset(g_counts, 0, sizeof g_counts);
	g_touched_count = 0;
	memset(g_site_counts, 0, sizeof g_site_counts);
	if (g_track)
		isr_begin_interval(0);
}

uint32_t isr_placed(void)
{
	return g_placed;
}

uint32_t isr_unplaced(void)
{
	return g_unplaced;
}

static uint32_t isr_bump(const void *fn)
{
	uintptr_t key = (uintptr_t)fn;
	uint32_t slot = (uint32_t)((key >> 4) ^ (key >> 13)) & ISR_SLOT_MASK;

	for (uint32_t probe = 0; probe < ISR_SLOTS; probe++) {
		if (g_counts[slot].fn == fn)
			return ++g_counts[slot].count;
		if (!g_counts[slot].fn) {
			g_counts[slot].fn = fn;
			g_counts[slot].count = 1;
			if (g_touched_count < ISR_SLOTS)
				g_touched[g_touched_count++] = (uint16_t)slot;
			return 1;
		}
		slot = (slot + 1u) & ISR_SLOT_MASK;
	}
	return 0;
}

void isr_begin_interval(uint32_t interval)
{
	if (!g_track)
		return;
	isr_clear_counts();
	g_interval = interval;
	if (interval >= g_track->count) {
		g_cursor = g_end = 0;
		return;
	}
	g_cursor = g_track->start[interval];
	g_end = g_track->start[interval + 1u];
}

static void isr_deliver_matching(int event, const void *fn, uint32_t seen)
{
	while (g_cursor < g_end) {
		uint16_t site = g_track->site[g_cursor];
		if (site >= g_track->sites || g_track->nth[g_cursor] != seen)
			return;
		if (event >= 0 ? g_track->site_event[site] != event : g_track->site_fn[site] != fn)
			return;
		g_delivering = 1;
		g_deliver(g_interval, g_track->kind[g_cursor], g_track->ordinal[g_cursor], g_track->value[g_cursor]);
		g_delivering = 0;
		g_cursor++;
		g_placed++;
	}
}

void isr_context_enter(void)
{
	g_context++;
}

void isr_context_leave(void)
{
	g_context--;
}

int isr_in_context(void)
{
	return g_context || g_delivering;
}

void isr_on_entry(const void *fn)
{
	if (!g_track || g_delivering || g_context || g_cursor >= g_end)
		return;
	isr_deliver_matching(-1, fn, isr_bump(fn));
}

void isr_on_site(unsigned site)
{
	if (!g_track || g_delivering || g_context || site >= ISR_SITE_EVENTS)
		return;
	uint32_t seen = ++g_site_counts[site];
	if (g_cursor >= g_end)
		return;
	isr_deliver_matching((int)site, NULL, seen);
}

void isr_close_interval(void)
{
	if (!g_track)
		return;
	g_unplaced += (uint32_t)(g_end - g_cursor);
	g_cursor = g_end;
}
