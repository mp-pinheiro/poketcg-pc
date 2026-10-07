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

/* >>> factory Preload_Gal2 */
static void adapt_Preload_Gal2(ProbeState *s)
{
	PreloadGal2Result r = Preload_Gal2();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Gal2 */

const ProbeEntry probe_entries_grass_club_lobby[] = {
	{ "GrassClubLobbyAfterDuel", adapt_GrassClubLobbyAfterDuel },
	{ "Preload_Gal2", adapt_Preload_Gal2 },
	{ NULL, NULL },
};
