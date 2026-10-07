/* >>> part includes */
#include "home/fire_club.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory FireClubAfterDuel */
static void adapt_FireClubAfterDuel(ProbeState *s)
{
	FireClubAfterDuelResult r = FireClubAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory FireClubAfterDuel */

/* >>> part probe_entries_fire_club */
const ProbeEntry probe_entries_fire_club[] = {
	{ "FireClubAfterDuel", adapt_FireClubAfterDuel },
	{ NULL, NULL },
};
/* <<< part probe_entries_fire_club */
