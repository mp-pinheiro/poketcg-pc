#include "home/grass_club.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory GrassClubAfterDuel */
static void adapt_GrassClubAfterDuel(ProbeState *s)
{
	GrassClubAfterDuelResult r = GrassClubAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory GrassClubAfterDuel */

const ProbeEntry probe_entries_grass_club[] = {
	{ "GrassClubAfterDuel", adapt_GrassClubAfterDuel },
	{ NULL, NULL },
};
