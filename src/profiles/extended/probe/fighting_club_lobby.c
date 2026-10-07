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

/* >>> factory Preload_Granny1 */
static void adapt_Preload_Granny1(ProbeState *s)
{
	PreloadGranny1Result r = Preload_Granny1();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Granny1 */

/* >>> factory Preload_ImakuniInFightingClubLobby */
static void adapt_Preload_ImakuniInFightingClubLobby(ProbeState *s)
{
	PreloadImakuniInFightingClubLobbyResult r = Preload_ImakuniInFightingClubLobby();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_ImakuniInFightingClubLobby */

const ProbeEntry probe_entries_fighting_club_lobby[] = {
	{ "FightingClubLobbyAfterDuel", adapt_FightingClubLobbyAfterDuel },
	{ "Preload_Granny1", adapt_Preload_Granny1 },
	{ "Preload_ImakuniInFightingClubLobby", adapt_Preload_ImakuniInFightingClubLobby },
	{ NULL, NULL },
};
