#include "home/challenge_hall_lobby.h"
#include "probe.h"

static void adapt_PreloaderChallengeHallNPCs2(ProbeState *s)
{
	ChallengeHallLobbyResult result = Preload_ChallengeHallNPCs2();
	s->a = result.a;
	s->f = result.f;
}

const ProbeEntry probe_entries_challenge_hall_lobby[] = {
	{"Preload_ChallengeHallNPCs2", adapt_PreloaderChallengeHallNPCs2},
	{NULL, NULL},
};
