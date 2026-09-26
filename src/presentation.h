#ifndef POKETCG_PRESENTATION_H
#define POKETCG_PRESENTATION_H

#include <stdint.h>

#include "ppu.h"

typedef enum {
	PRESENTATION_4X3,
	PRESENTATION_SGB_FRAME,
} PresentationMode;

#define PRESENTATION_SGB_WIDTH 256
#define PRESENTATION_SGB_HEIGHT 224

void presentation_render(PresentationMode mode, uint16_t *output,
                         const uint16_t *game);
void presentation_set_border(const uint8_t *border);

#endif
