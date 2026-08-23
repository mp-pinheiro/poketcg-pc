#include "home/water_club_lobby.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory WaterClubLobbyAfterDuel */
static void adapt_WaterClubLobbyAfterDuel(ProbeState *s)
{
	WaterClubLobbyAfterDuelResult r = WaterClubLobbyAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory WaterClubLobbyAfterDuel */

const ProbeEntry probe_entries_water_club_lobby[] = {
	{ "WaterClubLobbyAfterDuel", adapt_WaterClubLobbyAfterDuel },
	{ NULL, NULL },
};
