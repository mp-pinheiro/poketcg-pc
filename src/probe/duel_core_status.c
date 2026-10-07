/* >>> part includes */
#include "home/duel_core_status.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory IsArenaPokemonAsleepOrPoisoned */
static void adapt_IsArenaPokemonAsleepOrPoisoned(ProbeState *s)
{
	DuelCoreStatusResult r = IsArenaPokemonAsleepOrPoisoned();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory IsArenaPokemonAsleepOrPoisoned */

/* >>> factory DiscardAttachedPlusPowers */
static void adapt_DiscardAttachedPlusPowers(ProbeState *s)
{
	DuelCoreStatusDiscardResult r = DiscardAttachedPlusPowers();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory DiscardAttachedPlusPowers */

/* >>> factory DiscardAttachedDefenders */
static void adapt_DiscardAttachedDefenders(ProbeState *s)
{
	DuelCoreStatusDiscardResult r = DiscardAttachedDefenders();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory DiscardAttachedDefenders */

/* >>> part probe_entries_duel_core_status */
const ProbeEntry probe_entries_duel_core_status[] = {
	{ "IsArenaPokemonAsleepOrPoisoned", adapt_IsArenaPokemonAsleepOrPoisoned },
	{ "DiscardAttachedPlusPowers", adapt_DiscardAttachedPlusPowers },
	{ "DiscardAttachedDefenders", adapt_DiscardAttachedDefenders },
	{ NULL, NULL },
};
/* <<< part probe_entries_duel_core_status */
