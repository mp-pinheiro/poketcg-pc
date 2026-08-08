#include "generated/wram.h"
#include "home/objects.h"
#include "probe.h"

static void adapt_SetOneObjectAttributes(ProbeState *s)
{
	SetOneObjectAttributes(s->e, s->d, s->c, s->b);
}

static void adapt_ZeroObjectPositions(ProbeState *s)
{
	(void)s;
	ZeroObjectPositions();
}

#define OAM_TOTAL_BYTES 160u

static void adapt_SetManyObjectsAttributes(ProbeState *s)
{
	SetManyObjResult r = SetManyObjectsAttributes(s->hl, s->d, s->e);
	s->hl = r.hl;
	s->f = r.carry ? (uint8_t)(0x10u | (wOAMOffset == OAM_TOTAL_BYTES ? 0x80u : 0u)) : 0x80u;
}

const ProbeEntry probe_entries_objects[] = {
	{ "SetOneObjectAttributes", adapt_SetOneObjectAttributes },
	{ "ZeroObjectPositions", adapt_ZeroObjectPositions },
	{ "SetManyObjectsAttributes", adapt_SetManyObjectsAttributes },
	{ NULL, NULL },
};
