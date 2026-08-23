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

const ProbeEntry probe_entries_psychic_club_lobby[] = {
	{ "PsychicClubLobbyLoadMap", adapt_PsychicClubLobbyLoadMap },
	{ NULL, NULL },
};
