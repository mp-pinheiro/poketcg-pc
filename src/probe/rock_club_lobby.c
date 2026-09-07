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

/* >>> factory Preload_Lass3 */
static void adapt_Preload_Lass3(ProbeState *s)
{
	PreloadLass3Result r = Preload_Lass3();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Lass3 */

/* >>> factory Preload_ChrisInRockClubLobby */
static void adapt_Preload_ChrisInRockClubLobby(ProbeState *s)
{
	PreloadChrisInRockClubLobbyResult r = Preload_ChrisInRockClubLobby();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_ChrisInRockClubLobby */

const ProbeEntry probe_entries_rock_club_lobby[] = {
	{ "RockClubLobbyAfterDuel", adapt_RockClubLobbyAfterDuel },
	{ "Preload_Lass3", adapt_Preload_Lass3 },
	{ "Preload_ChrisInRockClubLobby", adapt_Preload_ChrisInRockClubLobby },
	{ NULL, NULL },
};
