#include "replay.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const unsigned char replay_magic[4] = {'P', 'K', 'R', 'P'};

void replay_init(Replay *replay)
{
	replay->frames = NULL;
	replay->count = 0;
	replay->capacity = 0;
}

void replay_free(Replay *replay)
{
	free(replay->frames);
	replay_init(replay);
}

int replay_push(Replay *replay, InputFrame frame)
{
	if (replay->count == replay->capacity) {
		size_t capacity = replay->capacity ? replay->capacity * 2 : 64;
		InputFrame *frames = realloc(replay->frames, capacity * sizeof *frames);
		if (!frames)
			return -1;
		replay->frames = frames;
		replay->capacity = capacity;
	}
	replay->frames[replay->count++] = frame;
	return 0;
}

int replay_save(const Replay *replay, const char *path)
{
	/* The on-disk count is 32-bit; refuse rather than silently truncate. */
	if (replay->count > UINT32_MAX)
		return -1;
	FILE *file = fopen(path, "wb");
	if (!file)
		return -1;
	uint32_t count = (uint32_t)replay->count;
	int ok = fwrite(replay_magic, 1, sizeof replay_magic, file) == sizeof replay_magic &&
		fputc(1, file) != EOF && fwrite(&count, sizeof count, 1, file) == 1;
	if (ok && count)
		ok = fwrite(replay->frames, sizeof *replay->frames, count, file) == count;
	if (fclose(file) != 0)
		ok = 0;
	return ok ? 0 : -1;
}

int replay_load(Replay *replay, const char *path)
{
	FILE *file = fopen(path, "rb");
	if (!file)
		return -1;
	unsigned char magic[4];
	unsigned char version;
	uint32_t count;
	int ok = fread(magic, 1, sizeof magic, file) == sizeof magic &&
		fread(&version, 1, 1, file) == 1 && fread(&count, sizeof count, 1, file) == 1;
	if (!ok || memcmp(magic, replay_magic, sizeof magic) != 0 || version != 1)
		ok = 0;
	InputFrame *frames = NULL;
	if (ok && count) {
		frames = malloc((size_t)count * sizeof *frames);
		if (!frames || fread(frames, sizeof *frames, count, file) != count)
			ok = 0;
	}
	if (fclose(file) != 0)
		ok = 0;
	if (!ok) {
		free(frames);
		return -1;
	}
	replay_free(replay);
	replay->frames = frames;
	replay->count = count;
	replay->capacity = count;
	return 0;
}

int replay_playback(const Replay *replay, ReplayStep step, void *context)
{
	if (!replay || !step)
		return -1;
	for (size_t i = 0; i < replay->count; i++)
		step(context, replay->frames[i]);
	return 0;
}

int replay_round_trip_run(const Replay *replay, const Snapshot *initial,
	ReplayStep step, void *context, SnapshotReport *report)
{
	Snapshot first, second;
	if (!replay || !initial || !step)
		return -1;
	snapshot_restore(initial);
	if (replay_playback(replay, step, context) != 0)
		return -1;
	snapshot_capture(&first);
	snapshot_restore(initial);
	if (replay_playback(replay, step, context) != 0)
		return -1;
	snapshot_capture(&second);
	return snapshot_compare(&first, &second, NULL, report);
}

int replay_round_trip(const Replay *replay, const Snapshot *initial,
	Snapshot *final_state, SnapshotReport *report)
{
	if (!replay || !initial || !final_state)
		return -1;
	return snapshot_compare(initial, final_state, NULL, report);
}

int replay_write_bug(const Replay *replay, const Snapshot *snapshot,
	SnapshotReport *report)
{
	if (!replay || !snapshot)
		return -1;
	return snapshot_write_bug("saves", snapshot, replay->frames, replay->count, report);
}
