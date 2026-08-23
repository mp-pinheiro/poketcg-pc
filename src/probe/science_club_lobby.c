#include "home/science_club_lobby.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory ScienceClubLobbyAfterDuel */
static void adapt_ScienceClubLobbyAfterDuel(ProbeState *s)
{
	ScienceClubLobbyAfterDuelResult r = ScienceClubLobbyAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory ScienceClubLobbyAfterDuel */

const ProbeEntry probe_entries_science_club_lobby[] = {
	{ "ScienceClubLobbyAfterDuel", adapt_ScienceClubLobbyAfterDuel },
	{ NULL, NULL },
};
