#include "home/rock_club_lobby.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory RockClubLobbyAfterDuel */
static void adapt_RockClubLobbyAfterDuel(ProbeState *s)
{
	RockClubLobbyAfterDuelResult r = RockClubLobbyAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory RockClubLobbyAfterDuel */

const ProbeEntry probe_entries_rock_club_lobby[] = {
	{ "RockClubLobbyAfterDuel", adapt_RockClubLobbyAfterDuel },
	{ NULL, NULL },
};
