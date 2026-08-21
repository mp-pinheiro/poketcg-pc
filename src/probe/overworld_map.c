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

const ProbeEntry probe_entries_overworld_map[] = {
	{ "OverworldMap_ContinuePlayerWalkingAnimation", adapt_OverworldMap_ContinuePlayerWalkingAnimation },
	{ "OverworldMap_NegateBC", adapt_OverworldMap_NegateBC },
	{ NULL, NULL },
};
