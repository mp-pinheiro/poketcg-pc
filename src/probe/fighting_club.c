#include "home/fighting_club.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory FightingClubAfterDuel */
static void adapt_FightingClubAfterDuel(ProbeState *s)
{
	FightingClubAfterDuelResult r = FightingClubAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory FightingClubAfterDuel */

const ProbeEntry probe_entries_fighting_club[] = {
	{ "FightingClubAfterDuel", adapt_FightingClubAfterDuel },
	{ NULL, NULL },
};
