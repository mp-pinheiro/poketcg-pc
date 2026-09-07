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

/* Resume from an injected reference checkpoint instead of booting: skips Start
 * and GameLoop and drives DoFrame directly, so a subsystem the port cannot yet
 * reach on its own can still be exercised. Diagnostic only. */
void runtime_skip_boot(int enable);

int runtime_run(struct Shell *shell, uint32_t frame_limit, RuntimeResult *result);
int runtime_run_with_input(
	struct Shell *shell, uint32_t frame_limit,
	const uint8_t *buttons, size_t button_count, RuntimeResult *result);

#endif
