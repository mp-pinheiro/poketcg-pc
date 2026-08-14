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

const ProbeEntry probe_entries_overworld_map[] = {
	{ "OverworldMap_ContinuePlayerWalkingAnimation", adapt_OverworldMap_ContinuePlayerWalkingAnimation },
	{ NULL, NULL },
};
