#include "home/coin_toss.h"
#include "probe.h"

static void adapt_CompareDEtoBC(ProbeState *s)
{
	s->f = CompareDEtoBC(s->d, s->e, s->b, s->c);
}

const ProbeEntry probe_entries_coin_toss[] = {
	{ "CompareDEtoBC", adapt_CompareDEtoBC },
	{ NULL, NULL },
};
