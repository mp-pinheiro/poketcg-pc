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

/* >>> factory TossCoin */
static void adapt_TossCoin(ProbeState *s)
{
	TossCoinRoutineResult result = TossCoin((uint16_t)(((uint16_t)s->d << 8u) | s->e), s->hl);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory TossCoin */

const ProbeEntry probe_entries_coin_toss[] = {
	{ "CompareDEtoBC", adapt_CompareDEtoBC },
	{ "TossCoinATimes", adapt_TossCoinATimes },
	{ "TossCoin", adapt_TossCoin },
	{ NULL, NULL },
};
