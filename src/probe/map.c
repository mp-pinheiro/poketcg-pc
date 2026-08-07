#include "home/map.h"
#include "probe.h"

static void adapt_GetPermissionByteOfMapPosition(ProbeState *s)
{
	PermissionResult result = GetPermissionByteOfMapPosition(s->b, s->c);
	s->a = result.a;
	s->hl = result.hl;
}

static void adapt_GetPermissionOfMapPosition(ProbeState *s)
{
	s->a = GetPermissionOfMapPosition(s->b, s->c);
}

static void adapt_SetPermissionOfMapPosition(ProbeState *s)
{
	SetPermissionOfMapPosition(s->a, s->b, s->c);
}

static void adapt_UpdatePermissionOfMapPosition(ProbeState *s)
{
	s->a = UpdatePermissionOfMapPosition(s->a, s->b, s->c);
}

static void adapt_GetLoadedNPCID(ProbeState *s)
{
	PermissionResult result = GetLoadedNPCID(s->a);
	s->a = result.a;
	s->hl = result.hl;
}

static void adapt_GetItemInLoadedNPCIndex(ProbeState *s)
{
	PermissionResult result = GetItemInLoadedNPCIndex(s->a, (uint8_t)s->hl);
	s->a = result.a;
	s->hl = result.hl;
}

const ProbeEntry probe_entries_map[] = {
	{ "GetPermissionByteOfMapPosition", adapt_GetPermissionByteOfMapPosition },
	{ "GetPermissionOfMapPosition", adapt_GetPermissionOfMapPosition },
	{ "SetPermissionOfMapPosition", adapt_SetPermissionOfMapPosition },
	{ "UpdatePermissionOfMapPosition", adapt_UpdatePermissionOfMapPosition },
	{ "GetLoadedNPCID", adapt_GetLoadedNPCID },
	{ "GetItemInLoadedNPCIndex", adapt_GetItemInLoadedNPCIndex },
	{ NULL, NULL },
};
