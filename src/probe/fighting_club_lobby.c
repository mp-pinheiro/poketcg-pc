#include "home/fighting_club_lobby.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory FightingClubLobbyAfterDuel */
static void adapt_FightingClubLobbyAfterDuel(ProbeState *s)
{
	FightingClubLobbyAfterDuelResult r = FightingClubLobbyAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory FightingClubLobbyAfterDuel */

const ProbeEntry probe_entries_fighting_club_lobby[] = {
	{ "FightingClubLobbyAfterDuel", adapt_FightingClubLobbyAfterDuel },
	{ NULL, NULL },
};
