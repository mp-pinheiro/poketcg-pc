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

/* >>> factory Preload_Man2 */
static void adapt_Preload_Man2(ProbeState *s)
{
	PreloadMan2Result r = Preload_Man2();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Man2 */

/* >>> factory Preload_ImakuniInWaterClubLobby */
static void adapt_Preload_ImakuniInWaterClubLobby(ProbeState *s)
{
	PreloadImakuniInWaterClubLobbyResult r = Preload_ImakuniInWaterClubLobby();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_ImakuniInWaterClubLobby */

const ProbeEntry probe_entries_water_club_lobby[] = {
	{ "WaterClubLobbyAfterDuel", adapt_WaterClubLobbyAfterDuel },
	{ "Preload_Man2", adapt_Preload_Man2 },
	{ "Preload_ImakuniInWaterClubLobby", adapt_Preload_ImakuniInWaterClubLobby },
	{ NULL, NULL },
};
