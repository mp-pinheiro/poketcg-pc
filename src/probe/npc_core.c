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
	{ NULL, NULL },
};
