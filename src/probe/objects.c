/* >>> part includes */
#include "generated/wram.h"
#include "home/objects.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory SetOneObjectAttributes */
static void adapt_SetOneObjectAttributes(ProbeState *s)
{
	SetOneObjectAttributes(s->e, s->d, s->c, s->b);
}
/* <<< factory SetOneObjectAttributes */

/* >>> factory ZeroObjectPositions */
static void adapt_ZeroObjectPositions(ProbeState *s)
{
	(void)s;
	ZeroObjectPositions();
}
/* <<< factory ZeroObjectPositions */

/* >>> part OAM_TOTAL_BYTES */
#define OAM_TOTAL_BYTES 160u
/* <<< part OAM_TOTAL_BYTES */

/* >>> factory SetManyObjectsAttributes */
static void adapt_SetManyObjectsAttributes(ProbeState *s)
{
	SetManyObjResult r = SetManyObjectsAttributes(s->hl, s->d, s->e);
	s->hl = r.hl;
	s->f = r.carry ? (uint8_t)(0x10u | (wOAMOffset == OAM_TOTAL_BYTES ? 0x80u : 0u)) : 0x80u;
}
/* <<< factory SetManyObjectsAttributes */

/* >>> part probe_entries_objects */
const ProbeEntry probe_entries_objects[] = {
	{ "SetOneObjectAttributes", adapt_SetOneObjectAttributes },
	{ "ZeroObjectPositions", adapt_ZeroObjectPositions },
	{ "SetManyObjectsAttributes", adapt_SetManyObjectsAttributes },
	{ NULL, NULL },
};
/* <<< part probe_entries_objects */
