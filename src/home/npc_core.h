#ifndef POKETCG_HOME_NPC_CORE_H
#define POKETCG_HOME_NPC_CORE_H

#include <stdint.h>

/* >>> factory CheckIfNPCIsRonald */
uint8_t CheckIfNPCIsRonald(uint8_t a); /* returns the exit flag byte: $90 if Ronald, $80 if a==0, else $00 */
/* <<< factory CheckIfNPCIsRonald */
/* >>> factory UpdateNPCAnimation */
uint8_t UpdateNPCAnimation(void); /* returns the asm's exit a (echo of entry wWhichSprite); f/bc/hl preserved, d/e clobbered by the farcall callee */
/* <<< factory UpdateNPCAnimation */
/* >>> factory ApplyRandomCountToNPCAnim */
uint8_t ApplyRandomCountToNPCAnim(void); /* returns the asm's exit a (echo of entry wWhichSprite); f/bc/hl preserved, d/e clobbered by callees */
/* <<< factory ApplyRandomCountToNPCAnim */
#endif /* POKETCG_HOME_NPC_CORE_H */
