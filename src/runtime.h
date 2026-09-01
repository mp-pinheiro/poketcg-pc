#ifndef POKETCG_RUNTIME_H
#define POKETCG_RUNTIME_H

#include <stddef.h>
#include "ppu.h"

struct Shell;

typedef struct {
	uint32_t frame_limit;
	uint32_t frames;
	int stopped_by_user;
	uint16_t framebuffer[SCREEN_W * SCREEN_H];
} RuntimeResult;

int runtime_run(struct Shell *shell, uint32_t frame_limit, RuntimeResult *result);
int runtime_run_with_input(
	struct Shell *shell, uint32_t frame_limit,
	const uint8_t *buttons, size_t button_count, RuntimeResult *result);

#endif
