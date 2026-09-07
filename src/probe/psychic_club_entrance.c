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

/* >>> factory Func_e8a0 */
static void adapt_Func_e8a0(ProbeState *s)
{
	Func_e8a0Result r = Func_e8a0(s->a, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Func_e8a0 */

/* >>> factory Preload_Ronald1InClubEntrance */
static void adapt_Preload_Ronald1InClubEntrance(ProbeState *s)
{
	PreloadRonaldInClubEntranceResult r = Preload_Ronald1InClubEntrance();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Ronald1InClubEntrance */

/* >>> factory Preload_Ronald2InClubEntrance */
static void adapt_Preload_Ronald2InClubEntrance(ProbeState *s)
{
	PreloadRonaldInClubEntranceResult r = Preload_Ronald2InClubEntrance(s->b, s->c, s->d, s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Ronald2InClubEntrance */

/* >>> factory Preload_Ronald3InClubEntrance */
static void adapt_Preload_Ronald3InClubEntrance(ProbeState *s)
{
	PreloadRonaldInClubEntranceResult r = Preload_Ronald3InClubEntrance(s->b, s->c, s->d, s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Ronald3InClubEntrance */

const ProbeEntry probe_entries_psychic_club_entrance[] = {
	{ "TryFirstRonaldEncounter", adapt_TryFirstRonaldEncounter },
	{ "TryFirstRonaldDuel", adapt_TryFirstRonaldDuel },
	{ "TrySecondRonaldDuel", adapt_TrySecondRonaldDuel },
	{ "LoadClubEntrance", adapt_LoadClubEntrance },
	{ "ClubEntranceAfterDuel", adapt_ClubEntranceAfterDuel },
	{ "Func_e8a0", adapt_Func_e8a0 },
	{ "Preload_Ronald1InClubEntrance", adapt_Preload_Ronald1InClubEntrance },
	{ "Preload_Ronald2InClubEntrance", adapt_Preload_Ronald2InClubEntrance },
	{ "Preload_Ronald3InClubEntrance", adapt_Preload_Ronald3InClubEntrance },
	{ NULL, NULL },
};
