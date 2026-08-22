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

/* >>> factory GetNPCNameAndScript */
static void adapt_GetNPCNameAndScript(ProbeState *s)
{
	GetNPCNameAndScriptResult result = GetNPCNameAndScript(s->a);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory GetNPCNameAndScript */

/* >>> factory LoadNPCSpriteData */
static void adapt_LoadNPCSpriteData(ProbeState *s)
{
	LoadNPCSpriteDataResult result = LoadNPCSpriteData(s->a, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory LoadNPCSpriteData */

const ProbeEntry probe_entries_npc_data[] = {
	{ "GetNPCHeaderPointer", adapt_GetNPCHeaderPointer },
	{ "SetNPCOpponentNameAndPortrait", adapt_SetNPCOpponentNameAndPortrait },
	{ "GetNPCNameAndScript", adapt_GetNPCNameAndScript },
	{ "LoadNPCSpriteData", adapt_LoadNPCSpriteData },
	{ NULL, NULL },
};
