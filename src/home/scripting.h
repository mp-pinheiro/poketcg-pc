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
#endif
