#include "home/duel.h"
#include "probe.h"

static uint16_t pair(uint8_t hi, uint8_t lo)
{
	return (uint16_t)((uint16_t)hi << 8 | lo);
}

static void adapt_CopyPlayerName(ProbeState *s)
{
	CopyTextResult r = CopyPlayerName(pair(s->d, s->e));
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_CopyOpponentName(ProbeState *s)
{
	CopyTextResult r = CopyOpponentName(pair(s->d, s->e));
	s->a = r.a;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

const ProbeEntry probe_entries_duel[] = {
	{ "CopyPlayerName", adapt_CopyPlayerName },
	{ "CopyOpponentName", adapt_CopyOpponentName },
	{ NULL, NULL },
};
