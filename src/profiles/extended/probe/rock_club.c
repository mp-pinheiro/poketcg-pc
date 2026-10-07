/* >>> part includes */
#include "home/rock_club.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory RockClubAfterDuel */
static void adapt_RockClubAfterDuel(ProbeState *s)
{
	RockClubAfterDuelResult r = RockClubAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory RockClubAfterDuel */

/* >>> part probe_entries_rock_club */
const ProbeEntry probe_entries_rock_club[] = {
	{ "RockClubAfterDuel", adapt_RockClubAfterDuel },
	{ NULL, NULL },
};
/* <<< part probe_entries_rock_club */
