#ifndef POKETCG_HOME_TILES_H
#define POKETCG_HOME_TILES_H

#include <stdint.h>

void FillRectangle(uint8_t a, uint8_t b, uint8_t c, uint16_t de, uint16_t hl);
void Copy1bppTiles(uint16_t *hl, uint16_t *de);
#endif /* POKETCG_HOME_TILES_H */
