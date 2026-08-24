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
#endif /* POKETCG_HOME_OVERWORLD_H */
