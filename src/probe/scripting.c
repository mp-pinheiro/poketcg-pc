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

const ProbeEntry probe_entries_scripting[] = {
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
	{ NULL, NULL },
};
