#include "home/overworld.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory Func_c6cc */
static void adapt_Func_c6cc(ProbeState *s)
{
	s->a = Func_c6cc(s->a);
}
/* <<< factory Func_c6cc */

/* >>> factory Func_c6d4 */
static void adapt_Func_c6d4(ProbeState *s)
{
	s->a = Func_c6d4(s->a);
}
/* <<< factory Func_c6d4 */

/* >>> factory Func_c6f7 */
static void adapt_Func_c6f7(ProbeState *s)
{
	s->a = Func_c6f7(&s->hl);
}
/* <<< factory Func_c6f7 */

/* >>> factory SetOverworldNPCFlags */
static void adapt_SetOverworldNPCFlags(ProbeState *s)
{
	OverworldNPCFlagsResult result = SetOverworldNPCFlags(s->a);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory SetOverworldNPCFlags */

/* >>> factory Func_c158 */
static void adapt_Func_c158(ProbeState *s)
{
	s->a = Func_c158();
}
/* <<< factory Func_c158 */

/* >>> factory Func_c184 */
static void adapt_Func_c184(ProbeState *s)
{
	Func_c184();
}
/* <<< factory Func_c184 */

/* >>> factory WhiteOutDMGPals */
static void adapt_WhiteOutDMGPals(ProbeState *s)
{
	(void)s;
	WhiteOutDMGPals();
}
/* <<< factory WhiteOutDMGPals */

/* >>> factory Func_c1f8 */
static void adapt_Func_c1f8(ProbeState *s)
{
	(void)s;
	Func_c1f8();
}
/* <<< factory Func_c1f8 */

/* >>> factory BackupPlayerPosition */
static void adapt_BackupPlayerPosition(ProbeState *s)
{
	(void)s;
	BackupPlayerPosition();
}
/* <<< factory BackupPlayerPosition */

/* >>> factory Func_c469 */
static void adapt_Func_c469(ProbeState *s)
{
	Func_c469();
}
/* <<< factory Func_c469 */



/* >>> factory SetScreenScrollWram */
static void adapt_SetScreenScrollWram(ProbeState *s)
{
	s->a = SetScreenScrollWram();
}
/* <<< factory SetScreenScrollWram */



/* >>> factory SetScreenScroll */
static void adapt_SetScreenScroll(ProbeState *s)
{
	SetScreenScroll();
}
/* <<< factory SetScreenScroll */



/* >>> factory Func_c70d */
static void adapt_Func_c70d(ProbeState *s)
{
	FuncC70dResult r = Func_c70d();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Func_c70d */

/* >>> factory Func_c430 */
static void adapt_Func_c430(ProbeState *s)
{
	(void)s;
	Func_c430();
}
/* <<< factory Func_c430 */

/* >>> factory Func_c41c */
static void adapt_Func_c41c(ProbeState *s)
{
	(void)s;
	Func_c41c();
}
/* <<< factory Func_c41c */

/* >>> factory Func_c3ca */
static void adapt_Func_c3ca(ProbeState *s)
{
	FuncC3caResult result = Func_c3ca(s->b, s->c, s->d, s->e);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Func_c3ca */

/* >>> factory GetDirectionFromDPad */
static void adapt_GetDirectionFromDPad(ProbeState *s)
{
	GetDirectionFromDPadResult result = GetDirectionFromDPad(s->a);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory GetDirectionFromDPad */

/* >>> factory Func_c694 */
static void adapt_Func_c694(ProbeState *s)
{
	Func_c694(s->a, s->c);
}
/* <<< factory Func_c694 */

/* >>> factory FindPlayerMovementWithOffset */
static void adapt_FindPlayerMovementWithOffset(ProbeState *s)
{
	FindPlayerMovementWithOffsetResult result = FindPlayerMovementWithOffset(s->a);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory FindPlayerMovementWithOffset */

/* >>> factory BackupObjectPalettes */
static void adapt_BackupObjectPalettes(ProbeState *s)
{
	(void)s;
	BackupObjectPalettes();
}
/* <<< factory BackupObjectPalettes */

/* >>> factory AttemptPlayerMovement */
static void adapt_AttemptPlayerMovement(ProbeState *s)
{
	AttemptPlayerMovement(s->b, s->c);
}
/* <<< factory AttemptPlayerMovement */

/* >>> factory FindPlayerMovementFromDirection */
static void adapt_FindPlayerMovementFromDirection(ProbeState *s)
{
	FindPlayerMovementWithOffsetResult result = FindPlayerMovementFromDirection();
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory FindPlayerMovementFromDirection */

/* >>> factory Func_c1a0 */
static void adapt_Func_c1a0(ProbeState *s)
{
	uint8_t f = s->f;
	FuncC1A0Result result = Func_c1a0(s->hl);
	s->a = result.a;
	s->f = f;
	s->hl = result.hl;
}
/* <<< factory Func_c1a0 */

/* >>> factory PauseMenu_Exit */
static void adapt_PauseMenu_Exit(ProbeState *s)
{
	(void)s;
	PauseMenu_Exit();
}
/* <<< factory PauseMenu_Exit */

/* >>> factory AttemptPlayerMovementFromDirection */
static void adapt_AttemptPlayerMovementFromDirection(ProbeState *s)
{
	AttemptPlayerMovementFromDirection();
	(void)s;
}
/* <<< factory AttemptPlayerMovementFromDirection */

/* >>> factory Func_c687 */
static void adapt_Func_c687(ProbeState *s)
{
	Func_c687();
}
/* <<< factory Func_c687 */

/* >>> factory Func_c36a */
static void adapt_Func_c36a(ProbeState *s)
{
	(void)s;
	Func_c36a();
}
/* <<< factory Func_c36a */

/* >>> factory Func_c915 */
static void adapt_Func_c915(ProbeState *s)
{
	FuncC3caResult result = Func_c915();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Func_c915 */

/* >>> factory StartScriptedMovement */
static void adapt_StartScriptedMovement(ProbeState *s)
{
	StartScriptedMovement();
	(void)s;
}
/* <<< factory StartScriptedMovement */

/* >>> factory RestoreObjectPalettes */
static void adapt_RestoreObjectPalettes(ProbeState *s)
{
	(void)s;
	RestoreObjectPalettes();
}
/* <<< factory RestoreObjectPalettes */

/* >>> factory Func_c3ff */
static void adapt_Func_c3ff(ProbeState *s)
{
	(void)s;
	Func_c3ff();
}
/* <<< factory Func_c3ff */

/* >>> factory Func_c49c */
static void adapt_Func_c49c(ProbeState *s)
{
	(void)s;
	Func_c49c();
}
/* <<< factory Func_c49c */

/* >>> factory Func_c58b */
static void adapt_Func_c58b(ProbeState *s)
{
	(void)s;
	Func_c58b();
}
/* <<< factory Func_c58b */

/* >>> factory UpdatePlayerSprite */
static void adapt_UpdatePlayerSprite(ProbeState *s)
{
	UpdatePlayerSprite();
}
/* <<< factory UpdatePlayerSprite */

/* >>> factory UpdatePlayerDirection */
static void adapt_UpdatePlayerDirection(ProbeState *s)
{
	UpdatePlayerDirection(s->a);
}
/* <<< factory UpdatePlayerDirection */

/* >>> factory UpdatePlayerDirectionFromDPad */
static void adapt_UpdatePlayerDirectionFromDPad(ProbeState *s)
{
	UpdatePlayerDirectionFromDPad(s->a);
}
/* <<< factory UpdatePlayerDirectionFromDPad */

/* >>> factory SetOverworldDoFrameFunction */
static void adapt_SetOverworldDoFrameFunction(ProbeState *s)
{
	(void)s;
	SetOverworldDoFrameFunction();
}
/* <<< factory SetOverworldDoFrameFunction */

/* >>> factory Func_c3ee */
static void adapt_Func_c3ee(ProbeState *s)
{
	(void)s;
	Func_c3ee();
}
/* <<< factory Func_c3ee */

/* >>> factory Func_c66c */
static void adapt_Func_c66c(ProbeState *s)
{
	(void)s;
	Func_c66c();
}
/* <<< factory Func_c66c */

/* >>> factory Func_c4b9 */
static void adapt_Func_c4b9(ProbeState *s)
{
	(void)s;
	Func_c4b9();
}
/* <<< factory Func_c4b9 */

/* >>> factory DecompressPermissionMap */
static void adapt_DecompressPermissionMap(ProbeState *s)
{
	DecompressPermissionMapResult r = DecompressPermissionMap(s->hl);
	s->hl = r.hl;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory DecompressPermissionMap */

const ProbeEntry probe_entries_overworld[] = {
	{ "Func_c6cc", adapt_Func_c6cc },
	{ "Func_c6d4", adapt_Func_c6d4 },
	{ "Func_c6f7", adapt_Func_c6f7 },
	{ "SetOverworldNPCFlags", adapt_SetOverworldNPCFlags },
	{ "Func_c158", adapt_Func_c158 },
	{ "Func_c184", adapt_Func_c184 },
	{ "WhiteOutDMGPals", adapt_WhiteOutDMGPals },
	{ "Func_c1f8", adapt_Func_c1f8 },
	{ "BackupPlayerPosition", adapt_BackupPlayerPosition },
	{ "Func_c469", adapt_Func_c469 },
	{ "SetScreenScrollWram", adapt_SetScreenScrollWram },
	{ "SetScreenScroll", adapt_SetScreenScroll },
	{ "Func_c70d", adapt_Func_c70d },
	{ "Func_c430", adapt_Func_c430 },
	{ "Func_c41c", adapt_Func_c41c },
	{ "Func_c3ca", adapt_Func_c3ca },
	{ "GetDirectionFromDPad", adapt_GetDirectionFromDPad },
	{ "Func_c694", adapt_Func_c694 },
	{ "FindPlayerMovementWithOffset", adapt_FindPlayerMovementWithOffset },
	{ "BackupObjectPalettes", adapt_BackupObjectPalettes },
	{ "AttemptPlayerMovement", adapt_AttemptPlayerMovement },
	{ "FindPlayerMovementFromDirection", adapt_FindPlayerMovementFromDirection },
	{ "Func_c1a0", adapt_Func_c1a0 },
	{ "PauseMenu_Exit", adapt_PauseMenu_Exit },
	{ "AttemptPlayerMovementFromDirection", adapt_AttemptPlayerMovementFromDirection },
	{ "Func_c687", adapt_Func_c687 },
	{ "Func_c36a", adapt_Func_c36a },
	{ "Func_c915", adapt_Func_c915 },
	{ "StartScriptedMovement", adapt_StartScriptedMovement },
	{ "RestoreObjectPalettes", adapt_RestoreObjectPalettes },
	{ "Func_c3ff", adapt_Func_c3ff },
	{ "Func_c49c", adapt_Func_c49c },
	{ "Func_c58b", adapt_Func_c58b },
	{ "UpdatePlayerSprite", adapt_UpdatePlayerSprite },
	{ "UpdatePlayerDirection", adapt_UpdatePlayerDirection },
	{ "UpdatePlayerDirectionFromDPad", adapt_UpdatePlayerDirectionFromDPad },
	{ "SetOverworldDoFrameFunction", adapt_SetOverworldDoFrameFunction },
	{ "Func_c3ee", adapt_Func_c3ee },
	{ "Func_c66c", adapt_Func_c66c },
	{ "Func_c4b9", adapt_Func_c4b9 },
	{ "DecompressPermissionMap", adapt_DecompressPermissionMap },
	{ NULL, NULL },
};
