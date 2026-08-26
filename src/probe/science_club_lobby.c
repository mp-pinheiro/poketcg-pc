#include "home/science_club_lobby.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory ScienceClubLobbyAfterDuel */
static void adapt_ScienceClubLobbyAfterDuel(ProbeState *s)
{
	ScienceClubLobbyAfterDuelResult r = ScienceClubLobbyAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory ScienceClubLobbyAfterDuel */


/* >>> factory Script_Specs2 */
static void adapt_Script_Specs2(ProbeState *s)
{
	ScriptSpecs2Result r = Script_Specs2();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory Script_Specs2 */

const ProbeEntry probe_entries_science_club_lobby[] = {
	{ "Script_Specs2", adapt_Script_Specs2 },
	{ "ScienceClubLobbyAfterDuel", adapt_ScienceClubLobbyAfterDuel },
	{ NULL, NULL },
};
