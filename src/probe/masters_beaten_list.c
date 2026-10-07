/* >>> part includes */
#include "home/masters_beaten_list.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory ClearMasterBeatenList */
static void adapt_ClearMasterBeatenList(ProbeState *s)
{
	s->a = ClearMasterBeatenList(&s->f);
}
/* <<< factory ClearMasterBeatenList */

/* >>> factory AddMasterBeatenToList */
static void adapt_AddMasterBeatenToList(ProbeState *s)
{
	s->a = AddMasterBeatenToList(s->a, &s->f);
}
/* <<< factory AddMasterBeatenToList */

/* >>> factory AddAllMastersToMastersBeatenList */
static void adapt_AddAllMastersToMastersBeatenList(ProbeState *s)
{
	s->a = AddAllMastersToMastersBeatenList(&s->f);
}
/* <<< factory AddAllMastersToMastersBeatenList */

/* >>> part probe_entries_masters_beaten_list */
const ProbeEntry probe_entries_masters_beaten_list[] = {
	{ "ClearMasterBeatenList", adapt_ClearMasterBeatenList },
	{ "AddMasterBeatenToList", adapt_AddMasterBeatenToList },
	{ "AddAllMastersToMastersBeatenList", adapt_AddAllMastersToMastersBeatenList },
	{ NULL, NULL },
};
/* <<< part probe_entries_masters_beaten_list */
