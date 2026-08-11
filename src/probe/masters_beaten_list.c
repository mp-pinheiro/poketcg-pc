#include "home/masters_beaten_list.h"
#include "probe.h"

static void adapt_ClearMasterBeatenList(ProbeState *s)
{
	s->a = ClearMasterBeatenList(&s->f);
}

static void adapt_AddMasterBeatenToList(ProbeState *s)
{
	s->a = AddMasterBeatenToList(s->a, &s->f);
}

const ProbeEntry probe_entries_masters_beaten_list[] = {
	{ "ClearMasterBeatenList", adapt_ClearMasterBeatenList },
	{ "AddMasterBeatenToList", adapt_AddMasterBeatenToList },
	{ NULL, NULL },
};
