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
/* >>> factory UpdateNPCPosition */
uint8_t UpdateNPCPosition(void);
/* <<< factory UpdateNPCPosition */
/* >>> factory UpdateNPCSpritePosition */
typedef struct { uint8_t a; uint8_t f; } UpdateNPCSpritePositionResult;
UpdateNPCSpritePositionResult UpdateNPCSpritePosition(uint16_t hl);
/* <<< factory UpdateNPCSpritePosition */
/* >>> factory CheckIsAnNPCMoving */
typedef struct { uint8_t a; uint8_t f; } CheckIsAnNPCMovingResult;
CheckIsAnNPCMovingResult CheckIsAnNPCMoving(void);
/* <<< factory CheckIsAnNPCMoving */
/* >>> factory UpdateNPCsTilePermission */
uint8_t UpdateNPCsTilePermission(void);
/* <<< factory UpdateNPCsTilePermission */
/* >>> factory SetNPCsTilePermission */
uint8_t SetNPCsTilePermission(void);
/* <<< factory SetNPCsTilePermission */
/* >>> factory SetNPCPosition */
uint8_t SetNPCPosition(uint8_t b, uint8_t c);
/* <<< factory SetNPCPosition */
#endif /* POKETCG_HOME_NPC_CORE_H */
