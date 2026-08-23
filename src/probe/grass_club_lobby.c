#include "home/grass_club_lobby.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory GrassClubLobbyAfterDuel */
static void adapt_GrassClubLobbyAfterDuel(ProbeState *s)
{
	GrassClubLobbyAfterDuelResult r = GrassClubLobbyAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory GrassClubLobbyAfterDuel */

const ProbeEntry probe_entries_grass_club_lobby[] = {
	{ "GrassClubLobbyAfterDuel", adapt_GrassClubLobbyAfterDuel },
	{ NULL, NULL },
};
