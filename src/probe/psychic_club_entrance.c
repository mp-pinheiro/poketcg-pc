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

/* >>> factory TryFirstRonaldDuel */
static void adapt_TryFirstRonaldDuel(ProbeState *s)
{
	TryFirstRonaldDuelResult r = TryFirstRonaldDuel(s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory TryFirstRonaldDuel */

/* >>> factory TrySecondRonaldDuel */
static void adapt_TrySecondRonaldDuel(ProbeState *s)
{
	TrySecondRonaldDuelResult r = TrySecondRonaldDuel(s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory TrySecondRonaldDuel */

/* >>> factory LoadClubEntrance */
static void adapt_LoadClubEntrance(ProbeState *s)
{
	(void)s;
	LoadClubEntrance();
}
/* <<< factory LoadClubEntrance */

/* >>> factory ClubEntranceAfterDuel */
static void adapt_ClubEntranceAfterDuel(ProbeState *s)
{
	ClubEntranceAfterDuelResult r = ClubEntranceAfterDuel();
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory ClubEntranceAfterDuel */

const ProbeEntry probe_entries_psychic_club_entrance[] = {
	{ "TryFirstRonaldEncounter", adapt_TryFirstRonaldEncounter },
	{ "TryFirstRonaldDuel", adapt_TryFirstRonaldDuel },
	{ "TrySecondRonaldDuel", adapt_TrySecondRonaldDuel },
	{ "LoadClubEntrance", adapt_LoadClubEntrance },
	{ "ClubEntranceAfterDuel", adapt_ClubEntranceAfterDuel },
	{ NULL, NULL },
};
