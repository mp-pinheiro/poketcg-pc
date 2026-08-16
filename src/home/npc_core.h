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
/* >>> factory SetNPCAnimation */
uint8_t SetNPCAnimation(uint8_t a); /* a = new animation; bc/hl preserved, returns exit a */
/* <<< factory SetNPCAnimation */
/* >>> factory SetNPCDirection */
uint8_t SetNPCDirection(uint8_t a); /* a = new direction; hl preserved, returns exit a */
/* <<< factory SetNPCDirection */
/* >>> factory StartNPCMovement */
uint8_t StartNPCMovement(uint16_t *bc); /* npc_core.asm:618; bc = movement script pointer in/out (asm leaves it at its exit position); returns exit a (stop path: GetItemInLoadedNPCIndex's a) */
/* <<< factory StartNPCMovement */
/* >>> factory Func_1c5e9 */
uint8_t Func_1c5e9(void);
/* <<< factory Func_1c5e9 */
#endif /* POKETCG_HOME_NPC_CORE_H */
