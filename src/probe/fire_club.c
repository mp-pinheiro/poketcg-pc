#include "home/fire_club.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

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

const ProbeEntry probe_entries_fire_club[] = {
	{ "FireClubAfterDuel", adapt_FireClubAfterDuel },
	{ NULL, NULL },
};
