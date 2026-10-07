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

/* >>> factory Preload_Murray2 */
static void adapt_Preload_Murray2(ProbeState *s)
{
	Preload_Murray2Result r = Preload_Murray2(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Murray2 */

/* >>> factory Preload_Murray1 */
static void adapt_Preload_Murray1(ProbeState *s)
{
	Preload_Murray2Result r = Preload_Murray1(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Murray1 */

const ProbeEntry probe_entries_psychic_club[] = {
	{ "PsychicClubAfterDuel", adapt_PsychicClubAfterDuel },
	{ "Preload_Murray2", adapt_Preload_Murray2 },
	{ "Preload_Murray1", adapt_Preload_Murray1 },
	{ NULL, NULL },
};
