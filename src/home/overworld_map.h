#ifndef POKETCG_HOME_OVERWORLD_MAP_H
#define POKETCG_HOME_OVERWORLD_MAP_H

#include <stdint.h>

/* >>> factory OverworldMap_ContinuePlayerWalkingAnimation */
void OverworldMap_ContinuePlayerWalkingAnimation(void);
/* <<< factory OverworldMap_ContinuePlayerWalkingAnimation */
/* >>> factory OverworldMap_NegateBC */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
} OverworldMapNegateBCResult;
OverworldMapNegateBCResult OverworldMap_NegateBC(uint8_t b, uint8_t c);
/* <<< factory OverworldMap_NegateBC */
/* >>> factory OverworldMap_InitVolcanoSprite */
void OverworldMap_InitVolcanoSprite(uint8_t f);
/* <<< factory OverworldMap_InitVolcanoSprite */
/* >>> factory OverworldMap_UpdateCursorAnimation */
void OverworldMap_UpdateCursorAnimation(void);
/* <<< factory OverworldMap_UpdateCursorAnimation */
/* >>> factory OverworldMap_LoadSelectedMap */
void OverworldMap_LoadSelectedMap(void);
/* <<< factory OverworldMap_LoadSelectedMap */
/* >>> factory OverworldMap_InitPlayerEastWestMovement */
void OverworldMap_InitPlayerEastWestMovement(uint8_t b, uint8_t c);
/* <<< factory OverworldMap_InitPlayerEastWestMovement */
/* >>> factory OverworldMap_GetOWMapID */
uint8_t OverworldMap_GetOWMapID(void);
/* <<< factory OverworldMap_GetOWMapID */
/* >>> factory OverworldMap_InitCursorSprite */
void OverworldMap_InitCursorSprite(void);
/* <<< factory OverworldMap_InitCursorSprite */
#endif /* POKETCG_HOME_OVERWORLD_MAP_H */
