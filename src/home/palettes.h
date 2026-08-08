#ifndef POKETCG_PALETTES_H
#define POKETCG_PALETTES_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} CopyCGBPalettesResult;

typedef struct {
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} FlushAllCGBPalettesResult;

void FlushAllPalettes(void);
void FlushPalette(uint8_t a);
void SetBGP(uint8_t a);
void FlushPalette0(void);
void FlushPalettes(uint8_t a);
void SetOBP0(uint8_t a);
void SetOBP1(uint8_t a);
void FlushPalettesIfRequested(void);
CopyCGBPalettesResult CopyCGBPalettes(uint8_t a, uint8_t b);
FlushAllCGBPalettesResult FlushAllCGBPalettes(void);

#endif /* POKETCG_PALETTES_H */
