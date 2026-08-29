#include "home/scripting.h"
#include "probe.h"

/* >>> factory IncreaseScriptPointer */
static void adapt_IncreaseScriptPointer(ProbeState *s)
{
	IncreaseScriptPointerResult result = IncreaseScriptPointer(s->a);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory IncreaseScriptPointer */


/* >>> factory SetScriptPointer */
static void adapt_SetScriptPointer(ProbeState *s)
{
	s->hl = SetScriptPointer((uint16_t)(s->b << 8 | s->c));
}
/* <<< factory SetScriptPointer */


/* >>> factory GetScriptArgsAfterPointer */
static void adapt_GetScriptArgsAfterPointer(ProbeState *s)
{
	GetScriptArgsAfterPointerResult result = GetScriptArgsAfterPointer(s->a);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory GetScriptArgsAfterPointer */


/* >>> factory GetEventVar */
static void adapt_GetEventVar(ProbeState *s)
{
	GetEventVarResult result = GetEventVar(s->a, s->f, s->b, s->c);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}
/* <<< factory GetEventVar */


/* >>> factory IncreaseScriptPointerBy1 */
static void adapt_IncreaseScriptPointerBy1(ProbeState *s)
{
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy1();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory IncreaseScriptPointerBy1 */

/* >>> factory IncreaseScriptPointerBy2 */
static void adapt_IncreaseScriptPointerBy2(ProbeState *s)
{
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy2();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory IncreaseScriptPointerBy2 */

/* >>> factory IncreaseScriptPointerBy4 */
static void adapt_IncreaseScriptPointerBy4(ProbeState *s)
{
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy4();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory IncreaseScriptPointerBy4 */

/* >>> factory IncreaseScriptPointerBy3 */
static void adapt_IncreaseScriptPointerBy3(ProbeState *s)
{
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy3();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory IncreaseScriptPointerBy3 */

/* >>> factory GetScriptArgs5AfterPointer */
static void adapt_GetScriptArgs5AfterPointer(ProbeState *s)
{
	GetScriptArgsAfterPointerResult r = GetScriptArgs5AfterPointer();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory GetScriptArgs5AfterPointer */

/* >>> factory SetScriptControlByteFail */
static void adapt_SetScriptControlByteFail(ProbeState *s)
{
	SetScriptControlByteFailResult r = SetScriptControlByteFail();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory SetScriptControlByteFail */

/* >>> factory IncreaseScriptPointerBy5 */
static void adapt_IncreaseScriptPointerBy5(ProbeState *s)
{
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory IncreaseScriptPointerBy5 */

/* >>> factory IncreaseScriptPointerBy6 */
static void adapt_IncreaseScriptPointerBy6(ProbeState *s)
{
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy6();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory IncreaseScriptPointerBy6 */

/* >>> factory IncreaseScriptPointerBy7 */
static void adapt_IncreaseScriptPointerBy7(ProbeState *s)
{
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy7();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory IncreaseScriptPointerBy7 */

/* >>> factory GetScriptArgs2AfterPointer */
static void adapt_GetScriptArgs2AfterPointer(ProbeState *s)
{
	GetScriptArgsAfterPointerResult r = GetScriptArgs2AfterPointer();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory GetScriptArgs2AfterPointer */

/* >>> factory GetScriptArgs3AfterPointer */
static void adapt_GetScriptArgs3AfterPointer(ProbeState *s)
{
	GetScriptArgsAfterPointerResult r = GetScriptArgs3AfterPointer();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory GetScriptArgs3AfterPointer */

/* >>> factory SetScriptControlBytePass */
static void adapt_SetScriptControlBytePass(ProbeState *s)
{
	s->a = SetScriptControlBytePass();
}
/* <<< factory SetScriptControlBytePass */

/* >>> factory ScriptCommand_JumpIfCardInCollection */
static void adapt_ScriptCommand_JumpIfCardInCollection(ProbeState *s)
{
	JumpIfCardInCollectionResult r = ScriptCommand_JumpIfCardInCollection(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory ScriptCommand_JumpIfCardInCollection */

/* >>> factory ScriptCommand_GiveCard */
static void adapt_ScriptCommand_GiveCard(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_GiveCard(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_GiveCard */

/* >>> factory ScriptCommand_TakeCard */
static void adapt_ScriptCommand_TakeCard(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_TakeCard(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_TakeCard */

/* >>> factory ScriptCommand_PauseSong */
static void adapt_ScriptCommand_PauseSong(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_PauseSong();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_PauseSong */

/* >>> factory ScriptCommand_ResumeSong */
static void adapt_ScriptCommand_ResumeSong(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_ResumeSong();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_ResumeSong */

/* >>> factory ScriptCommand_nop */
static void adapt_ScriptCommand_nop(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_nop();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_nop */

/* >>> factory ScriptCommand_OverrideSong */
static void adapt_ScriptCommand_OverrideSong(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_OverrideSong(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_OverrideSong */

/* >>> factory ScriptCommand_SetDefaultSong */
static void adapt_ScriptCommand_SetDefaultSong(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_SetDefaultSong(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_SetDefaultSong */

/* >>> factory ScriptCommand_RecordMasterWin */
static void adapt_ScriptCommand_RecordMasterWin(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_RecordMasterWin(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_RecordMasterWin */

/* >>> factory ScriptCommand_ChallengeMachine */
static void adapt_ScriptCommand_ChallengeMachine(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_ChallengeMachine();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_ChallengeMachine */

/* >>> factory ScriptCommand_PlaySong */
static void adapt_ScriptCommand_PlaySong(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_PlaySong(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_PlaySong */

/* >>> factory ScriptCommand_PlaySFX */
static void adapt_ScriptCommand_PlaySFX(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_PlaySFX(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_PlaySFX */

/* >>> factory ScriptCommand_PlayDefaultSong */
static void adapt_ScriptCommand_PlayDefaultSong(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_PlayDefaultSong();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_PlayDefaultSong */

/* >>> factory ScriptCommand_SetSpriteAttributes */
static void adapt_ScriptCommand_SetSpriteAttributes(ProbeState *s)
{
	SetSpriteAttributesResult r = ScriptCommand_SetSpriteAttributes(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
	s->e = r.e;
}
/* <<< factory ScriptCommand_SetSpriteAttributes */

/* >>> factory ScriptCommand_DoFrames */
static void adapt_ScriptCommand_DoFrames(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_DoFrames(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_DoFrames */

/* >>> factory ScriptCommand_EndScript */
static void adapt_ScriptCommand_EndScript(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_EndScript();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_EndScript */

/* >>> factory SetNPCDuelParams */
static void adapt_SetNPCDuelParams(ProbeState *s)
{
	SetNPCDuelParamsResult r = SetNPCDuelParams(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory SetNPCDuelParams */

/* >>> factory ScriptCommand_BattleCenter */
static void adapt_ScriptCommand_BattleCenter(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_BattleCenter();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_BattleCenter */

/* >>> factory ScriptCommand_LoadCurrentMapNameIntoTxRamSlot */
static void adapt_ScriptCommand_LoadCurrentMapNameIntoTxRamSlot(ProbeState *s)
{
	ScriptCommand_LoadCurrentMapNameIntoTxRamSlotResult r = ScriptCommand_LoadCurrentMapNameIntoTxRamSlot(s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory ScriptCommand_LoadCurrentMapNameIntoTxRamSlot */

/* >>> factory ScriptCommand_EnterMap */
static void adapt_ScriptCommand_EnterMap(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_EnterMap();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_EnterMap */

/* >>> factory GetScriptArgs1AfterPointer */
static void adapt_GetScriptArgs1AfterPointer(ProbeState *s)
{
	GetScriptArgsAfterPointerResult r = GetScriptArgs1AfterPointer();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory GetScriptArgs1AfterPointer */

/* >>> factory SetNextScript */
static void adapt_SetNextScript(ProbeState *s)
{
	SetNextScript((uint16_t)(((uint16_t)s->b << 8) | s->c));
}
/* <<< factory SetNextScript */

/* >>> factory SetEventValue */
static void adapt_SetEventValue(ProbeState *s)
{
	SetEventValueResult result = SetEventValue(s->a, s->f, s->b, s->c);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory SetEventValue */

/* >>> factory MaxOutEventValue */
static void adapt_MaxOutEventValue(ProbeState *s)
{
	SetEventValueResult r = MaxOutEventValue(s->a, s->f, s->b, s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory MaxOutEventValue */

/* >>> factory ZeroOutEventValue */
static void adapt_ZeroOutEventValue(ProbeState *s)
{
	SetEventValueResult r = ZeroOutEventValue(s->a, s->f, s->b, s->c);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ZeroOutEventValue */

/* >>> factory ClearEvents */
static void adapt_ClearEvents(ProbeState *s)
{
	ClearEvents();
	s->a = 0x00u;
	s->f = 0x80u;
}
/* <<< factory ClearEvents */

/* >>> factory ScriptCommand_Jump */
static void adapt_ScriptCommand_Jump(ProbeState *s)
{
	ScriptCommand_JumpResult r = ScriptCommand_Jump();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ScriptCommand_Jump */

/* >>> factory ScriptCommand_MaxOutEventValue */
static void adapt_ScriptCommand_MaxOutEventValue(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_MaxOutEventValue(s->f, s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_MaxOutEventValue */

/* >>> factory ScriptCommand_ZeroOutEventValue */
static void adapt_ScriptCommand_ZeroOutEventValue(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_ZeroOutEventValue(s->f, s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_ZeroOutEventValue */

/* >>> factory ScriptCommand_SetEventValue */
static void adapt_ScriptCommand_SetEventValue(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_SetEventValue(s->f, s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_SetEventValue */

/* >>> factory ScriptCommand_TryGivePCPack */
static void adapt_ScriptCommand_TryGivePCPack(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_TryGivePCPack(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_TryGivePCPack */

/* >>> factory ScriptCommand_SetActiveNPCCoords */
static void adapt_ScriptCommand_SetActiveNPCCoords(ProbeState *s)
{
	IncreaseScriptPointerResultWithB r = ScriptCommand_SetActiveNPCCoords(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory ScriptCommand_SetActiveNPCCoords */

/* >>> factory ScriptCommand_JumpIfEnoughCardsOwned */
static void adapt_ScriptCommand_JumpIfEnoughCardsOwned(ProbeState *s)
{
	JumpIfCardInCollectionResult r = ScriptCommand_JumpIfEnoughCardsOwned(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory ScriptCommand_JumpIfEnoughCardsOwned */

/* >>> factory ScriptCommand_RemoveAllEnergyCardsFromCollection */
static void adapt_ScriptCommand_RemoveAllEnergyCardsFromCollection(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_RemoveAllEnergyCardsFromCollection();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_RemoveAllEnergyCardsFromCollection */

/* >>> factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */
static void adapt_ScriptCommand_JumpIfAnyEnergyCardsInCollection(ProbeState *s)
{
	ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult r = ScriptCommand_JumpIfAnyEnergyCardsInCollection();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */

/* >>> factory ScriptCommand_JumpBasedOnFightingClubPupilStatus */
/* >>> factory ScriptCommand_JumpBasedOnFightingClubPupilStatus */
static void adapt_ScriptCommand_JumpBasedOnFightingClubPupilStatus(ProbeState *s)
{
	ScriptCommand_JumpBasedOnFightingClubPupilStatusResult r = ScriptCommand_JumpBasedOnFightingClubPupilStatus();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ScriptCommand_JumpBasedOnFightingClubPupilStatus */
/* <<< factory ScriptCommand_JumpBasedOnFightingClubPupilStatus */

/* >>> factory GetEventValue */
static void adapt_GetEventValue(ProbeState *s)
{
	uint8_t value = GetEventValue(s->a);
	s->a = value;
	s->f = value == 0u ? 0x80u : 0u;
}
/* <<< factory GetEventValue */

/* >>> factory GetEventValueBC */
static void adapt_GetEventValueBC(ProbeState *s)
{
	GetEventValueBCResult result = GetEventValueBC(s->b, s->c);
	s->a = result.a;
	s->f = result.f;
	s->b = result.c;
	s->c = result.c;
}
/* <<< factory GetEventValueBC */

/* >>> factory ScriptCommand_JumpIfEventEqual */
static void adapt_ScriptCommand_JumpIfEventEqual(ProbeState *s)
{
	ScriptCommand_JumpIfEventEqualResult r = ScriptCommand_JumpIfEventEqual(s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ScriptCommand_JumpIfEventEqual */

/* >>> factory ScriptCommand_JumpIfEventZero */
static void adapt_ScriptCommand_JumpIfEventZero(ProbeState *s)
{
	ScriptCommand_JumpIfEventZeroResult r = ScriptCommand_JumpIfEventZero(s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ScriptCommand_JumpIfEventZero */

/* >>> factory ScriptCommand_JumpIfEventGreaterOrEqual */
static void adapt_ScriptCommand_JumpIfEventGreaterOrEqual(ProbeState *s)
{
	ScriptCommand_JumpIfEventGreaterOrEqualResult r = ScriptCommand_JumpIfEventGreaterOrEqual(s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ScriptCommand_JumpIfEventGreaterOrEqual */

/* >>> factory ScriptCommand_JumpIfEventLessThan */
static void adapt_ScriptCommand_JumpIfEventLessThan(ProbeState *s)
{
	ScriptCommand_JumpIfEventLessThanResult r = ScriptCommand_JumpIfEventLessThan(s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ScriptCommand_JumpIfEventLessThan */

/* >>> factory ScriptCommand_JumpIfEventNotEqual */
static void adapt_ScriptCommand_JumpIfEventNotEqual(ProbeState *s)
{
	ScriptCommand_JumpIfEventNotEqualResult r = ScriptCommand_JumpIfEventNotEqual(s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ScriptCommand_JumpIfEventNotEqual */

/* >>> factory ScriptCommand_JumpIfEventNonzero */
static void adapt_ScriptCommand_JumpIfEventNonzero(ProbeState *s)
{
	ScriptCommand_JumpIfEventZeroResult r = ScriptCommand_JumpIfEventNonzero(s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ScriptCommand_JumpIfEventNonzero */

/* >>> factory ScriptCommand_JumpIfEventTrue */
static void adapt_ScriptCommand_JumpIfEventTrue(ProbeState *s)
{
	ScriptCommand_JumpIfEventTrueResult r = ScriptCommand_JumpIfEventTrue(s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ScriptCommand_JumpIfEventTrue */

/* >>> factory ScriptCommand_JumpIfEventFalse */
static void adapt_ScriptCommand_JumpIfEventFalse(ProbeState *s)
{
	ScriptCommand_JumpIfEventTrueResult r = ScriptCommand_JumpIfEventFalse(s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ScriptCommand_JumpIfEventFalse */

/* >>> factory ScriptCommand_WalkPlayerToMasonLaboratory */
static void adapt_ScriptCommand_WalkPlayerToMasonLaboratory(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_WalkPlayerToMasonLaboratory();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_WalkPlayerToMasonLaboratory */



/* >>> factory ScriptCommand_IncrementEventValue */
static void adapt_ScriptCommand_IncrementEventValue(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_IncrementEventValue(s->f, s->b, s->c);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_IncrementEventValue */

/* >>> factory ScriptCommand_JumpIfPlayerCoordsMatch */
static void adapt_ScriptCommand_JumpIfPlayerCoordsMatch(ProbeState *s)
{
	ScriptCommand_JumpIfPlayerCoordsMatchResult result = ScriptCommand_JumpIfPlayerCoordsMatch(s->b, s->c, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}
/* <<< factory ScriptCommand_JumpIfPlayerCoordsMatch */

/* >>> factory ScriptCommand_JumpIfActiveNPCCoordsMatch */
static void adapt_ScriptCommand_JumpIfActiveNPCCoordsMatch(ProbeState *s)
{
	ScriptCommand_JumpIfActiveNPCCoordsMatchResult result = ScriptCommand_JumpIfActiveNPCCoordsMatch(s->b, s->c, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory ScriptCommand_JumpIfActiveNPCCoordsMatch */

/* >>> factory SetNextNPCAndScript */
static void adapt_SetNextNPCAndScript(ProbeState *s)
{
	SetNextNPCAndScriptResult result = SetNextNPCAndScript((uint16_t)(((uint16_t)s->b << 8) | s->c), s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}
/* <<< factory SetNextNPCAndScript */

/* >>> factory ExecuteNPCMovement */
static void adapt_ExecuteNPCMovement(ProbeState *s)
{
	ExecuteNPCMovementResult result = ExecuteNPCMovement((uint16_t)(s->b << 8 | s->c));
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory ExecuteNPCMovement */

/* >>> factory Func_cdd1 */
static void adapt_Func_cdd1(ProbeState *s)
{
	IncreaseScriptPointerResult result = Func_cdd1();
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory Func_cdd1 */

/* >>> factory ScriptCommand_JumpIfCardOwned */
static void adapt_ScriptCommand_JumpIfCardOwned(ProbeState *s)
{
	JumpIfCardInCollectionResult r = ScriptCommand_JumpIfCardOwned(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory ScriptCommand_JumpIfCardOwned */

/* >>> factory ScriptCommand_WaitForSongToFinish */
static void adapt_ScriptCommand_WaitForSongToFinish(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_WaitForSongToFinish();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_WaitForSongToFinish */

/* >>> factory ScriptCommand_SaveGame */
static void adapt_ScriptCommand_SaveGame(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_SaveGame(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_SaveGame */

/* >>> factory ScriptCommand_MoveActiveNPC */
static void adapt_ScriptCommand_MoveActiveNPC(ProbeState *s)
{
	ExecuteNPCMovementResult result = ScriptCommand_MoveActiveNPC((uint16_t)(((uint16_t)s->b << 8) | s->c));
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory ScriptCommand_MoveActiveNPC */

/* >>> factory ScriptCommand_SetNextNPCAndScript */
static void adapt_ScriptCommand_SetNextNPCAndScript(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_SetNextNPCAndScript(s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_SetNextNPCAndScript */

/* >>> factory ScriptCommand_SetActiveNPCDirection */
static void adapt_ScriptCommand_SetActiveNPCDirection(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_SetActiveNPCDirection(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_SetActiveNPCDirection */

/* >>> factory ScriptCommand_PlayCredits */
static void adapt_ScriptCommand_PlayCredits(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_PlayCredits();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_PlayCredits */

/* >>> factory ScriptCommand_PickChallengeHallOpponent */
static void adapt_ScriptCommand_PickChallengeHallOpponent(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_PickChallengeHallOpponent();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_PickChallengeHallOpponent */

/* >>> factory ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot */
static void adapt_ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot */

/* >>> factory Func_c998 */
static void adapt_Func_c998(ProbeState *s)
{
	Func_c998Result r = Func_c998();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Func_c998 */

/* >>> factory DetermineImakuniRoom */
static void adapt_DetermineImakuniRoom(ProbeState *s)
{
	SetEventValueResult r = DetermineImakuniRoom();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory DetermineImakuniRoom */

/* >>> factory ScriptCommand_SetPlayerDirection */
static void adapt_ScriptCommand_SetPlayerDirection(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_SetPlayerDirection(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_SetPlayerDirection */

/* >>> factory ScriptCommand_UnloadActiveNPC */
static void adapt_ScriptCommand_UnloadActiveNPC(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_UnloadActiveNPC();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_UnloadActiveNPC */

/* >>> factory ScriptCommand_ReplaceMapBlocks */
static void adapt_ScriptCommand_ReplaceMapBlocks(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_ReplaceMapBlocks(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_ReplaceMapBlocks */

/* >>> factory ScriptCommand_GiveStarterDeck */
static void adapt_ScriptCommand_GiveStarterDeck(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_GiveStarterDeck();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_GiveStarterDeck */

/* >>> factory ScriptCommand_FlashScreen */
static void adapt_ScriptCommand_FlashScreen(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_FlashScreen(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_FlashScreen */

/* >>> factory ScriptCommand_MoveActiveNPCByDirection */
static void adapt_ScriptCommand_MoveActiveNPCByDirection(ProbeState *s)
{
	ExecuteNPCMovementResult r = ScriptCommand_MoveActiveNPCByDirection(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory ScriptCommand_MoveActiveNPCByDirection */

/* >>> factory ScriptCommand_UnloadChallengeHallNPC */
static void adapt_ScriptCommand_UnloadChallengeHallNPC(ProbeState *s)
{
	(void)s;
	ScriptCommand_UnloadChallengeHallNPC();
}
/* <<< factory ScriptCommand_UnloadChallengeHallNPC */

/* >>> factory DetermineChallengeHallEvent */
static void adapt_DetermineChallengeHallEvent(ProbeState *s)
{
	(void)s;
	DetermineChallengeHallEvent();
}
/* <<< factory DetermineChallengeHallEvent */

/* >>> factory DetermineImakuniAndChallengeHall */
static void adapt_DetermineImakuniAndChallengeHall(ProbeState *s)
{
	(void)s;
	DetermineImakuniAndChallengeHall();
}
/* <<< factory DetermineImakuniAndChallengeHall */

/* >>> factory ScriptCommand_SetChallengeHallNPCCoords */
static void adapt_ScriptCommand_SetChallengeHallNPCCoords(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_SetChallengeHallNPCCoords(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_SetChallengeHallNPCCoords */

/* >>> factory LoadOverworld */
static void adapt_LoadOverworld(ProbeState *s)
{
	(void)s;
	LoadOverworld();
}
/* <<< factory LoadOverworld */

/* >>> factory TryGiveMedalPCPacks */
static void adapt_TryGiveMedalPCPacks(ProbeState *s)
{
	TryGiveMedalPCPacksResult r = TryGiveMedalPCPacks(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory TryGiveMedalPCPacks */

/* >>> factory GetByteAfterCall */
static void adapt_GetByteAfterCall(ProbeState *s)
{
	s->a = GetByteAfterCall(s->hl);
}
/* <<< factory GetByteAfterCall */

/* >>> factory ScriptCommand_TryGiveMedalPCPacks */
static void adapt_ScriptCommand_TryGiveMedalPCPacks(ProbeState *s)
{
	ScriptCommand_TryGiveMedalPCPacksResult r = ScriptCommand_TryGiveMedalPCPacks(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory ScriptCommand_TryGiveMedalPCPacks */

/* >>> factory ScriptCommand_SetDialogNPC */
static void adapt_ScriptCommand_SetDialogNPC(ProbeState *s)
{
	ScriptCommand_SetDialogNPCResult r = ScriptCommand_SetDialogNPC(s->f, s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ScriptCommand_SetDialogNPC */

/* >>> factory ScriptCommand_LoadChallengeHallNPCIntoTxRamSlot */
static void adapt_ScriptCommand_LoadChallengeHallNPCIntoTxRamSlot(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_LoadChallengeHallNPCIntoTxRamSlot(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_LoadChallengeHallNPCIntoTxRamSlot */

/* >>> factory ScriptCommand_StartDuel */
static void adapt_ScriptCommand_StartDuel(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_StartDuel(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_StartDuel */

/* >>> factory ScriptCommand_StartChallengeHallDuel */
static void adapt_ScriptCommand_StartChallengeHallDuel(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_StartChallengeHallDuel(s->b, s->c);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_StartChallengeHallDuel */

/* >>> factory ScriptCommand_AskQuestionJump */
static void adapt_ScriptCommand_AskQuestionJump(ProbeState *s)
{
	ScriptCommand_AskQuestionJumpResult r = ScriptCommand_AskQuestionJump(s->b, s->c);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->hl = r.hl;
}
/* <<< factory ScriptCommand_AskQuestionJump */

/* >>> factory ScriptCommand_AskQuestionJumpDefaultYes */
static void adapt_ScriptCommand_AskQuestionJumpDefaultYes(ProbeState *s)
{
	ScriptCommand_AskQuestionJumpResult r = ScriptCommand_AskQuestionJumpDefaultYes(s->b, s->c);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->hl = r.hl;
}
/* <<< factory ScriptCommand_AskQuestionJumpDefaultYes */

/* >>> factory ScriptCommand_JumpIfNPCLoaded */
static void adapt_ScriptCommand_JumpIfNPCLoaded(ProbeState *s)
{
	ScriptCommand_JumpIfNPCLoadedResult result = ScriptCommand_JumpIfNPCLoaded(s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory ScriptCommand_JumpIfNPCLoaded */


/* >>> factory CallMapScriptPointerIfExists */
static void adapt_CallMapScriptPointerIfExists(ProbeState *s)
{
	CallMapScriptResult r = CallMapScriptPointerIfExists((uint8_t)s->hl);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory CallMapScriptPointerIfExists */


/* >>> factory Func_c9bc */
static void adapt_Func_c9bc(ProbeState *s)
{
	CallMapScriptResult r = Func_c9bc();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Func_c9bc */

/* >>> factory Func_c9c7 */
static void adapt_Func_c9c7(ProbeState *s)
{
	CallMapScriptResult r = Func_c9c7();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Func_c9c7 */

/* >>> factory Func_c9b8 */
static void adapt_Func_c9b8(ProbeState *s)
{
	CallMapScriptResult r = Func_c9b8();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Func_c9b8 */

/* >>> factory ScriptCommand_CloseTextBox */
static void adapt_ScriptCommand_CloseTextBox(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_CloseTextBox();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_CloseTextBox */

/* >>> factory ScriptCommand_PrintText */
static void adapt_ScriptCommand_PrintText(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_PrintText(s->b, s->c);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_PrintText */

/* >>> factory Func_c9c0 */
static void adapt_Func_c9c0(ProbeState *s)
{
	CallMapScriptResult r = Func_c9c0();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Func_c9c0 */

/* >>> factory Func_cc32 */
static void adapt_Func_cc32(ProbeState *s)
{
	Func_cc32(s->hl);
}
/* <<< factory Func_cc32 */

/* >>> factory Script_LegendaryCardRightSpark */
static void adapt_Script_LegendaryCardRightSpark(ProbeState *s)
{
	Script_LegendaryCardRightSpark();
}
/* <<< factory Script_LegendaryCardRightSpark */

/* >>> factory ScriptCommand_PrintNPCText */
static void adapt_ScriptCommand_PrintNPCText(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_PrintNPCText(s->b, s->c);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_PrintNPCText */

/* >>> factory ScriptCommand_CloseAdvancedTextBox */
static void adapt_ScriptCommand_CloseAdvancedTextBox(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_CloseAdvancedTextBox();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_CloseAdvancedTextBox */

/* >>> factory ScriptCommand_PrintVariableNPCText */
static void adapt_ScriptCommand_PrintVariableNPCText(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_PrintVariableNPCText(s->b, s->c);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_PrintVariableNPCText */

/* >>> factory ScriptCommand_PrintVariableText */
static void adapt_ScriptCommand_PrintVariableText(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_PrintVariableText(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_PrintVariableText */

/* >>> factory ScriptCommand_GiftCenter */
static void adapt_ScriptCommand_GiftCenter(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_GiftCenter(s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_GiftCenter */

/* >>> factory ScriptCommand_PrintTextQuitFully */
/* >>> factory ScriptCommand_PrintTextQuitFully */
static void adapt_ScriptCommand_PrintTextQuitFully(ProbeState *s)
{
	ScriptCommand_PrintTextQuitFullyResult result = ScriptCommand_PrintTextQuitFully(s->a, s->f, s->b, s->c, s->d, s->e, s->stack[0]);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory ScriptCommand_PrintTextQuitFully */

/* >>> factory ScriptCommand_QuitScriptFully */
static void adapt_ScriptCommand_QuitScriptFully(ProbeState *s)
{
	ScriptCommand_QuitScriptFullyResult result = ScriptCommand_QuitScriptFully(s->stack[0]);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
	s->hl = result.hl;
}
/* <<< factory ScriptCommand_QuitScriptFully */

/* >>> factory PrintInteractableObjectText */
static void adapt_PrintInteractableObjectText(ProbeState *s)
{
	PrintInteractableObjectText();
}
/* <<< factory PrintInteractableObjectText */

/* >>> factory Func_c943 */
static void adapt_Func_c943(ProbeState *s)
{
	Func_c943Result result = Func_c943(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory Func_c943 */

/* >>> factory ScriptCommand_MovePlayer */
static void adapt_ScriptCommand_MovePlayer(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_MovePlayer(s->b, s->c);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_MovePlayer */

/* >>> factory ShowMultichoiceTextbox */
static void adapt_ShowMultichoiceTextbox(ProbeState *s)
{
	ShowMultichoiceTextboxResult result = ShowMultichoiceTextbox(s->a, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory ShowMultichoiceTextbox */

/* >>> factory ScriptCommand_ChooseStarterDeckMultichoice */
static void adapt_ScriptCommand_ChooseStarterDeckMultichoice(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_ChooseStarterDeckMultichoice();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_ChooseStarterDeckMultichoice */

/* >>> factory ScriptCommand_ShowSamNormalMultichoice */
static void adapt_ScriptCommand_ShowSamNormalMultichoice(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_ShowSamNormalMultichoice();
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_ShowSamNormalMultichoice */

/* >>> factory ScriptCommand_ShowSamRulesMultichoice */
static void adapt_ScriptCommand_ShowSamRulesMultichoice(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_ShowSamRulesMultichoice();
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_ShowSamRulesMultichoice */

/* >>> factory ScriptCommand_ChooseDeckToDuelAgainstMultichoice */
static void adapt_ScriptCommand_ChooseDeckToDuelAgainstMultichoice(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_ChooseDeckToDuelAgainstMultichoice();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_ChooseDeckToDuelAgainstMultichoice */

/* >>> factory ScriptCommand_GiveOneOfEachTrainerBooster */
static void adapt_ScriptCommand_GiveOneOfEachTrainerBooster(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_GiveOneOfEachTrainerBooster();
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_GiveOneOfEachTrainerBooster */

/* >>> factory ScriptCommand_ShowCardReceivedScreen */
static void adapt_ScriptCommand_ShowCardReceivedScreen(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_ShowCardReceivedScreen(s->c);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_ShowCardReceivedScreen */

/* >>> factory ScriptCommand_ShowMedalReceivedScreen */
static void adapt_ScriptCommand_ShowMedalReceivedScreen(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_ShowMedalReceivedScreen(s->c);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_ShowMedalReceivedScreen */

/* >>> factory ScriptCommand_GiveBoosterPacks */
static void adapt_ScriptCommand_GiveBoosterPacks(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_GiveBoosterPacks(s->b, s->c);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_GiveBoosterPacks */

/* >>> factory Script_GiftCenterClerk */
static void adapt_Script_GiftCenterClerk(ProbeState *s)
{
	(void)s;
	Script_GiftCenterClerk();
}
/* <<< factory Script_GiftCenterClerk */

/* >>> factory Script_Clerk10 */
static void adapt_Script_Clerk10(ProbeState *s)
{
	Script_Clerk10();
	(void)s;
}
/* <<< factory Script_Clerk10 */

/* >>> factory Script_LegendaryCardBottomLeft */
static void adapt_Script_LegendaryCardBottomLeft(ProbeState *s)
{
	(void)s;
	Script_LegendaryCardBottomLeft();
}
/* <<< factory Script_LegendaryCardBottomLeft */

/* >>> factory Script_LegendaryCardTopRight */
static void adapt_Script_LegendaryCardTopRight(ProbeState *s)
{
	ScriptLegendaryCardTopRightResult result = Script_LegendaryCardTopRight();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Script_LegendaryCardTopRight */

/* >>> factory Script_LegendaryCardTopLeft */
static void adapt_Script_LegendaryCardTopLeft(ProbeState *s)
{
	(void)s;
	Script_LegendaryCardTopLeft();
}
/* <<< factory Script_LegendaryCardTopLeft */

/* >>> factory Script_LegendaryCardBottomRight */
static void adapt_Script_LegendaryCardBottomRight(ProbeState *s)
{
	(void)s;
	Script_LegendaryCardBottomRight();
}
/* <<< factory Script_LegendaryCardBottomRight */

/* >>> factory Script_LegendaryCardLeftSpark */
static void adapt_Script_LegendaryCardLeftSpark(ProbeState *s)
{
	(void)s;
	Script_LegendaryCardLeftSpark();
}
/* <<< factory Script_LegendaryCardLeftSpark */

/* >>> factory Script_Torch */
static void adapt_Script_Torch(ProbeState *s)
{
	(void)s;
	Script_Torch();
}
/* <<< factory Script_Torch */

/* >>> factory Script_Woman2 */
static void adapt_Script_Woman2(ProbeState *s)
{
	Script_Woman2();
	(void)s;
}
/* <<< factory Script_Woman2 */

/* >>> factory ScriptCommand_OpenDeckMachine */
static void adapt_ScriptCommand_OpenDeckMachine(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_OpenDeckMachine(s->c);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_OpenDeckMachine */

/* >>> factory ExecuteArbitraryNPCMovementFromStack */
static void adapt_ExecuteArbitraryNPCMovementFromStack(ProbeState *s)
{
	uint16_t bc = (uint16_t)(((uint16_t)s->b << 8) | s->c);
	ExecuteArbitraryNPCMovementFromStackResult result =
		ExecuteArbitraryNPCMovementFromStack(s->a, bc, s->stack[0], s->stack[1]);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory ExecuteArbitraryNPCMovementFromStack */

/* >>> factory ScriptCommand_MoveChallengeHallNPC */
static void adapt_ScriptCommand_MoveChallengeHallNPC(ProbeState *s)
{
	uint16_t bc = (uint16_t)(((uint16_t)s->b << 8) | s->c);
	ExecuteArbitraryNPCMovementFromStackResult result = ScriptCommand_MoveChallengeHallNPC(s->f, bc);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory ScriptCommand_MoveChallengeHallNPC */

/* >>> factory ScriptCommand_MoveArbitraryNPC */
static void adapt_ScriptCommand_MoveArbitraryNPC(ProbeState *s)
{
	ExecuteArbitraryNPCMovementFromStackResult result =
		ScriptCommand_MoveArbitraryNPC(s->f, s->c);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory ScriptCommand_MoveArbitraryNPC */

/* >>> factory MaxStackEventValue */
static void adapt_MaxStackEventValue(ProbeState *s)
{
	SetEventValueResult result = MaxStackEventValue(s->post_call_byte, s->f, s->b, s->c);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory MaxStackEventValue */

/* >>> factory SetStackEventFalse */
static void adapt_SetStackEventFalse(ProbeState *s)
{
	SetEventValueResult result = SetStackEventFalse(s->f, s->b, s->c, s->post_call_byte);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory SetStackEventFalse */

/* >>> factory SetStackEventValue */
static void adapt_SetStackEventValue(ProbeState *s)
{
	SetEventValueResult result = SetStackEventValue(s->f, s->b, s->c, s->post_call_byte);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory SetStackEventValue */

/* >>> factory SetStackEventZero */
static void adapt_SetStackEventZero(ProbeState *s)
{
	SetEventValueResult result = SetStackEventZero(s->post_call_byte, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory SetStackEventZero */

/* >>> factory GetStackEventValue */
static void adapt_GetStackEventValue(ProbeState *s)
{
	uint8_t value = GetStackEventValue(s->post_call_byte);
	s->a = value;
	s->f = value == 0u ? 0x80u : 0u;
}
/* <<< factory GetStackEventValue */

const ProbeEntry probe_entries_scripting[] = {
	{ "Func_c9bc", adapt_Func_c9bc },
	{ "CallMapScriptPointerIfExists", adapt_CallMapScriptPointerIfExists },
	{ "IncreaseScriptPointer", adapt_IncreaseScriptPointer },
	{ "SetScriptPointer", adapt_SetScriptPointer },
	{ "GetScriptArgsAfterPointer", adapt_GetScriptArgsAfterPointer },
	{ "GetEventVar", adapt_GetEventVar },
	{ "IncreaseScriptPointerBy1", adapt_IncreaseScriptPointerBy1 },
	{ "IncreaseScriptPointerBy2", adapt_IncreaseScriptPointerBy2 },
	{ "IncreaseScriptPointerBy4", adapt_IncreaseScriptPointerBy4 },
	{ "IncreaseScriptPointerBy3", adapt_IncreaseScriptPointerBy3 },
	{ "GetScriptArgs5AfterPointer", adapt_GetScriptArgs5AfterPointer },
	{ "SetScriptControlByteFail", adapt_SetScriptControlByteFail },
	{ "IncreaseScriptPointerBy5", adapt_IncreaseScriptPointerBy5 },
	{ "IncreaseScriptPointerBy6", adapt_IncreaseScriptPointerBy6 },
	{ "IncreaseScriptPointerBy7", adapt_IncreaseScriptPointerBy7 },
	{ "GetScriptArgs2AfterPointer", adapt_GetScriptArgs2AfterPointer },
	{ "GetScriptArgs3AfterPointer", adapt_GetScriptArgs3AfterPointer },
	{ "SetScriptControlBytePass", adapt_SetScriptControlBytePass },
	{ "ScriptCommand_JumpIfCardInCollection", adapt_ScriptCommand_JumpIfCardInCollection },
	{ "ScriptCommand_GiveCard", adapt_ScriptCommand_GiveCard },
	{ "ScriptCommand_TakeCard", adapt_ScriptCommand_TakeCard },
	{ "ScriptCommand_PauseSong", adapt_ScriptCommand_PauseSong },
	{ "ScriptCommand_ResumeSong", adapt_ScriptCommand_ResumeSong },
	{ "ScriptCommand_nop", adapt_ScriptCommand_nop },
	{ "ScriptCommand_OverrideSong", adapt_ScriptCommand_OverrideSong },
	{ "ScriptCommand_SetDefaultSong", adapt_ScriptCommand_SetDefaultSong },
	{ "ScriptCommand_RecordMasterWin", adapt_ScriptCommand_RecordMasterWin },
	{ "ScriptCommand_ChallengeMachine", adapt_ScriptCommand_ChallengeMachine },
	{ "ScriptCommand_PlaySong", adapt_ScriptCommand_PlaySong },
	{ "ScriptCommand_PlaySFX", adapt_ScriptCommand_PlaySFX },
	{ "ScriptCommand_PlayDefaultSong", adapt_ScriptCommand_PlayDefaultSong },
	{ "ScriptCommand_SetSpriteAttributes", adapt_ScriptCommand_SetSpriteAttributes },
	{ "ScriptCommand_DoFrames", adapt_ScriptCommand_DoFrames },
	{ "ScriptCommand_EndScript", adapt_ScriptCommand_EndScript },
	{ "SetNPCDuelParams", adapt_SetNPCDuelParams },
	{ "ScriptCommand_BattleCenter", adapt_ScriptCommand_BattleCenter },
	{ "ScriptCommand_LoadCurrentMapNameIntoTxRamSlot", adapt_ScriptCommand_LoadCurrentMapNameIntoTxRamSlot },
	{ "ScriptCommand_EnterMap", adapt_ScriptCommand_EnterMap },
	{ "GetScriptArgs1AfterPointer", adapt_GetScriptArgs1AfterPointer },
	{ "SetNextScript", adapt_SetNextScript },
	{ "SetEventValue", adapt_SetEventValue },
	{ "MaxOutEventValue", adapt_MaxOutEventValue },
	{ "ZeroOutEventValue", adapt_ZeroOutEventValue },
	{ "ClearEvents", adapt_ClearEvents },
	{ "ScriptCommand_Jump", adapt_ScriptCommand_Jump },
	{ "ScriptCommand_MaxOutEventValue", adapt_ScriptCommand_MaxOutEventValue },
	{ "ScriptCommand_ZeroOutEventValue", adapt_ScriptCommand_ZeroOutEventValue },
	{ "ScriptCommand_SetEventValue", adapt_ScriptCommand_SetEventValue },
	{ "ScriptCommand_TryGivePCPack", adapt_ScriptCommand_TryGivePCPack },
	{ "ScriptCommand_SetActiveNPCCoords", adapt_ScriptCommand_SetActiveNPCCoords },
	{ "ScriptCommand_JumpIfEnoughCardsOwned", adapt_ScriptCommand_JumpIfEnoughCardsOwned },
	{ "ScriptCommand_RemoveAllEnergyCardsFromCollection", adapt_ScriptCommand_RemoveAllEnergyCardsFromCollection },
	{ "ScriptCommand_JumpIfAnyEnergyCardsInCollection", adapt_ScriptCommand_JumpIfAnyEnergyCardsInCollection },
	{ "ScriptCommand_JumpBasedOnFightingClubPupilStatus", adapt_ScriptCommand_JumpBasedOnFightingClubPupilStatus },
	{ "GetEventValue", adapt_GetEventValue },
	{ "GetEventValueBC", adapt_GetEventValueBC },
	{ "ScriptCommand_JumpIfEventEqual", adapt_ScriptCommand_JumpIfEventEqual },
	{ "ScriptCommand_JumpIfEventZero", adapt_ScriptCommand_JumpIfEventZero },
	{ "ScriptCommand_JumpIfEventGreaterOrEqual", adapt_ScriptCommand_JumpIfEventGreaterOrEqual },
	{ "ScriptCommand_JumpIfEventLessThan", adapt_ScriptCommand_JumpIfEventLessThan },
	{ "ScriptCommand_JumpIfEventNotEqual", adapt_ScriptCommand_JumpIfEventNotEqual },
	{ "ScriptCommand_JumpIfEventNonzero", adapt_ScriptCommand_JumpIfEventNonzero },
	{ "ScriptCommand_JumpIfEventTrue", adapt_ScriptCommand_JumpIfEventTrue },
	{ "ScriptCommand_JumpIfEventFalse", adapt_ScriptCommand_JumpIfEventFalse },
	{ "ScriptCommand_WalkPlayerToMasonLaboratory", adapt_ScriptCommand_WalkPlayerToMasonLaboratory },
	{ "ScriptCommand_IncrementEventValue", adapt_ScriptCommand_IncrementEventValue },
	{ "ScriptCommand_JumpIfPlayerCoordsMatch", adapt_ScriptCommand_JumpIfPlayerCoordsMatch },
	{ "ScriptCommand_JumpIfActiveNPCCoordsMatch", adapt_ScriptCommand_JumpIfActiveNPCCoordsMatch },
	{ "SetNextNPCAndScript", adapt_SetNextNPCAndScript },
	{ "ExecuteNPCMovement", adapt_ExecuteNPCMovement },
	{ "Func_cdd1", adapt_Func_cdd1 },
	{ "ScriptCommand_JumpIfCardOwned", adapt_ScriptCommand_JumpIfCardOwned },
	{ "ScriptCommand_WaitForSongToFinish", adapt_ScriptCommand_WaitForSongToFinish },
	{ "ScriptCommand_SaveGame", adapt_ScriptCommand_SaveGame },
	{ "ScriptCommand_MoveActiveNPC", adapt_ScriptCommand_MoveActiveNPC },
	{ "ScriptCommand_SetNextNPCAndScript", adapt_ScriptCommand_SetNextNPCAndScript },
	{ "ScriptCommand_SetActiveNPCDirection", adapt_ScriptCommand_SetActiveNPCDirection },
	{ "ScriptCommand_PlayCredits", adapt_ScriptCommand_PlayCredits },
	{ "ScriptCommand_PickChallengeHallOpponent", adapt_ScriptCommand_PickChallengeHallOpponent },
	{ "ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot", adapt_ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot },
	{ "Func_c998", adapt_Func_c998 },
	{ "DetermineImakuniRoom", adapt_DetermineImakuniRoom },
	{ "ScriptCommand_SetPlayerDirection", adapt_ScriptCommand_SetPlayerDirection },
	{ "ScriptCommand_UnloadActiveNPC", adapt_ScriptCommand_UnloadActiveNPC },
	{ "ScriptCommand_ReplaceMapBlocks", adapt_ScriptCommand_ReplaceMapBlocks },
	{ "ScriptCommand_GiveStarterDeck", adapt_ScriptCommand_GiveStarterDeck },
	{ "ScriptCommand_FlashScreen", adapt_ScriptCommand_FlashScreen },
	{ "ScriptCommand_MoveActiveNPCByDirection", adapt_ScriptCommand_MoveActiveNPCByDirection },
	{ "ScriptCommand_UnloadChallengeHallNPC", adapt_ScriptCommand_UnloadChallengeHallNPC },
	{ "DetermineChallengeHallEvent", adapt_DetermineChallengeHallEvent },
	{ "DetermineImakuniAndChallengeHall", adapt_DetermineImakuniAndChallengeHall },
	{ "ScriptCommand_SetChallengeHallNPCCoords", adapt_ScriptCommand_SetChallengeHallNPCCoords },
	{ "LoadOverworld", adapt_LoadOverworld },
	{ "TryGiveMedalPCPacks", adapt_TryGiveMedalPCPacks },
	{ "GetByteAfterCall", adapt_GetByteAfterCall },
	{ "ScriptCommand_TryGiveMedalPCPacks", adapt_ScriptCommand_TryGiveMedalPCPacks },
	{ "ScriptCommand_SetDialogNPC", adapt_ScriptCommand_SetDialogNPC },
	{ "ScriptCommand_LoadChallengeHallNPCIntoTxRamSlot", adapt_ScriptCommand_LoadChallengeHallNPCIntoTxRamSlot },
	{ "ScriptCommand_StartDuel", adapt_ScriptCommand_StartDuel },
	{ "ScriptCommand_StartChallengeHallDuel", adapt_ScriptCommand_StartChallengeHallDuel },
	{ "ScriptCommand_AskQuestionJump", adapt_ScriptCommand_AskQuestionJump },
	{ "ScriptCommand_AskQuestionJumpDefaultYes", adapt_ScriptCommand_AskQuestionJumpDefaultYes },
	{ "ScriptCommand_JumpIfNPCLoaded", adapt_ScriptCommand_JumpIfNPCLoaded },
	{ "Func_c9c7", adapt_Func_c9c7 },
	{ "Func_c9b8", adapt_Func_c9b8 },
	{ "ScriptCommand_CloseTextBox", adapt_ScriptCommand_CloseTextBox },
	{ "ScriptCommand_PrintText", adapt_ScriptCommand_PrintText },
	{ "Func_c9c0", adapt_Func_c9c0 },
	{ "Script_LegendaryCardRightSpark", adapt_Script_LegendaryCardRightSpark },
	{ "ScriptCommand_PrintNPCText", adapt_ScriptCommand_PrintNPCText },
	{ "Func_cc32", adapt_Func_cc32 },
	{ "ScriptCommand_CloseAdvancedTextBox", adapt_ScriptCommand_CloseAdvancedTextBox },
	{ "ScriptCommand_PrintVariableNPCText", adapt_ScriptCommand_PrintVariableNPCText },
	{ "ScriptCommand_PrintVariableText", adapt_ScriptCommand_PrintVariableText },
	{ "ScriptCommand_GiftCenter", adapt_ScriptCommand_GiftCenter },
	{ "ScriptCommand_PrintTextQuitFully", adapt_ScriptCommand_PrintTextQuitFully },
	{ "ScriptCommand_QuitScriptFully", adapt_ScriptCommand_QuitScriptFully },
	{ "PrintInteractableObjectText", adapt_PrintInteractableObjectText },
	{ "Func_c943", adapt_Func_c943 },
	{ "ScriptCommand_MovePlayer", adapt_ScriptCommand_MovePlayer },
	{ "ScriptCommand_ChooseStarterDeckMultichoice", adapt_ScriptCommand_ChooseStarterDeckMultichoice },
	{ "ScriptCommand_ShowSamNormalMultichoice", adapt_ScriptCommand_ShowSamNormalMultichoice },
	{ "ScriptCommand_ShowSamRulesMultichoice", adapt_ScriptCommand_ShowSamRulesMultichoice },
	{ "ScriptCommand_ChooseDeckToDuelAgainstMultichoice", adapt_ScriptCommand_ChooseDeckToDuelAgainstMultichoice },
	{ "ShowMultichoiceTextbox", adapt_ShowMultichoiceTextbox },
	{ "ScriptCommand_GiveOneOfEachTrainerBooster", adapt_ScriptCommand_GiveOneOfEachTrainerBooster },
	{ "ScriptCommand_ShowCardReceivedScreen", adapt_ScriptCommand_ShowCardReceivedScreen },
	{ "ScriptCommand_ShowMedalReceivedScreen", adapt_ScriptCommand_ShowMedalReceivedScreen },
	{ "ScriptCommand_GiveBoosterPacks", adapt_ScriptCommand_GiveBoosterPacks },
	{ "Script_GiftCenterClerk", adapt_Script_GiftCenterClerk },
	{ "Script_Clerk10", adapt_Script_Clerk10 },
	{ "Script_LegendaryCardBottomLeft", adapt_Script_LegendaryCardBottomLeft },
	{ "Script_LegendaryCardTopRight", adapt_Script_LegendaryCardTopRight },
	{ "Script_LegendaryCardTopLeft", adapt_Script_LegendaryCardTopLeft },
	{ "Script_LegendaryCardBottomRight", adapt_Script_LegendaryCardBottomRight },
	{ "Script_LegendaryCardLeftSpark", adapt_Script_LegendaryCardLeftSpark },
	{ "Script_Torch", adapt_Script_Torch },
	{ "Script_Woman2", adapt_Script_Woman2 },
	{ "ScriptCommand_OpenDeckMachine", adapt_ScriptCommand_OpenDeckMachine },
	{ "ExecuteArbitraryNPCMovementFromStack", adapt_ExecuteArbitraryNPCMovementFromStack },
	{ "ScriptCommand_MoveChallengeHallNPC", adapt_ScriptCommand_MoveChallengeHallNPC },
	{ "ScriptCommand_MoveArbitraryNPC", adapt_ScriptCommand_MoveArbitraryNPC },
	{ "MaxStackEventValue", adapt_MaxStackEventValue },
	{ "SetStackEventFalse", adapt_SetStackEventFalse },
	{ "SetStackEventValue", adapt_SetStackEventValue },
	{ "SetStackEventZero", adapt_SetStackEventZero },
	{ "GetStackEventValue", adapt_GetStackEventValue },
	{ NULL, NULL },
};
