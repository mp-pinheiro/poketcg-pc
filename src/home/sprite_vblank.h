#ifndef POKETCG_HOME_SPRITE_VBLANK_H
#define POKETCG_HOME_SPRITE_VBLANK_H

#include <stdint.h>

uint8_t BackupVBlankFunctionTrampoline(uint16_t *hl, uint16_t *de);

/* >>> factory SetSpriteAnimationsAsVBlankFunction */
void SetSpriteAnimationsAsVBlankFunction(void);
/* <<< factory SetSpriteAnimationsAsVBlankFunction */
/* >>> factory RestoreVBlankFunction */
void RestoreVBlankFunction(void);
/* <<< factory RestoreVBlankFunction */
#endif
