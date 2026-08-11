#include "home/science_club_lobby.h"
#include "probe.h"

static void adapt_Script_Specs2(ProbeState *s)
{
	Script_Specs2();
	(void)s;
}

const ProbeEntry probe_entries_science_club_lobby[] = {
	{"Script_Specs2", adapt_Script_Specs2},
	{NULL, NULL},
};
