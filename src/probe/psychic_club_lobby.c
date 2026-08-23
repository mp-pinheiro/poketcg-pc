#include "home/psychic_club_lobby.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory PsychicClubLobbyLoadMap */
static void adapt_PsychicClubLobbyLoadMap(ProbeState *s)
{
	PsychicClubLobbyLoadMapResult r = PsychicClubLobbyLoadMap(s->b, s->c, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory PsychicClubLobbyLoadMap */

/* >>> factory PsychicClubLobbyAfterDuel */
static void adapt_PsychicClubLobbyAfterDuel(ProbeState *s)
{
	PsychicClubLobbyAfterDuelResult r = PsychicClubLobbyAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory PsychicClubLobbyAfterDuel */

const ProbeEntry probe_entries_psychic_club_lobby[] = {
	{ "PsychicClubLobbyLoadMap", adapt_PsychicClubLobbyLoadMap },
	{ "PsychicClubLobbyAfterDuel", adapt_PsychicClubLobbyAfterDuel },
	{ NULL, NULL },
};
