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

/* >>> factory _GetNPCDuelConfigurations */
static void adapt__GetNPCDuelConfigurations(ProbeState *s)
{
	_GetNPCDuelDuelConfigurationsResult r = _GetNPCDuelConfigurations(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory _GetNPCDuelConfigurations */

/* >>> factory SetNPCDeckIDAndDuelTheme */
static void adapt_SetNPCDeckIDAndDuelTheme(ProbeState *s)
{
	SetNPCDeckIDAndDuelThemeResult r = SetNPCDeckIDAndDuelTheme(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory SetNPCDeckIDAndDuelTheme */

const ProbeEntry probe_entries_npc_data[] = {
	{ "GetNPCHeaderPointer", adapt_GetNPCHeaderPointer },
	{ "SetNPCOpponentNameAndPortrait", adapt_SetNPCOpponentNameAndPortrait },
	{ "GetNPCNameAndScript", adapt_GetNPCNameAndScript },
	{ "LoadNPCSpriteData", adapt_LoadNPCSpriteData },
	{ "_GetNPCDuelConfigurations", adapt__GetNPCDuelConfigurations },
	{ "SetNPCDeckIDAndDuelTheme", adapt_SetNPCDeckIDAndDuelTheme },
	{ NULL, NULL },
};
