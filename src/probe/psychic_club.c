#include "home/psychic_club.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory PsychicClubAfterDuel */
static void adapt_PsychicClubAfterDuel(ProbeState *s)
{
	PsychicClubAfterDuelResult r = PsychicClubAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory PsychicClubAfterDuel */

const ProbeEntry probe_entries_psychic_club[] = {
	{ "PsychicClubAfterDuel", adapt_PsychicClubAfterDuel },
	{ NULL, NULL },
};
