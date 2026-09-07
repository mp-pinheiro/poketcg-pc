#include "home/challenge_hall_lobby.h"
#include "probe.h"

static void adapt_PreloaderChallengeHallNPCs2(ProbeState *s)
{
	ChallengeHallLobbyResult result = Preload_ChallengeHallNPCs2();
	s->a = result.a;
	s->f = result.f;
}

/* >>> factory ChallengeHallLobbyLoadMap */
static void adapt_ChallengeHallLobbyLoadMap(ProbeState *s)
{
	ChallengeHallLobbyLoadMapResult r = ChallengeHallLobbyLoadMap(s->b, s->c, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->hl = r.hl;
}
/* <<< factory ChallengeHallLobbyLoadMap */

/* >>> factory Preload_ChallengeHallNPCs1 */
static void adapt_Preload_ChallengeHallNPCs1(ProbeState *s)
{
	PreloadChallengeHallNPCs1Result r = Preload_ChallengeHallNPCs1();
	s->a = r.a; s->f = r.f;
}
/* <<< factory Preload_ChallengeHallNPCs1 */

/* >>> factory Preload_ChallengeHallLobbyRonald1 */
static void adapt_Preload_ChallengeHallLobbyRonald1(ProbeState *s)
{
	PreloadChallengeHallLobbyRonald1Result r = Preload_ChallengeHallLobbyRonald1();
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c;
	s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory Preload_ChallengeHallLobbyRonald1 */

/* >>> factory SetRonaldChallengeHallLobbyState */
static void adapt_SetRonaldChallengeHallLobbyState(ProbeState *s)
{
	SetRonaldChallengeHallLobbyStateResult r = SetRonaldChallengeHallLobbyState(s->hl, s->d, s->e);
	s->a = r.a; s->f = r.f; s->hl = r.hl;
}
/* <<< factory SetRonaldChallengeHallLobbyState */

const ProbeEntry probe_entries_challenge_hall_lobby[] = {
	{ "Preload_ChallengeHallNPCs2", adapt_PreloaderChallengeHallNPCs2 },
	{ "ChallengeHallLobbyLoadMap", adapt_ChallengeHallLobbyLoadMap },
	{ "Preload_ChallengeHallNPCs1", adapt_Preload_ChallengeHallNPCs1 },
	{ "Preload_ChallengeHallLobbyRonald1", adapt_Preload_ChallengeHallLobbyRonald1 },
	{ "SetRonaldChallengeHallLobbyState", adapt_SetRonaldChallengeHallLobbyState },
	{ NULL, NULL },
};
