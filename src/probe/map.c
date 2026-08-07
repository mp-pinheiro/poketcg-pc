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

const ProbeEntry probe_entries_map[] = {
	{ "GetPermissionByteOfMapPosition", adapt_GetPermissionByteOfMapPosition },
	{ "GetPermissionOfMapPosition", adapt_GetPermissionOfMapPosition },
	{ "SetPermissionOfMapPosition", adapt_SetPermissionOfMapPosition },
	{ "UpdatePermissionOfMapPosition", adapt_UpdatePermissionOfMapPosition },
	{ NULL, NULL },
};
