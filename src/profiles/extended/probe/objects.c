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

/* >>> part probe_entries_objects */
const ProbeEntry probe_entries_objects[] = {
	{ "SetOneObjectAttributes", adapt_SetOneObjectAttributes },
	{ "ZeroObjectPositions", adapt_ZeroObjectPositions },
	{ NULL, NULL },
};
/* <<< part probe_entries_objects */
