#include "snapshot.h"

#include "mem.h"

#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>

struct SnapshotRegion {
	const char *name;
	unsigned char *mine;
	unsigned char *theirs;
	size_t size;
};

static size_t snapshot_regions(Snapshot *mine, const Snapshot *theirs,
	struct SnapshotRegion regions[12])
{
	regions[0] = (struct SnapshotRegion){"wram", mine->wram, (unsigned char *)theirs->wram, sizeof mine->wram};
	regions[1] = (struct SnapshotRegion){"hram", mine->hram, (unsigned char *)theirs->hram, sizeof mine->hram};
	regions[2] = (struct SnapshotRegion){"sram", mine->sram, (unsigned char *)theirs->sram, sizeof mine->sram};
	regions[3] = (struct SnapshotRegion){"vram", mine->vram, (unsigned char *)theirs->vram, sizeof mine->vram};
	regions[4] = (struct SnapshotRegion){"oam", mine->oam, (unsigned char *)theirs->oam, sizeof mine->oam};
	regions[5] = (struct SnapshotRegion){"io", mine->io, (unsigned char *)theirs->io, sizeof mine->io};
	regions[6] = (struct SnapshotRegion){"pal", mine->pal, (unsigned char *)theirs->pal, sizeof mine->pal};
	regions[7] = (struct SnapshotRegion){"rom_bank", &mine->rom_bank, (unsigned char *)&theirs->rom_bank, 1};
	regions[8] = (struct SnapshotRegion){"sram_bank", &mine->sram_bank, (unsigned char *)&theirs->sram_bank, 1};
	regions[9] = (struct SnapshotRegion){"vram_bank", &mine->vram_bank, (unsigned char *)&theirs->vram_bank, 1};
	regions[10] = (struct SnapshotRegion){"sram_enabled", (unsigned char *)&mine->sram_enabled,
		(unsigned char *)&theirs->sram_enabled, sizeof mine->sram_enabled};
	regions[11] = (struct SnapshotRegion){"scratch", mine->scratch, (unsigned char *)theirs->scratch, sizeof mine->scratch};
	return 12;
}

void snapshot_capture(Snapshot *snapshot)
{
	memcpy(snapshot->wram, g_wram, sizeof snapshot->wram);
	memcpy(snapshot->hram, g_hram, sizeof snapshot->hram);
	memcpy(snapshot->sram, g_sram, sizeof snapshot->sram);
	memcpy(snapshot->vram, g_vram, sizeof snapshot->vram);
	memcpy(snapshot->oam, g_oam, sizeof snapshot->oam);
	memcpy(snapshot->io, g_io, sizeof snapshot->io);
	memcpy(snapshot->pal, g_pal, sizeof snapshot->pal);
	memcpy(snapshot->scratch, g_scratch, sizeof snapshot->scratch);
	snapshot->rom_bank = g_rom_bank;
	snapshot->sram_bank = g_sram_bank;
	snapshot->vram_bank = g_vram_bank;
	snapshot->sram_enabled = g_sram_enabled;
}

void snapshot_restore(const Snapshot *snapshot)
{
	memcpy(g_wram, snapshot->wram, sizeof g_wram);
	memcpy(g_hram, snapshot->hram, sizeof g_hram);
	memcpy(g_sram, snapshot->sram, sizeof g_sram);
	memcpy(g_vram, snapshot->vram, sizeof g_vram);
	memcpy(g_oam, snapshot->oam, sizeof g_oam);
	memcpy(g_io, snapshot->io, sizeof g_io);
	memcpy(g_pal, snapshot->pal, sizeof g_pal);
	memcpy(g_scratch, snapshot->scratch, sizeof g_scratch);
	g_rom_bank = snapshot->rom_bank;
	g_sram_bank = snapshot->sram_bank;
	g_vram_bank = snapshot->vram_bank;
	g_sram_enabled = snapshot->sram_enabled;
}

static int compare_regions(const Snapshot *mine, const Snapshot *theirs,
	const enum SnapshotResolveMode *modes, SnapshotReport *report)
{
	struct SnapshotRegion regions[12];
	Snapshot copy = *mine;
	size_t count = snapshot_regions(&copy, theirs, regions);
	if (report) {
		report->equal = 1;
		report->difference = (SnapshotDifference){0};
	}
	for (size_t i = 0; i < count; i++) {
		enum SnapshotResolveMode mode = modes ? modes[i] : RM_BOTH;
		if (mode != RM_BOTH)
			continue;
		for (size_t j = 0; j < regions[i].size; j++) {
			if (regions[i].mine[j] == regions[i].theirs[j])
				continue;
			if (report) {
				report->equal = 0;
				report->difference = (SnapshotDifference){regions[i].name, j,
					regions[i].mine[j], regions[i].theirs[j]};
			}
			return 1;
		}
	}
	return 0;
}

int snapshot_compare(const Snapshot *mine, const Snapshot *theirs,
	const enum SnapshotResolveMode *modes, SnapshotReport *report)
{
	return compare_regions(mine, theirs, modes, report);
}

int snapshot_resolve(Snapshot *mine, Snapshot *theirs,
	const enum SnapshotResolveMode *modes, SnapshotReport *report)
{
	struct SnapshotRegion regions[12];
	size_t count = snapshot_regions(mine, theirs, regions);
	int dirty = 0;
	if (report) {
		report->equal = 1;
		report->difference = (SnapshotDifference){0};
	}
	for (size_t i = 0; i < count; i++) {
		enum SnapshotResolveMode mode = modes ? modes[i] : RM_BOTH;
		if (mode == RM_MINE) {
			memcpy(regions[i].theirs, regions[i].mine, regions[i].size);
			continue;
		}
		if (mode == RM_THEIRS) {
			memcpy(regions[i].mine, regions[i].theirs, regions[i].size);
			continue;
		}
		for (size_t j = 0; j < regions[i].size; j++) {
			if (regions[i].mine[j] == regions[i].theirs[j])
				continue;
			if (!dirty && report)
				*report = (SnapshotReport){0, {regions[i].name, j, regions[i].mine[j], regions[i].theirs[j]}};
			dirty = 1;
		}
	}
	return dirty;
}

static int write_snapshot(FILE *file, const Snapshot *snapshot)
{
	struct SnapshotRegion regions[12];
	Snapshot zero = {0};
	size_t count = snapshot_regions(&zero, snapshot, regions);
	for (size_t i = 0; i < count; i++)
		if (fwrite(regions[i].theirs, 1, regions[i].size, file) != regions[i].size)
			return -1;
	return 0;
}

int snapshot_write_bug(const char *directory, const Snapshot *snapshot,
	const InputFrame *frames, size_t frame_count, SnapshotReport *report)
{
	char path[512];
	if (mkdir(directory, 0755) != 0 && errno != EEXIST) {
		fprintf(stderr, "snapshot: mkdir %s: %s\n", directory, strerror(errno));
		return -1;
	}
	for (unsigned int suffix = 0; suffix < 1000; suffix++) {
		long long stamp = (long long)time(NULL);
		if (suffix)
			snprintf(path, sizeof path, "%s/bug-%lld-%u.sav", directory, stamp, suffix);
		else
			snprintf(path, sizeof path, "%s/bug-%lld.sav", directory, stamp);
		FILE *file = fopen(path, "wx");
		if (!file && errno == EEXIST)
			continue;
		if (!file) {
			fprintf(stderr, "snapshot: open %s: %s\n", path, strerror(errno));
			return -1;
		}
		uint32_t count = (uint32_t)frame_count;
		int ok = fwrite("PKSV", 1, 4, file) == 4 && fwrite("\1", 1, 1, file) == 1 &&
			fwrite(&count, sizeof count, 1, file) == 1;
		if (ok)
			for (size_t i = 0; i < frame_count; i++)
				ok = fwrite(&frames[i], sizeof frames[i], 1, file) == 1;
		if (ok)
			ok = write_snapshot(file, snapshot) == 0;
		if (fclose(file) != 0)
			ok = 0;
		if (!ok) {
			fprintf(stderr, "snapshot: write %s: %s\n", path, strerror(errno));
			return -1;
		}
		return 0;
	}
	fprintf(stderr, "snapshot: no unused bug filename\n");
	(void)report;
	return -1;
}
