#ifndef POKETCG_HOME_MAP_H
#define POKETCG_HOME_MAP_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint16_t hl;
} PermissionResult;

typedef struct {
	uint8_t a;
	uint8_t f;
} NPCSearchResult;

PermissionResult GetPermissionByteOfMapPosition(uint8_t b, uint8_t c);
uint8_t GetPermissionOfMapPosition(uint8_t b, uint8_t c);
void SetPermissionOfMapPosition(uint8_t a, uint8_t b, uint8_t c);
uint8_t UpdatePermissionOfMapPosition(uint8_t a, uint8_t b, uint8_t c);
PermissionResult GetLoadedNPCID(uint8_t a);
PermissionResult GetItemInLoadedNPCIndex(uint8_t a, uint8_t l);
uint8_t GameEvent_Overworld(uint8_t f);
void CopyGfxDataFromTempBank(uint16_t *hl, uint16_t *de, uint8_t b, uint8_t c);
typedef struct {
	uint8_t a;
	uint8_t f;
} SongResult;

SongResult PlayDefaultSong(void);
NPCSearchResult FindLoadedNPC(void);
uint8_t GetNextNPCMovementByte(uint16_t bc);
uint8_t GetDefaultSong(void);

/* >>> factory HandleMapWarp */
void HandleMapWarp(void);
/* <<< factory HandleMapWarp */
/* >>> factory GetReceivedLegendaryCards */
typedef struct { uint8_t a; uint8_t f; } GetReceivedLegendaryCardsResult;
GetReceivedLegendaryCardsResult GetReceivedLegendaryCards(void);
/* <<< factory GetReceivedLegendaryCards */
/* >>> factory OverworldDoFrameFunction */
void OverworldDoFrameFunction(void);
/* <<< factory OverworldDoFrameFunction */
/* >>> factory GameEvent_Duel */
uint8_t GameEvent_Duel(void);
/* <<< factory GameEvent_Duel */
/* >>> factory GameEvent_ChallengeMachine */
void GameEvent_ChallengeMachine(void);
/* <<< factory GameEvent_ChallengeMachine */
#endif
