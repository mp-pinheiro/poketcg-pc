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

/* >>> factory Preload_ChrisInFightingClub */
static void adapt_Preload_ChrisInFightingClub(ProbeState *s)
{
	PreloadPupilInFightingClubResult r = Preload_ChrisInFightingClub();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_ChrisInFightingClub */

/* >>> factory Preload_MichaelInFightingClub */
static void adapt_Preload_MichaelInFightingClub(ProbeState *s)
{
	PreloadPupilInFightingClubResult r = Preload_MichaelInFightingClub();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_MichaelInFightingClub */

/* >>> factory Preload_JessicaInFightingClub */
static void adapt_Preload_JessicaInFightingClub(ProbeState *s)
{
	PreloadPupilInFightingClubResult r = Preload_JessicaInFightingClub();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_JessicaInFightingClub */

const ProbeEntry probe_entries_fighting_club[] = {
	{ "FightingClubAfterDuel", adapt_FightingClubAfterDuel },
	{ "Preload_ChrisInFightingClub", adapt_Preload_ChrisInFightingClub },
	{ "Preload_MichaelInFightingClub", adapt_Preload_MichaelInFightingClub },
	{ "Preload_JessicaInFightingClub", adapt_Preload_JessicaInFightingClub },
	{ NULL, NULL },
};
