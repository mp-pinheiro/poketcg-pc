#include "home/masters_beaten_list.h"
#include "probe.h"

static void adapt_AddMasterBeatenToList(ProbeState *s)
{
	MasterBeatenListResult result = AddMasterBeatenToList(s->a);
	s->a = result.a;
	s->f = result.f;
}

static void adapt_ClearMasterBeatenList(ProbeState *s)
{
	MasterBeatenListResult result = ClearMasterBeatenList();
	s->a = result.a;
	s->f = result.f;
}

const ProbeEntry probe_entries_masters_beaten_list[] = {
	{ "AddMasterBeatenToList", adapt_AddMasterBeatenToList },
	{ "ClearMasterBeatenList", adapt_ClearMasterBeatenList },
	{ NULL, NULL },
};
