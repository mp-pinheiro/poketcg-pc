#ifndef POKETCG_PALETTES_H
#define POKETCG_PALETTES_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part CopyCGBPalettesResult */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} CopyCGBPalettesResult;
/* <<< part CopyCGBPalettesResult */

/* >>> part FlushAllCGBPalettesResult */
typedef struct {
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} FlushAllCGBPalettesResult;
/* <<< part FlushAllCGBPalettesResult */

/* >>> part FlushPalettesIfRequestedResult */
typedef struct {
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
} FlushPalettesIfRequestedResult;
/* <<< part FlushPalettesIfRequestedResult */

/* >>> factory FlushAllPalettes */
void FlushAllPalettes(void);
/* <<< factory FlushAllPalettes */
/* >>> part FlushPalette */
void FlushPalette(uint8_t a);
/* <<< part FlushPalette */
/* >>> factory SetBGP */
void SetBGP(uint8_t a);
/* <<< factory SetBGP */
/* >>> factory FlushPalette0 */
void FlushPalette0(void);
/* <<< factory FlushPalette0 */
/* >>> factory FlushPalettes */
void FlushPalettes(uint8_t a);
/* <<< factory FlushPalettes */
/* >>> factory SetOBP0 */
void SetOBP0(uint8_t a);
/* <<< factory SetOBP0 */
/* >>> factory SetOBP1 */
void SetOBP1(uint8_t a);
/* <<< factory SetOBP1 */
/* >>> factory FlushPalettesIfRequested */
void FlushPalettesIfRequested(void);
/* <<< factory FlushPalettesIfRequested */
/* >>> part FlushPalettesIfRequested_Registers */
FlushPalettesIfRequestedResult FlushPalettesIfRequested_Registers(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< part FlushPalettesIfRequested_Registers */
/* >>> factory CopyCGBPalettes */
CopyCGBPalettesResult CopyCGBPalettes(uint8_t a, uint8_t b);
/* <<< factory CopyCGBPalettes */
/* >>> factory FlushAllCGBPalettes */
FlushAllCGBPalettesResult FlushAllCGBPalettes(void);
/* <<< factory FlushAllCGBPalettes */

#endif /* POKETCG_PALETTES_H */
