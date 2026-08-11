#include "home/deck_machine_room.h"
#include "probe.h"

#include <stdint.h>

static void adapt_Func_d96c(ProbeState *s)
{
	FuncD96cResult result = Func_d96c(s->a);
	s->a = result.a;
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}

static void adapt_Script_BeatAaron(ProbeState *s)
{
	(void)s;
	Script_BeatAaron();
}

const ProbeEntry probe_entries_deck_machine_room[] = {
	{"Func_d96c", adapt_Func_d96c},
	{"Script_BeatAaron", adapt_Script_BeatAaron},
	{NULL, NULL},
};
