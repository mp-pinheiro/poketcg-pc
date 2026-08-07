#ifndef POKETCG_PALETTES_H
#define POKETCG_PALETTES_H

#include <stdint.h>

void FlushAllPalettes(void);
void FlushPalette(uint8_t a);
void SetBGP(uint8_t a);
void FlushPalette0(void);
void FlushPalettes(uint8_t a);
void SetOBP0(uint8_t a);
void SetOBP1(uint8_t a);
void FlushPalettesIfRequested(void);

#endif /* POKETCG_PALETTES_H */
