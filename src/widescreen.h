#ifndef POKETCG_WIDESCREEN_H
#define POKETCG_WIDESCREEN_H

#include <stdint.h>

#define WIDESCREEN_OVERWORLD_DO_FRAME 0x380Eu
#define WIDESCREEN_OVERWORLD_MAP 0x00u

typedef struct {
	int x0;
	int x1;
	int room;
} WidescreenRect;

WidescreenRect widescreen_rect(int extra);
WidescreenRect widescreen_apply_viewport(uint16_t *fb, int extra);

#endif
