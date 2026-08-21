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

const ProbeEntry probe_entries_overworld_map[] = {
	{ "OverworldMap_ContinuePlayerWalkingAnimation", adapt_OverworldMap_ContinuePlayerWalkingAnimation },
	{ "OverworldMap_NegateBC", adapt_OverworldMap_NegateBC },
	{ "OverworldMap_InitVolcanoSprite", adapt_OverworldMap_InitVolcanoSprite },
	{ "OverworldMap_UpdateCursorAnimation", adapt_OverworldMap_UpdateCursorAnimation },
	{ "OverworldMap_LoadSelectedMap", adapt_OverworldMap_LoadSelectedMap },
	{ NULL, NULL },
};
