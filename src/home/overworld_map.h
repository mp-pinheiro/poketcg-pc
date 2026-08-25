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
/* >>> factory OverworldMap_GetMapPosition */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t d;
	uint8_t e;
} OverworldMapGetMapPositionResult;

OverworldMapGetMapPositionResult OverworldMap_GetMapPosition(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory OverworldMap_GetMapPosition */
/* >>> factory OverworldMap_SetSpritePosition */
void OverworldMap_SetSpritePosition(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory OverworldMap_SetSpritePosition */
/* >>> factory OverworldMap_InitPlayerNorthSouthMovement */
void OverworldMap_InitPlayerNorthSouthMovement(uint8_t b, uint8_t c);
/* <<< factory OverworldMap_InitPlayerNorthSouthMovement */
/* >>> factory OverworldMap_PrintMapName */
void OverworldMap_PrintMapName(void);
/* <<< factory OverworldMap_PrintMapName */
/* >>> factory OverworldMap_UpdatePlayerAndCursorSprites */
void OverworldMap_UpdatePlayerAndCursorSprites(void);
/* <<< factory OverworldMap_UpdatePlayerAndCursorSprites */
/* >>> factory OverworldMap_InitNextPlayerVelocity */
void OverworldMap_InitNextPlayerVelocity(uint8_t b, uint8_t c);
/* <<< factory OverworldMap_InitNextPlayerVelocity */
/* >>> factory OverworldMap_BeginPlayerMovement */
void OverworldMap_BeginPlayerMovement(void);
/* <<< factory OverworldMap_BeginPlayerMovement */
/* >>> factory OverworldMap_UpdatePlayerWalkingAnimation */
void OverworldMap_UpdatePlayerWalkingAnimation(void);
/* <<< factory OverworldMap_UpdatePlayerWalkingAnimation */
/* >>> factory OverworldMap_HandleDPad */
void OverworldMap_HandleDPad(uint16_t w0, uint16_t w1);
/* <<< factory OverworldMap_HandleDPad */
/* >>> factory OverworldMap_HandleKeyPress */
void OverworldMap_HandleKeyPress(void);
/* <<< factory OverworldMap_HandleKeyPress */
/* >>> factory OverworldMap_Update */
void OverworldMap_Update(void);
/* <<< factory OverworldMap_Update */
#endif /* POKETCG_HOME_OVERWORLD_MAP_H */
