#include "home/psychic_club_entrance.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory TryFirstRonaldEncounter */
static void adapt_TryFirstRonaldEncounter(ProbeState *s)
{
	TryFirstRonaldEncounterResult r = TryFirstRonaldEncounter(s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory TryFirstRonaldEncounter */

const ProbeEntry probe_entries_psychic_club_entrance[] = {
	{ "TryFirstRonaldEncounter", adapt_TryFirstRonaldEncounter },
	{ NULL, NULL },
};
