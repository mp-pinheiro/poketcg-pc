#ifndef POKETCG_RUNTIME_H
#define POKETCG_RUNTIME_H

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include "ppu.h"

struct Shell;

typedef enum {
	RUNTIME_EVENT_NONE = 0,
	RUNTIME_EVENT_BOOT_STARTED = 1,
	RUNTIME_EVENT_TITLE_READY = 2,
	RUNTIME_EVENT_START_MENU_READY = 3,
	RUNTIME_EVENT_NEW_GAME_ENTERED = 4,
	RUNTIME_EVENT_OVERWORLD_READY = 5,
} RuntimeEvent;

typedef struct {
	uint32_t frame_limit;
	uint32_t frames;
	uint32_t event_mask;
	uint32_t event_count;
	RuntimeEvent terminal_event;
	int stopped_by_user;
	uint16_t framebuffer[SCREEN_W * SCREEN_H];
} RuntimeResult;

void runtime_events_reset(void);
void runtime_mark_event(RuntimeEvent event);
void runtime_record_event(RuntimeEvent event);
RuntimeEvent runtime_terminal_event(void);
uint32_t runtime_event_mask(void);
uint32_t runtime_event_count(void);

typedef void (*RuntimeStateDumpCb)(uint32_t frame, const RuntimeResult *result);

void runtime_set_state_dump_frames(
	RuntimeStateDumpCb callback, const uint32_t *frames, size_t frame_count);

/* The DoFrame-ordinal lane. Ordinals are 1-based counts of completed DoFrame
 * tails (frame_boundary_doframe_ordinal); the reference stream indexes the same
 * axis, so everything here is comparable ordinal-for-ordinal with no lag.
 *  - ordinal input: entry k-1 is what DoFrame k reads. Never wraps: past the
 *    end, the shell supplies input, which is how a recorded prefix is replayed
 *    at full speed and then handed to a human.
 *  - record: one decimal line per ordinal with the InputFrame byte DoFrame k
 *    read, including ordinals the timeline supplied.
 *  - dump ordinals: state written at the anchor, same callback and naming as
 *    the host-frame dumps.
 *  - stop ordinal: the run ends once that many DoFrames completed. */
void runtime_set_ordinal_input(const uint8_t *buttons, size_t count);
void runtime_set_record_input(FILE *sink);
void runtime_set_state_dump_ordinals(
	RuntimeStateDumpCb callback, const uint32_t *ordinals, size_t count);
void runtime_set_stop_ordinal(uint32_t ordinal);
/* Lag track: for DoFrame k, entry k-1 is (cycles of real time, timer ISRs,
 * VBlank ISRs) the reference spent between anchors k-1 and k, read off the
 * ROM's own counters, plus the ISR schedule of that interval's timer sync
 * points (home/frames.h): call_ticks[call_start[k-1] .. call_start[k]) is,
 * per sync point reached in order, how many of the interval's timer ISRs had
 * fired before it. The host ages the clock by the cycles and runs the VBlank
 * services at the boundary; the timer ISRs run on the game thread, delivered
 * up to each sync point's count there and the remainder at the anchor, so
 * the sound driver and the play-time counter are seen by game code at the
 * same tick as on the ROM and a song-timed wait exits on the same DoFrame.
 * Verification only; live play has no track and no lag. */
typedef struct {
	uint32_t *cycles;
	uint16_t *ticks;
	uint16_t *vblanks;
	uint32_t *call_start; /* count + 1 entries */
	uint16_t *call_ticks;
	uint32_t *write_start; /* count + 1 entries: game writes to wVBlankCounter */
	uint16_t *write_vblanks; /* VBlank ISRs of the interval fired before each write */
	size_t count;
} LagTrack;
void runtime_set_lag_track(const LagTrack *track);
/* Sync points the schedule could not place: the interval reached more or
 * fewer of them than the reference recorded, a different code path. */
uint32_t runtime_lag_schedule_mismatches(void);

/* Resume from an injected reference checkpoint instead of booting: skips Start
 * and GameLoop and drives DoFrame directly, so a subsystem the port cannot yet
 * reach on its own can still be exercised. Diagnostic only. */
void runtime_skip_boot(int enable);

int runtime_run(struct Shell *shell, uint32_t frame_limit, RuntimeResult *result);
int runtime_run_with_input(
	struct Shell *shell, uint32_t frame_limit,
	const uint8_t *buttons, size_t button_count, RuntimeResult *result);

#endif
