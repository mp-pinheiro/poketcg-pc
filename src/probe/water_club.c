/* >>> part includes */
#include "home/water_club.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory Preload_Amy */
static void adapt_PreloadAmy(ProbeState *s)
{
	PreloadAmyResult result = Preload_Amy();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Preload_Amy */

/* >>> factory WaterClubMovePlayer */
static void adapt_WaterClubMovePlayer(ProbeState *s)
{
	WaterClubMovePlayerResult r = WaterClubMovePlayer(s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory WaterClubMovePlayer */

/* >>> factory WaterClubAfterDuel */
static void adapt_WaterClubAfterDuel(ProbeState *s)
{
	WaterClubAfterDuelResult r = WaterClubAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory WaterClubAfterDuel */

/* >>> part probe_entries_water_club */
const ProbeEntry probe_entries_water_club[] = {
	{"Preload_Amy", adapt_PreloadAmy},
	{ "WaterClubMovePlayer", adapt_WaterClubMovePlayer },
	{ "WaterClubAfterDuel", adapt_WaterClubAfterDuel },
	{NULL, NULL},
};
/* <<< part probe_entries_water_club */
