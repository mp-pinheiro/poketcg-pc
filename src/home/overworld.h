#ifndef POKETCG_HOME_OVERWORLD_H
#define POKETCG_HOME_OVERWORLD_H

#include <stdint.h>

/* >>> factory Func_c6cc */
uint8_t Func_c6cc(uint8_t a);
/* <<< factory Func_c6cc */
/* >>> factory Func_c6d4 */
uint8_t Func_c6d4(uint8_t a);
/* <<< factory Func_c6d4 */
/* >>> factory Func_c6f7 */
uint8_t Func_c6f7(uint16_t *hl);
/* <<< factory Func_c6f7 */
/* >>> factory SetOverworldNPCFlags */
typedef struct {
	uint8_t a;
	uint8_t f;
} OverworldNPCFlagsResult;
OverworldNPCFlagsResult SetOverworldNPCFlags(uint8_t a);
/* <<< factory SetOverworldNPCFlags */
/* >>> factory Func_c158 */
uint8_t Func_c158(void);
/* <<< factory Func_c158 */
/* >>> factory Func_c184 */
void Func_c184(void);
/* <<< factory Func_c184 */
/* >>> factory WhiteOutDMGPals */
void WhiteOutDMGPals(void);
/* <<< factory WhiteOutDMGPals */
/* >>> factory Func_c1f8 */
void Func_c1f8(void);
/* <<< factory Func_c1f8 */
/* >>> factory BackupPlayerPosition */
void BackupPlayerPosition(void);
/* <<< factory BackupPlayerPosition */
/* >>> factory Func_c469 */
void Func_c469(void);
/* <<< factory Func_c469 */
/* >>> factory SetScreenScrollWram */
uint8_t SetScreenScrollWram(void);
/* <<< factory SetScreenScrollWram */
/* >>> factory SetScreenScroll */
void SetScreenScroll(void);
/* <<< factory SetScreenScroll */
/* >>> factory Func_c70d */
typedef struct {
	uint8_t a;
	uint8_t f;
} FuncC70dResult;

FuncC70dResult Func_c70d(void);
/* <<< factory Func_c70d */
/* >>> factory Func_c430 */
void Func_c430(void);
/* <<< factory Func_c430 */
/* >>> factory Func_c41c */
void Func_c41c(void);
/* <<< factory Func_c41c */
/* >>> factory Func_c3ca */
typedef struct {
	uint8_t a;
	uint8_t f;
} FuncC3caResult;

FuncC3caResult Func_c3ca(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory Func_c3ca */
/* >>> factory GetDirectionFromDPad */
typedef struct {
	uint8_t a;
	uint8_t f;
} GetDirectionFromDPadResult;

GetDirectionFromDPadResult GetDirectionFromDPad(uint8_t a);
/* <<< factory GetDirectionFromDPad */
/* >>> factory Func_c694 */
void Func_c694(uint8_t a, uint8_t c);
/* <<< factory Func_c694 */
/* >>> factory FindPlayerMovementWithOffset */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
} FindPlayerMovementWithOffsetResult;
FindPlayerMovementWithOffsetResult FindPlayerMovementWithOffset(uint8_t a);
/* <<< factory FindPlayerMovementWithOffset */
/* >>> factory BackupObjectPalettes */
void BackupObjectPalettes(void);
/* <<< factory BackupObjectPalettes */
/* >>> factory AttemptPlayerMovement */
void AttemptPlayerMovement(uint8_t b, uint8_t c);
/* <<< factory AttemptPlayerMovement */
/* >>> factory FindPlayerMovementFromDirection */
FindPlayerMovementWithOffsetResult FindPlayerMovementFromDirection(void);
/* <<< factory FindPlayerMovementFromDirection */
/* >>> factory Func_c1a0 */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} FuncC1A0Result;
FuncC1A0Result Func_c1a0(uint16_t hl);
/* <<< factory Func_c1a0 */
/* >>> factory PauseMenu_Exit */
void PauseMenu_Exit(void);
/* <<< factory PauseMenu_Exit */
/* >>> factory AttemptPlayerMovementFromDirection */
void AttemptPlayerMovementFromDirection(void);
/* <<< factory AttemptPlayerMovementFromDirection */
/* >>> factory Func_c687 */
void Func_c687(void);
/* <<< factory Func_c687 */
/* >>> factory Func_c36a */
void Func_c36a(void);
/* <<< factory Func_c36a */
/* >>> factory Func_c915 */
FuncC3caResult Func_c915(void);
/* <<< factory Func_c915 */
/* >>> factory StartScriptedMovement */
void StartScriptedMovement(void);
/* <<< factory StartScriptedMovement */
/* >>> factory RestoreObjectPalettes */
void RestoreObjectPalettes(void);
/* <<< factory RestoreObjectPalettes */
/* >>> factory Func_c3ff */
void Func_c3ff(void);
/* <<< factory Func_c3ff */
/* >>> factory Func_c49c */
void Func_c49c(void);
/* <<< factory Func_c49c */
/* >>> factory Func_c58b */
void Func_c58b(void);
/* <<< factory Func_c58b */
/* >>> factory UpdatePlayerSprite */
void UpdatePlayerSprite(void);
/* <<< factory UpdatePlayerSprite */
/* >>> factory UpdatePlayerDirection */
void UpdatePlayerDirection(uint8_t a);
/* <<< factory UpdatePlayerDirection */
/* >>> factory UpdatePlayerDirectionFromDPad */
void UpdatePlayerDirectionFromDPad(uint8_t a);
/* <<< factory UpdatePlayerDirectionFromDPad */
/* >>> factory SetOverworldDoFrameFunction */
void SetOverworldDoFrameFunction(void);
/* <<< factory SetOverworldDoFrameFunction */
/* >>> factory Func_c3ee */
void Func_c3ee(void);
/* <<< factory Func_c3ee */
/* >>> factory Func_c66c */
void Func_c66c(void);
/* <<< factory Func_c66c */
/* >>> factory Func_c4b9 */
void Func_c4b9(void);
/* <<< factory Func_c4b9 */
/* >>> factory DecompressPermissionMap */
typedef struct { uint16_t hl; uint8_t d; uint8_t e; } DecompressPermissionMapResult;
DecompressPermissionMapResult DecompressPermissionMap(uint16_t hl);
/* <<< factory DecompressPermissionMap */
/* >>> factory LoadPermissionMap */
void LoadPermissionMap(void);
/* <<< factory LoadPermissionMap */
/* >>> factory Func_c1ed */
void Func_c1ed(void);
/* <<< factory Func_c1ed */
/* >>> factory Func_c1b1 */
void Func_c1b1(void);
/* <<< factory Func_c1b1 */
/* >>> factory Func_c554 */
void Func_c554(void);
/* <<< factory Func_c554 */
/* >>> factory Func_c280 */
void Func_c280(void);
/* <<< factory Func_c280 */
/* >>> factory UpdateOverworldMap */
void UpdateOverworldMap(void);
/* <<< factory UpdateOverworldMap */
/* >>> factory DisplayPauseMenu */
void DisplayPauseMenu(void);
/* <<< factory DisplayPauseMenu */
/* >>> factory Func_c8ed */
typedef struct { uint8_t a; uint8_t f; } FuncC8edResult;
FuncC8edResult Func_c8ed(uint16_t hl);
/* <<< factory Func_c8ed */
/* >>> factory PauseMenu_Diary */
void PauseMenu_Diary(void);
/* <<< factory PauseMenu_Diary */
/* >>> factory DisplayPCMenu */
void DisplayPCMenu(void);
void BankswitchROM(uint8_t bank);
/* <<< factory DisplayPCMenu */
/* >>> factory Func_c268 */
void Func_c268(void);
/* <<< factory Func_c268 */
/* >>> factory PauseMenu_Status */
void PauseMenu_Status(void);
/* <<< factory PauseMenu_Status */
/* >>> factory Func_c258 */
void Func_c258(void);
/* <<< factory Func_c258 */
/* >>> factory Func_c251 */
/* >>> factory Func_c251 */
void Func_c251(void);
/* <<< factory Func_c251 */
/* >>> factory Func_c241 */
void Func_c241(void);
/* <<< factory Func_c241 */
/* >>> factory Func_c141 */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } Func_c141Result;
Func_c141Result Func_c141(void);
/* <<< factory Func_c141 */
/* >>> factory CloseTextBox */
void CloseTextBox(void);
/* <<< factory CloseTextBox */
/* >>> factory Func_c891 */
void Func_c891(uint16_t hl);
/* <<< factory Func_c891 */
/* >>> factory ReturnToOverworld */
uint8_t ReturnToOverworld(void);
/* <<< factory ReturnToOverworld */
/* >>> factory CloseAdvancedDialogueBox */
void CloseAdvancedDialogueBox(void);
/* <<< factory CloseAdvancedDialogueBox */
/* >>> factory Func_c8ba */
/* >>> factory Func_c8ba */
void Func_c8ba(uint16_t hl, uint16_t de);
/* <<< factory Func_c8ba */
/* >>> factory ReturnToOverworldNoCallback */
uint8_t ReturnToOverworldNoCallback(void);
/* <<< factory ReturnToOverworldNoCallback */
/* >>> factory ReturnToOverworldWithCallback */
uint8_t ReturnToOverworldWithCallback(uint16_t hl);
/* <<< factory ReturnToOverworldWithCallback */
/* >>> factory FindNPCOrObject */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} FindNPCOrObjectResult;

FindNPCOrObjectResult FindNPCOrObject(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory FindNPCOrObject */
/* >>> factory Func_c6dc */
/* >>> factory Func_c6dc */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t c;
	uint16_t hl;
} FuncC6dcResult;
FuncC6dcResult Func_c6dc(uint16_t saved_hl);
/* <<< factory Func_c6dc */
/* >>> factory HandlePlayerMoveModeInput */
void HandlePlayerMoveModeInput(void);
/* <<< factory HandlePlayerMoveModeInput */
/* >>> factory PCMenu_Glossary */
void PCMenu_Glossary(void);
/* <<< factory PCMenu_Glossary */
/* >>> factory Func_c17a */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} FuncC17aResult;

FuncC17aResult Func_c17a(uint16_t hl);
/* <<< factory Func_c17a */
/* >>> factory Func_c53d */
void Func_c53d(void);
/* <<< factory Func_c53d */
/* >>> factory PCMenu_CardAlbum */
void PCMenu_CardAlbum(void);
/* <<< factory PCMenu_CardAlbum */
/* >>> factory PauseMenu_Config */
void PauseMenu_Config(void);
/* <<< factory PauseMenu_Config */
/* >>> factory PCMenu_ReadMail */
/* overworld.asm:1264. The farcall forwards the callee's a unchanged; b, c, d,
 * e and hl follow _PCMenu_ReadMail, which models none of them. */
uint8_t PCMenu_ReadMail(void);
/* <<< factory PCMenu_ReadMail */
/* >>> factory Func_c2a3 */
/* overworld.asm:363. Preserves bc, de and hl; clobbers a and f. */
void Func_c2a3(void);
/* <<< factory Func_c2a3 */
/* >>> factory PauseMenu_Card */
void PauseMenu_Card(void);
/* <<< factory PauseMenu_Card */
/* >>> factory EnterScript */
typedef struct {
	uint8_t a;
	uint16_t hl;
} EnterScriptResult;

EnterScriptResult EnterScript(void);
/* <<< factory EnterScript */
/* >>> factory SetScriptData */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} SetScriptDataResult;

SetScriptDataResult SetScriptData(uint16_t hl);
/* <<< factory SetScriptData */
/* >>> factory PauseMenu_Deck */
void PauseMenu_Deck(void);
/* <<< factory PauseMenu_Deck */
/* >>> factory PauseMenu */
void PauseMenu(void);
/* <<< factory PauseMenu */
/* >>> factory OpenPauseMenu */
void OpenPauseMenu(void);
/* <<< factory OpenPauseMenu */
/* >>> factory HandlePlayerMoveMode */
void HandlePlayerMoveMode(void);
/* <<< factory HandlePlayerMoveMode */
/* >>> factory CallHandlePlayerMoveMode */
void CallHandlePlayerMoveMode(void);
/* <<< factory CallHandlePlayerMoveMode */
/* >>> factory HandleOverworldMode */
void HandleOverworldMode(uint16_t hl);
/* <<< factory HandleOverworldMode */
/* >>> factory LoadMap */
void LoadMap(void);
/* <<< factory LoadMap */
/* >>> factory PCMenu_Print */
void PCMenu_Print(void);
/* <<< factory PCMenu_Print */
#endif /* POKETCG_HOME_OVERWORLD_H */
