#ifndef POKETCG_SNAPSHOT_H
#define POKETCG_SNAPSHOT_H

#include <stddef.h>
#include <stdint.h>

#include "input.h"
#include "mem.h"

enum SnapshotResolveMode {
	RM_BOTH = 0,
	RM_MINE,
	RM_THEIRS,
};

typedef struct {
	uint8_t wram[0x2000];
	uint8_t hram[0x80];
	uint8_t sram[0x8000];
	uint8_t vram[0x4000];
	uint8_t oam[0xA0];
	uint8_t io[0x80];
	uint8_t pal[0x80];
	uint8_t scratch[MEM_SCRATCH_SIZE];
	uint8_t rom_bank;
	uint8_t sram_bank;
	uint8_t vram_bank;
	int sram_enabled;
} Snapshot;

typedef struct {
	const char *region;
	size_t offset;
	uint8_t mine;
	uint8_t theirs;
} SnapshotDifference;

typedef struct {
	int equal;
	SnapshotDifference difference;
} SnapshotReport;

void snapshot_capture(Snapshot *snapshot);
void snapshot_restore(const Snapshot *snapshot);
int snapshot_compare(const Snapshot *mine, const Snapshot *theirs,
	const enum SnapshotResolveMode *modes, SnapshotReport *report);
int snapshot_resolve(Snapshot *mine, Snapshot *theirs,
	const enum SnapshotResolveMode *modes, SnapshotReport *report);
int snapshot_write_bug(const char *directory, const Snapshot *snapshot,
	const InputFrame *frames, size_t frame_count, SnapshotReport *report);

#endif
