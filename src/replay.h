#ifndef POKETCG_REPLAY_H
#define POKETCG_REPLAY_H

#include <stddef.h>

#include "input.h"
#include "snapshot.h"

typedef struct {
	InputFrame *frames;
	size_t count;
	size_t capacity;
} Replay;
#define REPLAY_FORMAT_VERSION 2u
typedef void (*ReplayStep)(void *context, InputFrame frame);

int replay_playback(const Replay *replay, ReplayStep step, void *context);
int replay_round_trip_run(const Replay *replay, const Snapshot *initial,
	ReplayStep step, void *context, SnapshotReport *report);

void replay_init(Replay *replay);
void replay_free(Replay *replay);
int replay_push(Replay *replay, InputFrame frame);
int replay_save(const Replay *replay, const char *path);
int replay_load(Replay *replay, const char *path);
int replay_round_trip(const Replay *replay, const Snapshot *initial,
	Snapshot *final_state, SnapshotReport *report);
int replay_write_bug(const Replay *replay, const Snapshot *snapshot,
	SnapshotReport *report);

#endif
