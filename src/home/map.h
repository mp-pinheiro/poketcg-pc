#ifndef POKETCG_HOME_MAP_H
#define POKETCG_HOME_MAP_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part PermissionResult */
typedef struct {
	uint8_t a;
	uint16_t hl;
} PermissionResult;
/* <<< part PermissionResult */

/* >>> part NPCSearchResult */
typedef struct {
	uint8_t a;
	uint8_t f;
} NPCSearchResult;
/* <<< part NPCSearchResult */

/* >>> factory GetPermissionByteOfMapPosition */
PermissionResult GetPermissionByteOfMapPosition(uint8_t b, uint8_t c);
/* <<< factory GetPermissionByteOfMapPosition */
/* >>> factory GetPermissionOfMapPosition */
uint8_t GetPermissionOfMapPosition(uint8_t b, uint8_t c);
/* <<< factory GetPermissionOfMapPosition */
/* >>> factory SetPermissionOfMapPosition */
void SetPermissionOfMapPosition(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory SetPermissionOfMapPosition */
/* >>> factory UpdatePermissionOfMapPosition */
uint8_t UpdatePermissionOfMapPosition(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory UpdatePermissionOfMapPosition */
/* >>> factory GetLoadedNPCID */
PermissionResult GetLoadedNPCID(uint8_t a);
/* <<< factory GetLoadedNPCID */
/* >>> factory GetItemInLoadedNPCIndex */
PermissionResult GetItemInLoadedNPCIndex(uint8_t a, uint8_t l);
/* <<< factory GetItemInLoadedNPCIndex */
/* >>> factory GameEvent_Overworld */
uint8_t GameEvent_Overworld(uint8_t f);
/* <<< factory GameEvent_Overworld */
/* >>> factory CopyGfxDataFromTempBank */
void CopyGfxDataFromTempBank(uint16_t *hl, uint16_t *de, uint8_t b, uint8_t c);
/* <<< factory CopyGfxDataFromTempBank */
/* >>> part SongResult */
typedef struct {
	uint8_t a;
	uint8_t f;
} SongResult;
/* <<< part SongResult */

/* >>> factory PlayDefaultSong */
SongResult PlayDefaultSong(void);
/* <<< factory PlayDefaultSong */
/* >>> factory FindLoadedNPC */
NPCSearchResult FindLoadedNPC(void);
/* <<< factory FindLoadedNPC */
/* >>> factory GetNextNPCMovementByte */
uint8_t GetNextNPCMovementByte(uint16_t bc);
/* <<< factory GetNextNPCMovementByte */
/* >>> factory GetDefaultSong */
uint8_t GetDefaultSong(void);
/* <<< factory GetDefaultSong */

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
uint8_t GameEvent_ChallengeMachine(void);
/* <<< factory GameEvent_ChallengeMachine */
/* >>> factory GameEvent_GiftCenter */
uint8_t GameEvent_GiftCenter(void);
/* <<< factory GameEvent_GiftCenter */
/* >>> factory GameEvent_Credits */
void GameEvent_Credits(void);
/* <<< factory GameEvent_Credits */
/* >>> factory GameEvent_BattleCenter */
uint8_t GameEvent_BattleCenter(void);
/* <<< factory GameEvent_BattleCenter */
/* >>> factory GameEvent_ContinueDuel */
SongResult GameEvent_ContinueDuel(void);
/* <<< factory GameEvent_ContinueDuel */
/* >>> factory _ExecuteGameEvent */
uint8_t _ExecuteGameEvent(void);
/* <<< factory _ExecuteGameEvent */
/* >>> factory ExecuteGameEvent */
void ExecuteGameEvent(void);
/* <<< factory ExecuteGameEvent */
#endif
