#ifndef POKETCG_HOME_BG_MAP_H
#define POKETCG_HOME_BG_MAP_H

#include <stdint.h>

void WriteDataBlocksToBGMap0(uint16_t *hl, uint16_t *de, uint8_t *a, uint8_t *b, uint8_t *c);
void WriteDataBlockToBGMap0(uint16_t *hl, uint16_t *de, uint8_t *a, uint8_t *b, uint8_t *c);
void WriteByteToBGMap0(uint8_t a, uint8_t b, uint8_t c);

/* Returns the exit value of a, which is always 0 -- see the note in bg_map.c. */
uint8_t HblankWriteByteToBGMap0(uint8_t a, uint8_t b, uint8_t c);
void CopyDataToBGMap0(uint8_t a, uint16_t *hl, uint16_t *de, uint8_t b, uint8_t c);
void SafeCopyDataHLtoDE(uint16_t *hl, uint16_t *de, uint8_t b);

#endif
