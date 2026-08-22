#include "home/npc_core.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory CheckIfNPCIsRonald */
static void adapt_CheckIfNPCIsRonald(ProbeState *s)
{
	s->f = CheckIfNPCIsRonald(s->a);
}
/* <<< factory CheckIfNPCIsRonald */

/* >>> factory UpdateNPCAnimation */
static void adapt_UpdateNPCAnimation(ProbeState *s)
{
	s->a = UpdateNPCAnimation();
}
/* <<< factory UpdateNPCAnimation */

/* >>> factory ApplyRandomCountToNPCAnim */
static void adapt_ApplyRandomCountToNPCAnim(ProbeState *s)
{
	s->a = ApplyRandomCountToNPCAnim();
}
/* <<< factory ApplyRandomCountToNPCAnim */

/* >>> factory SetNPCAnimation */
static void adapt_SetNPCAnimation(ProbeState *s)
{
	s->a = SetNPCAnimation(s->a);
}
/* <<< factory SetNPCAnimation */

/* >>> factory SetNPCDirection */
static void adapt_SetNPCDirection(ProbeState *s)
{
	s->a = SetNPCDirection(s->a);
}
/* <<< factory SetNPCDirection */

/* >>> factory StartNPCMovement */
static void adapt_StartNPCMovement(ProbeState *s)
{
	uint16_t bc = (uint16_t)(s->b << 8 | s->c);
	s->a = StartNPCMovement(&bc);
	s->b = (uint8_t)(bc >> 8);
	s->c = (uint8_t)bc;
}
/* <<< factory StartNPCMovement */

/* >>> factory Func_1c5e9 */
static void adapt_Func_1c5e9(ProbeState *s)
{
	s->a = Func_1c5e9();
}
/* <<< factory Func_1c5e9 */

/* >>> factory UpdateNPCPosition */
static void adapt_UpdateNPCPosition(ProbeState *s)
{
	s->a = UpdateNPCPosition();
}
/* <<< factory UpdateNPCPosition */

/* >>> factory UpdateNPCSpritePosition */
static void adapt_UpdateNPCSpritePosition(ProbeState *s)
{
	UpdateNPCSpritePositionResult result = UpdateNPCSpritePosition(s->hl);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory UpdateNPCSpritePosition */

/* >>> factory CheckIsAnNPCMoving */
static void adapt_CheckIsAnNPCMoving(ProbeState *s)
{
	CheckIsAnNPCMovingResult result = CheckIsAnNPCMoving();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory CheckIsAnNPCMoving */

/* >>> factory UpdateNPCsTilePermission */
static void adapt_UpdateNPCsTilePermission(ProbeState *s)
{
	s->a = UpdateNPCsTilePermission();
}
/* <<< factory UpdateNPCsTilePermission */

/* >>> factory SetNPCsTilePermission */
static void adapt_SetNPCsTilePermission(ProbeState *s)
{
	s->a = SetNPCsTilePermission();
}
/* <<< factory SetNPCsTilePermission */

/* >>> factory SetNPCPosition */
static void adapt_SetNPCPosition(ProbeState *s)
{
	s->a = SetNPCPosition(s->b, s->c);
}
/* <<< factory SetNPCPosition */

/* >>> factory Func_1c53f */
static void adapt_Func_1c53f(ProbeState *s)
{
	s->a = Func_1c53f();
}
/* <<< factory Func_1c53f */

/* >>> factory GetNPCDirection */
static void adapt_GetNPCDirection(ProbeState *s)
{
	s->a = GetNPCDirection();
}
/* <<< factory GetNPCDirection */

/* >>> factory GetNPCPosition */
static void adapt_GetNPCPosition(ProbeState *s)
{
	NPCPositionResult r = GetNPCPosition();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory GetNPCPosition */

/* >>> factory UpdateIsAnNPCMovingFlag */
static void adapt_UpdateIsAnNPCMovingFlag(ProbeState *s)
{
	UpdateIsAnNPCMovingFlagResult result = UpdateIsAnNPCMovingFlag(s->hl);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory UpdateIsAnNPCMovingFlag */

/* >>> factory ClearNPCs */
static void adapt_ClearNPCs(ProbeState *s)
{
	ClearNPCs();
	s->a = 0x00u;
	s->f = 0xC0u;
}
/* <<< factory ClearNPCs */

/* >>> factory SetAllNPCTilePermissions */
static void adapt_SetAllNPCTilePermissions(ProbeState *s)
{
	SetAllNPCTilePermissionsResult r = SetAllNPCTilePermissions();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory SetAllNPCTilePermissions */

/* >>> factory Func_1c557 */
static void adapt_Func_1c557(ProbeState *s)
{
	s->a = Func_1c557(s->a);
}
/* <<< factory Func_1c557 */

/* >>> factory LoadNPC */
static void adapt_LoadNPC(ProbeState *s)
{
	s->a = LoadNPC();
}
/* <<< factory LoadNPC */

/* >>> factory SetNewScriptNPC */
static void adapt_SetNewScriptNPC(ProbeState *s)
{
	SetNewScriptNPCResult result = SetNewScriptNPC(s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}
/* <<< factory SetNewScriptNPC */

/* >>> factory UnloadNPC */
static void adapt_UnloadNPC(ProbeState *s)
{
	s->a = UnloadNPC();
}
/* <<< factory UnloadNPC */

/* >>> factory Func_1c52e */
static void adapt_Func_1c52e(ProbeState *s)
{
	s->a = Func_1c52e(s->a);
}
/* <<< factory Func_1c52e */

/* >>> factory UpdateNPCMovementStep */
static void adapt_UpdateNPCMovementStep(ProbeState *s)
{
	s->a = UpdateNPCMovementStep(s->a, s->hl);
}
/* <<< factory UpdateNPCMovementStep */

const ProbeEntry probe_entries_npc_core[] = {
	{ "CheckIfNPCIsRonald", adapt_CheckIfNPCIsRonald },
	{ "UpdateNPCAnimation", adapt_UpdateNPCAnimation },
	{ "ApplyRandomCountToNPCAnim", adapt_ApplyRandomCountToNPCAnim },
	{ "SetNPCAnimation", adapt_SetNPCAnimation },
	{ "SetNPCDirection", adapt_SetNPCDirection },
	{ "StartNPCMovement", adapt_StartNPCMovement },
	{ "Func_1c5e9", adapt_Func_1c5e9 },
	{ "UpdateNPCPosition", adapt_UpdateNPCPosition },
	{ "UpdateNPCSpritePosition", adapt_UpdateNPCSpritePosition },
	{ "CheckIsAnNPCMoving", adapt_CheckIsAnNPCMoving },
	{ "UpdateNPCsTilePermission", adapt_UpdateNPCsTilePermission },
	{ "SetNPCsTilePermission", adapt_SetNPCsTilePermission },
	{ "SetNPCPosition", adapt_SetNPCPosition },
	{ "Func_1c53f", adapt_Func_1c53f },
	{ "GetNPCDirection", adapt_GetNPCDirection },
	{ "GetNPCPosition", adapt_GetNPCPosition },
	{ "UpdateIsAnNPCMovingFlag", adapt_UpdateIsAnNPCMovingFlag },
	{ "ClearNPCs", adapt_ClearNPCs },
	{ "SetAllNPCTilePermissions", adapt_SetAllNPCTilePermissions },
	{ "Func_1c557", adapt_Func_1c557 },
	{ "LoadNPC", adapt_LoadNPC },
	{ "SetNewScriptNPC", adapt_SetNewScriptNPC },
	{ "UnloadNPC", adapt_UnloadNPC },
	{ "Func_1c52e", adapt_Func_1c52e },
	{ "UpdateNPCMovementStep", adapt_UpdateNPCMovementStep },
	{ NULL, NULL },
};
