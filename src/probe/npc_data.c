#include "home/npc_data.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory GetNPCHeaderPointer */
static void adapt_GetNPCHeaderPointer(ProbeState *s)
{
	GetNPCHeaderPointerResult result = GetNPCHeaderPointer(s->a);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory GetNPCHeaderPointer */

/* >>> factory SetNPCOpponentNameAndPortrait */
static void adapt_SetNPCOpponentNameAndPortrait(ProbeState *s)
{
	SetNPCOpponentNameAndPortrait(s->a);
}
/* <<< factory SetNPCOpponentNameAndPortrait */

const ProbeEntry probe_entries_npc_data[] = {
	{ "GetNPCHeaderPointer", adapt_GetNPCHeaderPointer },
	{ "SetNPCOpponentNameAndPortrait", adapt_SetNPCOpponentNameAndPortrait },
	{ NULL, NULL },
};
