#include "home/challenge_hall_lobby.h"
#include "probe.h"

static void adapt_PreloaderChallengeHallNPCs2(ProbeState *s)
{
	ChallengeHallLobbyResult result = Preload_ChallengeHallNPCs2();
	s->a = result.a;
	s->f = result.f;
}

/* >>> factory SetRonaldChallengeHallLobbyState */
static void adapt_SetRonaldChallengeHallLobbyState(ProbeState *s)
{
	SetRonaldChallengeHallLobbyStateResult r = SetRonaldChallengeHallLobbyState(s->hl, s->d, s->e);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory SetRonaldChallengeHallLobbyState */

const ProbeEntry probe_entries_challenge_hall_lobby[] = {
	{"Preload_ChallengeHallNPCs2", adapt_PreloaderChallengeHallNPCs2},
	{ "SetRonaldChallengeHallLobbyState", adapt_SetRonaldChallengeHallLobbyState },
	{NULL, NULL},
};
