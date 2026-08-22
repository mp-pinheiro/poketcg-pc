#include "home/overworld_map.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory OverworldMap_ContinuePlayerWalkingAnimation */
static void adapt_OverworldMap_ContinuePlayerWalkingAnimation(ProbeState *s)
{
	OverworldMap_ContinuePlayerWalkingAnimation();
}
/* <<< factory OverworldMap_ContinuePlayerWalkingAnimation */

/* >>> factory OverworldMap_NegateBC */
static void adapt_OverworldMap_NegateBC(ProbeState *s)
{
	OverworldMapNegateBCResult result = OverworldMap_NegateBC(s->b, s->c);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory OverworldMap_NegateBC */

/* >>> factory OverworldMap_InitVolcanoSprite */
static void adapt_OverworldMap_InitVolcanoSprite(ProbeState *s)
{
	OverworldMap_InitVolcanoSprite(s->f);
}
/* <<< factory OverworldMap_InitVolcanoSprite */

/* >>> factory OverworldMap_UpdateCursorAnimation */
static void adapt_OverworldMap_UpdateCursorAnimation(ProbeState *s)
{
	(void)s;
	OverworldMap_UpdateCursorAnimation();
}
/* <<< factory OverworldMap_UpdateCursorAnimation */

/* >>> factory OverworldMap_LoadSelectedMap */
static void adapt_OverworldMap_LoadSelectedMap(ProbeState *s)
{
	(void)s;
	OverworldMap_LoadSelectedMap();
}
/* <<< factory OverworldMap_LoadSelectedMap */

/* >>> factory OverworldMap_InitPlayerEastWestMovement */
static void adapt_OverworldMap_InitPlayerEastWestMovement(ProbeState *s)
{
	OverworldMap_InitPlayerEastWestMovement(s->b, s->c);
}
/* <<< factory OverworldMap_InitPlayerEastWestMovement */

/* >>> factory OverworldMap_GetOWMapID */
static void adapt_OverworldMap_GetOWMapID(ProbeState *s)
{
	s->a = OverworldMap_GetOWMapID();
}
/* <<< factory OverworldMap_GetOWMapID */

/* >>> factory OverworldMap_InitCursorSprite */
static void adapt_OverworldMap_InitCursorSprite(ProbeState *s)
{
	OverworldMap_InitCursorSprite();
}
/* <<< factory OverworldMap_InitCursorSprite */

/* >>> factory OverworldMap_GetMapPosition */
static void adapt_OverworldMap_GetMapPosition(ProbeState *s)
{
	OverworldMapGetMapPositionResult result = OverworldMap_GetMapPosition(s->a, s->d, s->e);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
}
/* <<< factory OverworldMap_GetMapPosition */

/* >>> factory OverworldMap_SetSpritePosition */
static void adapt_OverworldMap_SetSpritePosition(ProbeState *s)
{
	OverworldMap_SetSpritePosition(s->a, s->d, s->e);
}
/* <<< factory OverworldMap_SetSpritePosition */

/* >>> factory OverworldMap_InitPlayerNorthSouthMovement */
static void adapt_OverworldMap_InitPlayerNorthSouthMovement(ProbeState *s)
{
	OverworldMap_InitPlayerNorthSouthMovement(s->b, s->c);
}
/* <<< factory OverworldMap_InitPlayerNorthSouthMovement */

/* >>> factory OverworldMap_PrintMapName */
static void adapt_OverworldMap_PrintMapName(ProbeState *s)
{
	OverworldMap_PrintMapName();
}
/* <<< factory OverworldMap_PrintMapName */

const ProbeEntry probe_entries_overworld_map[] = {
	{ "OverworldMap_ContinuePlayerWalkingAnimation", adapt_OverworldMap_ContinuePlayerWalkingAnimation },
	{ "OverworldMap_NegateBC", adapt_OverworldMap_NegateBC },
	{ "OverworldMap_InitVolcanoSprite", adapt_OverworldMap_InitVolcanoSprite },
	{ "OverworldMap_UpdateCursorAnimation", adapt_OverworldMap_UpdateCursorAnimation },
	{ "OverworldMap_LoadSelectedMap", adapt_OverworldMap_LoadSelectedMap },
	{ "OverworldMap_InitPlayerEastWestMovement", adapt_OverworldMap_InitPlayerEastWestMovement },
	{ "OverworldMap_GetOWMapID", adapt_OverworldMap_GetOWMapID },
	{ "OverworldMap_InitCursorSprite", adapt_OverworldMap_InitCursorSprite },
	{ "OverworldMap_GetMapPosition", adapt_OverworldMap_GetMapPosition },
	{ "OverworldMap_SetSpritePosition", adapt_OverworldMap_SetSpritePosition },
	{ "OverworldMap_InitPlayerNorthSouthMovement", adapt_OverworldMap_InitPlayerNorthSouthMovement },
	{ "OverworldMap_PrintMapName", adapt_OverworldMap_PrintMapName },
	{ NULL, NULL },
};
