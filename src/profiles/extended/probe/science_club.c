#include "home/science_club.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory Preload_Joseph */
static void adapt_Preload_Joseph(ProbeState *s)
{
	PreloadJosephResult r = Preload_Joseph();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Joseph */

/* >>> factory ScienceClubAfterDuel */
static void adapt_ScienceClubAfterDuel(ProbeState *s)
{
	ScienceClubAfterDuelResult r = ScienceClubAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory ScienceClubAfterDuel */

const ProbeEntry probe_entries_science_club[] = {
	{ "Preload_Joseph", adapt_Preload_Joseph },
	{ "ScienceClubAfterDuel", adapt_ScienceClubAfterDuel },
	{ NULL, NULL },
};
