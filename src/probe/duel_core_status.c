#include "home/duel_core_status.h"
#include "probe.h"

static void adapt_IsArenaPokemonAsleepOrPoisoned(ProbeState *s)
{
	DuelCoreStatusResult r = IsArenaPokemonAsleepOrPoisoned();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_DiscardAttachedPlusPowers(ProbeState *s)
{
	DuelCoreStatusDiscardResult r = DiscardAttachedPlusPowers();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
}

static void adapt_DiscardAttachedDefenders(ProbeState *s)
{
	DuelCoreStatusDiscardResult r = DiscardAttachedDefenders();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
}

const ProbeEntry probe_entries_duel_core_status[] = {
	{ "IsArenaPokemonAsleepOrPoisoned", adapt_IsArenaPokemonAsleepOrPoisoned },
	{ "DiscardAttachedPlusPowers", adapt_DiscardAttachedPlusPowers },
	{ "DiscardAttachedDefenders", adapt_DiscardAttachedDefenders },
	{ NULL, NULL },
};
