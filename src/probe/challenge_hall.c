#include "home/challenge_hall.h"
#include "probe.h"

static void adapt_Func_f5db(ProbeState *s)
{
	ChallengeHallClearResult out = Func_f5db();
	s->a = out.a;
	s->f = out.f;
}

static void adapt_Func_f5e9(ProbeState *s)
{
	ChallengeHallBitResult out = Func_f5e9(s->c);
	s->b = out.b;
	s->hl = out.hl;
}

static void adapt_Script_Host(ProbeState *s)
{
	(void)s;
	Script_Host();
}

/* >>> factory Func_f5cc */
static void adapt_Func_f5cc(ProbeState *s)
{
	ChallengeHallTestBitResult out = Func_f5cc(s->c);
	s->a = out.a;
	s->f = out.f;
}
/* <<< factory Func_f5cc */

/* >>> factory Func_f5d4 */
static void adapt_Func_f5d4(ProbeState *s)
{
	ChallengeHallSetBitResult out = Func_f5d4(s->c);
	s->a = out.a;
	s->f = out.f;
}
/* <<< factory Func_f5d4 */

/* >>> factory ChallengeHallAfterDuel */
static void adapt_ChallengeHallAfterDuel(ProbeState *s)
{
	ChallengeHallAfterDuelResult r = ChallengeHallAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ChallengeHallAfterDuel */

/* >>> factory ChallengeHallLoadMap */
static void adapt_ChallengeHallLoadMap(ProbeState *s)
{
	ChallengeHallLoadMapResult r = ChallengeHallLoadMap(s->b, s->c, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->hl = r.hl;
}
/* <<< factory ChallengeHallLoadMap */

/* >>> factory Preload_Guide */
static void adapt_Preload_Guide(ProbeState *s)
{
	PreloadGuideResult r = Preload_Guide();
	s->a = r.a; s->f = r.f;
}
/* <<< factory Preload_Guide */

/* >>> factory Preload_ChallengeHallOpponent */
static void adapt_Preload_ChallengeHallOpponent(ProbeState *s)
{
	PreloadChallengeHallOpponentResult r = Preload_ChallengeHallOpponent();
	s->a = r.a; s->f = r.f;
}
/* <<< factory Preload_ChallengeHallOpponent */

const ProbeEntry probe_entries_challenge_hall[] = {
	{ "Func_f5db", adapt_Func_f5db },
	{ "Func_f5e9", adapt_Func_f5e9 },
	{ "Script_Host", adapt_Script_Host },
	{ "Func_f5cc", adapt_Func_f5cc },
	{ "Func_f5d4", adapt_Func_f5d4 },
	{ "ChallengeHallAfterDuel", adapt_ChallengeHallAfterDuel },
	{ "ChallengeHallLoadMap", adapt_ChallengeHallLoadMap },
	{ "Preload_Guide", adapt_Preload_Guide },
	{ "Preload_ChallengeHallOpponent", adapt_Preload_ChallengeHallOpponent },
	{ NULL, NULL },
};
