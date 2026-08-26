#include "home/coin_toss.h"
#include "probe.h"

static void adapt_CompareDEtoBC(ProbeState *s)
{
	s->f = CompareDEtoBC(s->d, s->e, s->b, s->c);
}

/* >>> factory TossCoinATimes */
static void adapt_TossCoinATimes(ProbeState *s)
{
	TossCoinATimesResult result = TossCoinATimes(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory TossCoinATimes */

const ProbeEntry probe_entries_coin_toss[] = {
	{ "CompareDEtoBC", adapt_CompareDEtoBC },
	{ "TossCoinATimes", adapt_TossCoinATimes },
	{ NULL, NULL },
};
