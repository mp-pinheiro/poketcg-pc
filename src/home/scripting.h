#ifndef POKETCG_HOME_SCRIPTING_H
#define POKETCG_HOME_SCRIPTING_H

#include <stdint.h>

/* >>> factory IncreaseScriptPointer */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t c;
} IncreaseScriptPointerResult;

IncreaseScriptPointerResult IncreaseScriptPointer(uint8_t a);
/* <<< factory IncreaseScriptPointer */

/* >>> factory SetScriptPointer */
uint16_t SetScriptPointer(uint16_t bc);
/* <<< factory SetScriptPointer */

/* >>> factory GetScriptArgsAfterPointer */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
} GetScriptArgsAfterPointerResult;

GetScriptArgsAfterPointerResult GetScriptArgsAfterPointer(uint8_t a);
/* <<< factory GetScriptArgsAfterPointer */

/* >>> factory GetEventVar */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} GetEventVarResult;

GetEventVarResult GetEventVar(uint8_t a, uint8_t f, uint8_t b, uint8_t c);
/* <<< factory GetEventVar */

/* >>> factory IncreaseScriptPointerBy1 */
IncreaseScriptPointerResult IncreaseScriptPointerBy1(void);
/* <<< factory IncreaseScriptPointerBy1 */
/* >>> factory IncreaseScriptPointerBy2 */
IncreaseScriptPointerResult IncreaseScriptPointerBy2(void);
/* <<< factory IncreaseScriptPointerBy2 */
/* >>> factory IncreaseScriptPointerBy4 */
IncreaseScriptPointerResult IncreaseScriptPointerBy4(void);
/* <<< factory IncreaseScriptPointerBy4 */
/* >>> factory IncreaseScriptPointerBy3 */
/* >>> factory IncreaseScriptPointerBy3 */
IncreaseScriptPointerResult IncreaseScriptPointerBy3(void);
/* <<< factory IncreaseScriptPointerBy3 */
/* >>> factory GetScriptArgs5AfterPointer */
GetScriptArgsAfterPointerResult GetScriptArgs5AfterPointer(void);
/* <<< factory GetScriptArgs5AfterPointer */
/* >>> factory SetScriptControlByteFail */
typedef struct {
	uint8_t a;
	uint8_t f;
} SetScriptControlByteFailResult;

SetScriptControlByteFailResult SetScriptControlByteFail(void);
/* <<< factory SetScriptControlByteFail */
/* >>> factory IncreaseScriptPointerBy5 */
IncreaseScriptPointerResult IncreaseScriptPointerBy5(void);
/* <<< factory IncreaseScriptPointerBy5 */
/* >>> factory IncreaseScriptPointerBy6 */
IncreaseScriptPointerResult IncreaseScriptPointerBy6(void);
/* <<< factory IncreaseScriptPointerBy6 */
/* >>> factory IncreaseScriptPointerBy7 */
IncreaseScriptPointerResult IncreaseScriptPointerBy7(void);
/* <<< factory IncreaseScriptPointerBy7 */
/* >>> factory GetScriptArgs2AfterPointer */
GetScriptArgsAfterPointerResult GetScriptArgs2AfterPointer(void);
/* <<< factory GetScriptArgs2AfterPointer */
/* >>> factory GetScriptArgs3AfterPointer */
GetScriptArgsAfterPointerResult GetScriptArgs3AfterPointer(void);
/* <<< factory GetScriptArgs3AfterPointer */
/* >>> factory SetScriptControlBytePass */
uint8_t SetScriptControlBytePass(void);
/* <<< factory SetScriptControlBytePass */
/* >>> factory ScriptCommand_JumpIfCardInCollection */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
} JumpIfCardInCollectionResult;

JumpIfCardInCollectionResult ScriptCommand_JumpIfCardInCollection(uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_JumpIfCardInCollection */
/* >>> factory ScriptCommand_GiveCard */
IncreaseScriptPointerResult ScriptCommand_GiveCard(uint8_t c);
/* <<< factory ScriptCommand_GiveCard */
/* >>> factory ScriptCommand_TakeCard */
IncreaseScriptPointerResult ScriptCommand_TakeCard(uint8_t c);
/* <<< factory ScriptCommand_TakeCard */
/* >>> factory ScriptCommand_PauseSong */
IncreaseScriptPointerResult ScriptCommand_PauseSong(void);
/* <<< factory ScriptCommand_PauseSong */
/* >>> factory ScriptCommand_ResumeSong */
IncreaseScriptPointerResult ScriptCommand_ResumeSong(void);
/* <<< factory ScriptCommand_ResumeSong */
/* >>> factory ScriptCommand_nop */
IncreaseScriptPointerResult ScriptCommand_nop(void);
/* <<< factory ScriptCommand_nop */
/* >>> factory ScriptCommand_OverrideSong */
IncreaseScriptPointerResult ScriptCommand_OverrideSong(uint8_t c);
/* <<< factory ScriptCommand_OverrideSong */
/* >>> factory ScriptCommand_SetDefaultSong */
IncreaseScriptPointerResult ScriptCommand_SetDefaultSong(uint8_t c);
/* <<< factory ScriptCommand_SetDefaultSong */
/* >>> factory ScriptCommand_RecordMasterWin */
IncreaseScriptPointerResult ScriptCommand_RecordMasterWin(uint8_t c);
/* <<< factory ScriptCommand_RecordMasterWin */
/* >>> factory ScriptCommand_ChallengeMachine */
IncreaseScriptPointerResult ScriptCommand_ChallengeMachine(void);
/* <<< factory ScriptCommand_ChallengeMachine */
/* >>> factory ScriptCommand_PlaySong */
IncreaseScriptPointerResult ScriptCommand_PlaySong(uint8_t c);
/* <<< factory ScriptCommand_PlaySong */
/* >>> factory ScriptCommand_PlaySFX */
IncreaseScriptPointerResult ScriptCommand_PlaySFX(uint8_t c);
/* <<< factory ScriptCommand_PlaySFX */
/* >>> factory ScriptCommand_PlayDefaultSong */
IncreaseScriptPointerResult ScriptCommand_PlayDefaultSong(void);
/* <<< factory ScriptCommand_PlayDefaultSong */
/* >>> factory ScriptCommand_SetSpriteAttributes */
/* >>> factory ScriptCommand_SetSpriteAttributes */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t c;
	uint8_t e;
} SetSpriteAttributesResult;

SetSpriteAttributesResult ScriptCommand_SetSpriteAttributes(uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_SetSpriteAttributes */
/* >>> factory ScriptCommand_DoFrames */
/* >>> factory ScriptCommand_DoFrames */
IncreaseScriptPointerResult ScriptCommand_DoFrames(uint8_t c);
/* <<< factory ScriptCommand_DoFrames */
/* >>> factory ScriptCommand_EndScript */
/* >>> factory ScriptCommand_EndScript */
IncreaseScriptPointerResult ScriptCommand_EndScript(void);
/* <<< factory ScriptCommand_EndScript */
/* >>> factory SetNPCDuelParams */
/* >>> factory SetNPCDuelParams */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
} SetNPCDuelParamsResult;

SetNPCDuelParamsResult SetNPCDuelParams(uint8_t b, uint8_t c);
/* <<< factory SetNPCDuelParams */
/* >>> factory ScriptCommand_BattleCenter */
/* >>> factory ScriptCommand_BattleCenter */
IncreaseScriptPointerResult ScriptCommand_BattleCenter(void);
/* <<< factory ScriptCommand_BattleCenter */
/* >>> factory ScriptCommand_LoadCurrentMapNameIntoTxRamSlot */
/* >>> factory ScriptCommand_LoadCurrentMapNameIntoTxRamSlot */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
} ScriptCommand_LoadCurrentMapNameIntoTxRamSlotResult;

ScriptCommand_LoadCurrentMapNameIntoTxRamSlotResult ScriptCommand_LoadCurrentMapNameIntoTxRamSlot(uint8_t c);
/* <<< factory ScriptCommand_LoadCurrentMapNameIntoTxRamSlot */
/* >>> factory ScriptCommand_EnterMap */
/* >>> factory ScriptCommand_EnterMap */
IncreaseScriptPointerResult ScriptCommand_EnterMap(void);
/* <<< factory ScriptCommand_EnterMap */
/* >>> factory GetScriptArgs1AfterPointer */
GetScriptArgsAfterPointerResult GetScriptArgs1AfterPointer(void);
/* <<< factory GetScriptArgs1AfterPointer */
/* >>> factory SetNextScript */
void SetNextScript(uint16_t bc);
/* <<< factory SetNextScript */
/* >>> factory SetEventValue */
typedef struct { uint8_t a; uint8_t f; } SetEventValueResult;
SetEventValueResult SetEventValue(uint8_t a, uint8_t f, uint8_t b, uint8_t c);
/* <<< factory SetEventValue */
/* >>> factory MaxOutEventValue */
SetEventValueResult MaxOutEventValue(uint8_t a, uint8_t f, uint8_t b, uint8_t c);
/* <<< factory MaxOutEventValue */
/* >>> factory ZeroOutEventValue */
SetEventValueResult ZeroOutEventValue(uint8_t a, uint8_t f, uint8_t b, uint8_t c);
/* <<< factory ZeroOutEventValue */
/* >>> factory ClearEvents */
void ClearEvents(void);
/* <<< factory ClearEvents */
/* >>> factory ScriptCommand_Jump */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} ScriptCommand_JumpResult;

ScriptCommand_JumpResult ScriptCommand_Jump(void);
/* <<< factory ScriptCommand_Jump */
/* >>> factory ScriptCommand_MaxOutEventValue */
IncreaseScriptPointerResult ScriptCommand_MaxOutEventValue(uint8_t f, uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_MaxOutEventValue */
/* >>> factory ScriptCommand_ZeroOutEventValue */
IncreaseScriptPointerResult ScriptCommand_ZeroOutEventValue(uint8_t f, uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_ZeroOutEventValue */
/* >>> factory ScriptCommand_SetEventValue */
IncreaseScriptPointerResult ScriptCommand_SetEventValue(uint8_t f, uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_SetEventValue */
/* >>> factory ScriptCommand_TryGivePCPack */
IncreaseScriptPointerResult ScriptCommand_TryGivePCPack(uint8_t c);
/* <<< factory ScriptCommand_TryGivePCPack */
/* >>> factory ScriptCommand_SetActiveNPCCoords */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
} IncreaseScriptPointerResultWithB;

IncreaseScriptPointerResultWithB ScriptCommand_SetActiveNPCCoords(uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_SetActiveNPCCoords */
/* >>> factory ScriptCommand_JumpIfEnoughCardsOwned */
JumpIfCardInCollectionResult ScriptCommand_JumpIfEnoughCardsOwned(uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_JumpIfEnoughCardsOwned */
/* >>> factory ScriptCommand_RemoveAllEnergyCardsFromCollection */
IncreaseScriptPointerResult ScriptCommand_RemoveAllEnergyCardsFromCollection(void);
/* <<< factory ScriptCommand_RemoveAllEnergyCardsFromCollection */
/* >>> factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
} ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult;

ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult ScriptCommand_JumpIfAnyEnergyCardsInCollection(void);
/* <<< factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */
/* >>> factory ScriptCommand_JumpBasedOnFightingClubPupilStatus */
/* >>> factory ScriptCommand_JumpBasedOnFightingClubPupilStatus */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} ScriptCommand_JumpBasedOnFightingClubPupilStatusResult;

ScriptCommand_JumpBasedOnFightingClubPupilStatusResult ScriptCommand_JumpBasedOnFightingClubPupilStatus(void);
/* <<< factory ScriptCommand_JumpBasedOnFightingClubPupilStatus */
/* <<< factory ScriptCommand_JumpBasedOnFightingClubPupilStatus */
/* >>> factory GetEventValue */
uint8_t GetEventValue(uint8_t a);
/* <<< factory GetEventValue */
/* >>> factory GetEventValueBC */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t c;
} GetEventValueBCResult;

GetEventValueBCResult GetEventValueBC(uint8_t b, uint8_t c);
/* <<< factory GetEventValueBC */
/* >>> factory ScriptCommand_JumpIfEventEqual */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} ScriptCommand_JumpIfEventEqualResult;

ScriptCommand_JumpIfEventEqualResult ScriptCommand_JumpIfEventEqual(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory ScriptCommand_JumpIfEventEqual */
/* >>> factory ScriptCommand_JumpIfEventZero */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} ScriptCommand_JumpIfEventZeroResult;

ScriptCommand_JumpIfEventZeroResult ScriptCommand_JumpIfEventZero(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory ScriptCommand_JumpIfEventZero */
/* >>> factory ScriptCommand_JumpIfEventGreaterOrEqual */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} ScriptCommand_JumpIfEventGreaterOrEqualResult;

ScriptCommand_JumpIfEventGreaterOrEqualResult ScriptCommand_JumpIfEventGreaterOrEqual(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory ScriptCommand_JumpIfEventGreaterOrEqual */
/* >>> factory ScriptCommand_JumpIfEventLessThan */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} ScriptCommand_JumpIfEventLessThanResult;

ScriptCommand_JumpIfEventLessThanResult ScriptCommand_JumpIfEventLessThan(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory ScriptCommand_JumpIfEventLessThan */
/* >>> factory ScriptCommand_JumpIfEventNotEqual */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} ScriptCommand_JumpIfEventNotEqualResult;

ScriptCommand_JumpIfEventNotEqualResult ScriptCommand_JumpIfEventNotEqual(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory ScriptCommand_JumpIfEventNotEqual */
/* >>> factory ScriptCommand_JumpIfEventNonzero */
ScriptCommand_JumpIfEventZeroResult ScriptCommand_JumpIfEventNonzero(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory ScriptCommand_JumpIfEventNonzero */
/* >>> factory ScriptCommand_IncrementEventValue */
IncreaseScriptPointerResult ScriptCommand_IncrementEventValue(uint8_t f, uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_IncrementEventValue */
/* >>> factory ScriptCommand_JumpIfPlayerCoordsMatch */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} ScriptCommand_JumpIfPlayerCoordsMatchResult;

ScriptCommand_JumpIfPlayerCoordsMatchResult ScriptCommand_JumpIfPlayerCoordsMatch(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory ScriptCommand_JumpIfPlayerCoordsMatch */
/* >>> factory ScriptCommand_JumpIfActiveNPCCoordsMatch */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} ScriptCommand_JumpIfActiveNPCCoordsMatchResult;

ScriptCommand_JumpIfActiveNPCCoordsMatchResult ScriptCommand_JumpIfActiveNPCCoordsMatch(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory ScriptCommand_JumpIfActiveNPCCoordsMatch */
/* >>> factory SetNextNPCAndScript */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} SetNextNPCAndScriptResult;
SetNextNPCAndScriptResult SetNextNPCAndScript(uint16_t bc, uint16_t hl);
/* <<< factory SetNextNPCAndScript */
/* >>> factory ExecuteNPCMovement */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
} ExecuteNPCMovementResult;

ExecuteNPCMovementResult ExecuteNPCMovement(uint16_t bc);
/* <<< factory ExecuteNPCMovement */
/* >>> factory Func_cdd1 */
IncreaseScriptPointerResult Func_cdd1(void);
/* <<< factory Func_cdd1 */
/* >>> factory ScriptCommand_JumpIfCardOwned */
JumpIfCardInCollectionResult ScriptCommand_JumpIfCardOwned(uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_JumpIfCardOwned */
/* >>> factory ScriptCommand_WaitForSongToFinish */
IncreaseScriptPointerResult ScriptCommand_WaitForSongToFinish(void);
/* <<< factory ScriptCommand_WaitForSongToFinish */
/* >>> factory ScriptCommand_SaveGame */
IncreaseScriptPointerResult ScriptCommand_SaveGame(uint8_t c);
/* <<< factory ScriptCommand_SaveGame */
/* >>> factory ScriptCommand_MoveActiveNPC */
ExecuteNPCMovementResult ScriptCommand_MoveActiveNPC(uint16_t bc);
/* <<< factory ScriptCommand_MoveActiveNPC */
/* >>> factory ScriptCommand_SetNextNPCAndScript */
IncreaseScriptPointerResult ScriptCommand_SetNextNPCAndScript(uint8_t c, uint16_t hl);
/* <<< factory ScriptCommand_SetNextNPCAndScript */
/* >>> factory ScriptCommand_SetActiveNPCDirection */
IncreaseScriptPointerResult ScriptCommand_SetActiveNPCDirection(uint8_t c);
/* <<< factory ScriptCommand_SetActiveNPCDirection */
/* >>> factory ScriptCommand_PlayCredits */
IncreaseScriptPointerResult ScriptCommand_PlayCredits(void);
/* <<< factory ScriptCommand_PlayCredits */
/* >>> factory ScriptCommand_PickChallengeHallOpponent */
IncreaseScriptPointerResult ScriptCommand_PickChallengeHallOpponent(void);
/* <<< factory ScriptCommand_PickChallengeHallOpponent */
/* >>> factory ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot */
IncreaseScriptPointerResult ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot(uint8_t c);
/* <<< factory ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot */
/* >>> factory Func_c998 */
typedef struct { uint8_t a; uint8_t f; } Func_c998Result;
Func_c998Result Func_c998(void);
/* <<< factory Func_c998 */
/* >>> factory DetermineImakuniRoom */
SetEventValueResult DetermineImakuniRoom(void);
/* <<< factory DetermineImakuniRoom */
/* >>> factory ScriptCommand_SetPlayerDirection */
IncreaseScriptPointerResult ScriptCommand_SetPlayerDirection(uint8_t c);
/* <<< factory ScriptCommand_SetPlayerDirection */
/* >>> factory ScriptCommand_UnloadActiveNPC */
IncreaseScriptPointerResult ScriptCommand_UnloadActiveNPC(void);
/* <<< factory ScriptCommand_UnloadActiveNPC */
/* >>> factory ScriptCommand_ReplaceMapBlocks */
IncreaseScriptPointerResult ScriptCommand_ReplaceMapBlocks(uint8_t c);
/* <<< factory ScriptCommand_ReplaceMapBlocks */
/* >>> factory ScriptCommand_GiveStarterDeck */
IncreaseScriptPointerResult ScriptCommand_GiveStarterDeck(void);
/* <<< factory ScriptCommand_GiveStarterDeck */
/* >>> factory ScriptCommand_FlashScreen */
IncreaseScriptPointerResult ScriptCommand_FlashScreen(uint8_t c);
/* <<< factory ScriptCommand_FlashScreen */
/* >>> factory ScriptCommand_MoveActiveNPCByDirection */
ExecuteNPCMovementResult ScriptCommand_MoveActiveNPCByDirection(uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_MoveActiveNPCByDirection */
/* >>> factory ScriptCommand_UnloadChallengeHallNPC */
void ScriptCommand_UnloadChallengeHallNPC(void);
/* <<< factory ScriptCommand_UnloadChallengeHallNPC */
/* >>> factory DetermineChallengeHallEvent */
void DetermineChallengeHallEvent(void);
/* <<< factory DetermineChallengeHallEvent */
/* >>> factory DetermineImakuniAndChallengeHall */
void DetermineImakuniAndChallengeHall(void);
/* <<< factory DetermineImakuniAndChallengeHall */
/* >>> factory ScriptCommand_SetChallengeHallNPCCoords */
IncreaseScriptPointerResult ScriptCommand_SetChallengeHallNPCCoords(uint8_t b, uint8_t c);
/* <<< factory ScriptCommand_SetChallengeHallNPCCoords */
/* >>> factory LoadOverworld */
void LoadOverworld(void);
/* <<< factory LoadOverworld */
#endif
