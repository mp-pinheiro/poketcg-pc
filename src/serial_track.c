#include "serial_track.h"

#include "generated/wram.h"
#include "home/serial.h"
#include "mem.h"
#include "isr.h"
#include "link.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

uint8_t g_serial_track_watch[0x10000u >> 3];
int g_serial_track_on;

static struct {
	uint32_t *start;
	uint32_t *access;
	uint8_t *kind;
	uint8_t *value;
	uint32_t *total;
	uint32_t *residue_interval;
	uint8_t *residue;
	uint32_t residues;
	uint32_t residue_cursor;
	uint32_t intervals;
	uint32_t records;
	uint32_t interval;
	uint32_t cursor;
	uint32_t end;
	uint32_t seen;
	uint32_t mismatches;
	uint32_t first_mismatch;
} g_track;

static int read_u32(FILE *file, uint32_t *out)
{
	uint8_t bytes[4];

	if (fread(bytes, 1, sizeof bytes, file) != sizeof bytes)
		return -1;
	*out = (uint32_t)bytes[0] | (uint32_t)bytes[1] << 8 | (uint32_t)bytes[2] << 16 | (uint32_t)bytes[3] << 24;
	return 0;
}

static int read_u16(FILE *file, uint16_t *out)
{
	uint8_t bytes[2];

	if (fread(bytes, 1, sizeof bytes, file) != sizeof bytes)
		return -1;
	*out = (uint16_t)(bytes[0] | bytes[1] << 8);
	return 0;
}

void serial_track_free(void)
{
	free(g_track.start);
	free(g_track.access);
	free(g_track.kind);
	free(g_track.value);
	free(g_track.total);
	free(g_track.residue_interval);
	free(g_track.residue);
	memset(&g_track, 0, sizeof g_track);
	memset(g_serial_track_watch, 0, sizeof g_serial_track_watch);
	g_serial_track_on = 0;
}

int serial_track_load(const char *path)
{
	FILE *file = fopen(path, "rb");
	char magic[4];
	uint16_t addresses;
	uint32_t previous = 0;

	if (!file)
		return -1;
	serial_track_free();
	if (fread(magic, 1, sizeof magic, file) != sizeof magic || memcmp(magic, "SRL1", 4) != 0 ||
	    read_u16(file, &addresses) != 0)
		goto fail;
	for (uint16_t i = 0; i < addresses; i++) {
		uint16_t address;

		if (read_u16(file, &address) != 0)
			goto fail;
		g_serial_track_watch[address >> 3] |= (uint8_t)(1u << (address & 7u));
	}
	if (read_u32(file, &g_track.records) != 0)
		goto fail;
	g_track.access = malloc(((size_t)g_track.records + 1u) * sizeof *g_track.access);
	g_track.kind = malloc((size_t)g_track.records + 1u);
	g_track.value = malloc((size_t)g_track.records + 1u);
	uint32_t *interval_of = malloc(((size_t)g_track.records + 1u) * sizeof *interval_of);
	if (!g_track.access || !g_track.kind || !g_track.value || !interval_of) {
		free(interval_of);
		goto fail;
	}
	for (uint32_t i = 0; i < g_track.records; i++) {
		uint8_t tail[2];

		if (read_u32(file, &interval_of[i]) != 0 || read_u32(file, &g_track.access[i]) != 0 ||
		    fread(tail, 1, sizeof tail, file) != sizeof tail || interval_of[i] < previous) {
			free(interval_of);
			goto fail;
		}
		previous = interval_of[i];
		g_track.kind[i] = tail[0];
		g_track.value[i] = tail[1];
	}
	if (read_u32(file, &g_track.intervals) != 0) {
		free(interval_of);
		goto fail;
	}
	g_track.total = malloc(((size_t)g_track.intervals + 1u) * sizeof *g_track.total);
	g_track.start = malloc(((size_t)g_track.intervals + 2u) * sizeof *g_track.start);
	if (!g_track.total || !g_track.start) {
		free(interval_of);
		goto fail;
	}
	for (uint32_t i = 0; i < g_track.intervals; i++) {
		if (read_u32(file, &g_track.total[i]) != 0) {
			free(interval_of);
			goto fail;
		}
	}
	if (read_u32(file, &g_track.residues) != 0) {
		free(interval_of);
		goto fail;
	}
	g_track.residue_interval = malloc(((size_t)g_track.residues + 1u) * sizeof *g_track.residue_interval);
	g_track.residue = malloc(((size_t)g_track.residues + 1u) * 8u);
	if (!g_track.residue_interval || !g_track.residue) {
		free(interval_of);
		goto fail;
	}
	for (uint32_t i = 0; i < g_track.residues; i++) {
		if (read_u32(file, &g_track.residue_interval[i]) != 0 ||
		    fread(g_track.residue + (size_t)i * 8u, 1, 8u, file) != 8u) {
			free(interval_of);
			goto fail;
		}
	}
	uint32_t record = 0;
	for (uint32_t interval = 0; interval <= g_track.intervals; interval++) {
		g_track.start[interval] = record;
		while (record < g_track.records && interval_of[record] == interval)
			record++;
	}
	g_track.start[g_track.intervals + 1u] = g_track.records;
	free(interval_of);
	fclose(file);
	g_serial_track_on = 1;
	serial_track_begin_interval(0);
	return 0;
fail:
	fclose(file);
	serial_track_free();
	return -1;
}

static void mismatch(void)
{
	if (!g_track.mismatches)
		g_track.first_mismatch = g_track.interval;
	g_track.mismatches++;
}

void serial_track_begin_interval(uint32_t interval)
{
	if (!g_serial_track_on)
		return;
	g_track.interval = interval;
	g_track.seen = 0;
	if (interval >= g_track.intervals) {
		g_track.cursor = g_track.end = g_track.records;
		return;
	}
	g_track.cursor = g_track.start[interval];
	g_track.end = g_track.start[interval + 1u];
}

#define rSC 0xFF02u
#define SERIAL_TIMER_LEVELS 8u

static struct {
	uint8_t a[SERIAL_TIMER_LEVELS];
	uint8_t z[SERIAL_TIMER_LEVELS];
	uint8_t next[SERIAL_TIMER_LEVELS];
	unsigned depth;
} g_timer;

static void timer_step(uint8_t step)
{
	unsigned level;
	uint8_t next = 0u;

	if (step == 0x9Du || step == 0xAAu) {
		if (g_timer.depth == SERIAL_TIMER_LEVELS) {
			mismatch();
			return;
		}
		level = g_timer.depth++;
	} else {
		if (g_timer.depth == 0u || g_timer.next[g_timer.depth - 1u] != step) {
			mismatch();
			return;
		}
		level = g_timer.depth - 1u;
	}
	uint8_t *a = &g_timer.a[level];

	switch (step) {
	case 0x9Du:
		*a = gb_read8(rSC);
		if (!(*a & 0x80u))
			next = 0xA3u;
		break;
	case 0xA3u:
		gb_write8(rSC, 0x01u);
		next = 0xA7u;
		break;
	case 0xA7u:
		gb_write8(rSC, 0x81u);
		break;
	case 0xAAu:
		*a = gb_read8(wSerialCounter_ADDR);
		next = 0xB0u;
		break;
	case 0xB0u:
		g_timer.z[level] = *a == gb_read8(wSerialCounter2_ADDR);
		next = 0xB1u;
		break;
	case 0xB1u:
		gb_write8(wSerialCounter2_ADDR, *a);
		next = g_timer.z[level] ? 0xB7u : 0xC2u;
		break;
	case 0xB7u:
		gb_write8(wSerialTimeoutCounter_ADDR, (uint8_t)(gb_read8(wSerialTimeoutCounter_ADDR) + 1u));
		next = 0xB8u;
		break;
	case 0xB8u:
		*a = gb_read8(wSerialTimeoutCounter_ADDR);
		if (*a >= 4u)
			next = 0xBFu;
		break;
	case 0xBFu:
		gb_write8(wSerialFlags_ADDR, (uint8_t)(gb_read8(wSerialFlags_ADDR) | 0x80u));
		break;
	case 0xC2u:
		gb_write8(wSerialTimeoutCounter_ADDR, 0u);
		break;
	}
	if (next)
		g_timer.next[level] = next;
	else
		g_timer.depth = level;
}

static void deliver(uint32_t index)
{
	isr_context_enter();
	if (g_track.kind[index] == SERIAL_TRACK_TRANSFER)
		link_replay_serial(g_track.value[index]);
	else
		timer_step(g_track.value[index]);
	isr_context_leave();
}

void serial_track_access(void)
{
	if (isr_in_context())
		return;
	g_track.seen++;
	while (g_track.cursor < g_track.end && g_track.access[g_track.cursor] == g_track.seen)
		deliver(g_track.cursor++);
}

void serial_track_anchor(void)
{
	if (!g_serial_track_on)
		return;
	while (g_track.cursor < g_track.end && g_track.access[g_track.cursor] == UINT32_MAX)
		deliver(g_track.cursor++);
	if (g_track.interval < g_track.intervals &&
	    (g_track.cursor != g_track.end || g_track.seen != g_track.total[g_track.interval]))
		mismatch();
}

void serial_track_residue(uint8_t known, uint8_t bytes[8])
{
	static const uint8_t slot_bit[8] = {0x02u, 0x01u, 0x80u, 0x40u, 0x20u, 0x10u, 0x08u, 0x04u};

	if (!g_serial_track_on)
		return;
	while (g_track.residue_cursor < g_track.residues &&
	       g_track.residue_interval[g_track.residue_cursor] < g_track.interval) {
		g_track.residue_cursor++;
		mismatch();
	}
	if (g_track.residue_cursor >= g_track.residues ||
	    g_track.residue_interval[g_track.residue_cursor] != g_track.interval) {
		mismatch();
		return;
	}
	const uint8_t *recorded = g_track.residue + (size_t)g_track.residue_cursor * 8u;
	g_track.residue_cursor++;
	for (unsigned i = 0; i < 8u; i++) {
		if (!(known & slot_bit[i]))
			bytes[i] = recorded[i];
	}
}

uint32_t serial_track_mismatches(void)
{
	return g_track.mismatches;
}

uint32_t serial_track_first_mismatch(void)
{
	return g_track.first_mismatch;
}
