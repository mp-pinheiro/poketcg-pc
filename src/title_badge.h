#ifndef POKETCG_TITLE_BADGE_H
#define POKETCG_TITLE_BADGE_H

#include <stdint.h>

int title_badge_title_visible(const uint16_t *framebuffer);
void title_badge_draw(uint16_t *frame, int stride, int x_offset, const uint16_t *background);

#endif
