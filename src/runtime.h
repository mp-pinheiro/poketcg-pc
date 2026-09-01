#ifndef POKETCG_RUNTIME_H
#define POKETCG_RUNTIME_H

#include <stddef.h>
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

int runtime_run(struct Shell *shell, uint32_t frame_limit, RuntimeResult *result);
int runtime_run_with_input(
	struct Shell *shell, uint32_t frame_limit,
	const uint8_t *buttons, size_t button_count, RuntimeResult *result);

#endif
