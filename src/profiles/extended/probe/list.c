/* >>> part includes */
#include "home/list.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory SetListPointer */
/* Both routines preserve every register, so nothing is written back. */

static void adapt_SetListPointer(ProbeState *s)
{
	SetListPointer((uint16_t)(s->d << 8 | s->e));
}
/* <<< factory SetListPointer */

/* >>> factory SetNextElementOfList */
static void adapt_SetNextElementOfList(ProbeState *s)
{
	SetNextElementOfList(s->a);
}
/* <<< factory SetNextElementOfList */

/* >>> part probe_entries_list */
const ProbeEntry probe_entries_list[] = {
	{ "SetListPointer", adapt_SetListPointer },
	{ "SetNextElementOfList", adapt_SetNextElementOfList },
	{ NULL, NULL },
};
/* <<< part probe_entries_list */
