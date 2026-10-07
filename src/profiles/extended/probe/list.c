#include "home/list.h"
#include "probe.h"

/* Both routines preserve every register, so nothing is written back. */

static void adapt_SetListPointer(ProbeState *s)
{
	SetListPointer((uint16_t)(s->d << 8 | s->e));
}

static void adapt_SetNextElementOfList(ProbeState *s)
{
	SetNextElementOfList(s->a);
}

const ProbeEntry probe_entries_list[] = {
	{ "SetListPointer", adapt_SetListPointer },
	{ "SetNextElementOfList", adapt_SetNextElementOfList },
	{ NULL, NULL },
};
