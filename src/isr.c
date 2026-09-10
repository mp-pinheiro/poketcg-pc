#include "isr.h"

#include "mem.h"
#include "generated/wram.h"
#include "home/vblank.h"

#include <string.h>

#define ISR_SLOTS 1024u
#define ISR_SLOT_MASK (ISR_SLOTS - 1u)

static const IsrTrack *g_track;
static uint32_t g_interval = UINT32_MAX;
static size_t g_cursor;
static size_t g_end;
static uint8_t g_delivering;
static uint32_t g_placed;
static uint32_t g_unplaced;

static struct {
	const void *fn;
	uint32_t count;
} g_counts[ISR_SLOTS];
static uint16_t g_touched[ISR_SLOTS];
static uint16_t g_touched_count;

void isr_set_track(const IsrTrack *track)
{
	g_track = track && track->count ? track : NULL;
	g_interval = UINT32_MAX;
	g_cursor = 0;
	g_end = 0;
	g_placed = 0;
	g_unplaced = 0;
	g_touched_count = 0;
	memset(g_counts, 0, sizeof g_counts);
	if (g_track)
		isr_begin_interval(0);
}

int isr_active(void)
{
	return g_track != NULL;
}

uint32_t isr_placed(void)
{
	return g_placed;
}

uint32_t isr_unplaced(void)
{
	return g_unplaced;
}

void isr_begin_interval(uint32_t interval);

static void isr_clear_counts(void)
{
	for (uint16_t i = 0; i < g_touched_count; i++)
		g_counts[g_touched[i]].fn = NULL;
	g_touched_count = 0;
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

static void isr_deliver(size_t index)
{
	g_delivering = 1;
	if (g_track->kind[index] == ISR_KIND_VBLANK) {
		RuntimeVBlankHandler();
		gb_write8(wVBlankCounter_ADDR, (uint8_t)(gb_read8(wVBlankCounter_ADDR) + 1u));
	} else {
		(void)RuntimeLCDCHandlerOnce();
	}
	g_delivering = 0;
}

void isr_on_entry(const void *fn)
{
	if (!g_track || g_delivering || g_cursor >= g_end)
		return;
	uint32_t seen = isr_bump(fn);

	while (g_cursor < g_end) {
		uint16_t site = g_track->site[g_cursor];

		if (site >= g_track->sites || g_track->site_fn[site] != fn
		    || g_track->nth[g_cursor] != seen)
			return;
		isr_deliver(g_cursor);
		g_cursor++;
		g_placed++;
	}
}

unsigned isr_close_interval(void)
{
	unsigned remainder = 0;

	if (!g_track)
		return 0;
	while (g_cursor < g_end) {
		if (g_track->kind[g_cursor] == ISR_KIND_VBLANK)
			remainder++;
		isr_deliver(g_cursor);
		g_cursor++;
		g_unplaced++;
	}
	return remainder;
}
