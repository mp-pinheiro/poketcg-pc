#ifndef POKETCG_HOME_SCENES_H
#define POKETCG_HOME_SCENES_H

#include <stdint.h>

void SetMintSinglePalette(uint8_t single);
/* >>> factory SetBoosterLogoOAM */
void SetBoosterLogoOAM(void);
/* <<< factory SetBoosterLogoOAM */
/* >>> factory _LoadScene */
void _LoadScene(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory _LoadScene */
/* >>> factory LoadBoosterGfx */
uint8_t LoadBoosterGfx(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory LoadBoosterGfx */
#endif /* POKETCG_HOME_SCENES_H */
