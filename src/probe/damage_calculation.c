#include "home/damage_calculation.h"
#include "probe.h"

static void adapt_CalculateDamage_VersusDefendingPokemon(ProbeState *s)
{
    DamageCalculationResult r = CalculateDamage_VersusDefendingPokemon();
    s->a = r.a;
    s->f = r.f;
    s->d = r.d;
    s->e = r.e;
    s->hl = r.hl;
}

/* >>> factory EstimateDamage_VersusDefendingCard */
static void adapt_EstimateDamage_VersusDefendingCard(ProbeState *s)
{
    DamageCalculationResult r = EstimateDamage_VersusDefendingCard(s->a);
    s->a = r.a;
    s->f = r.f;
    s->d = r.d;
    s->e = r.e;
    s->hl = r.hl;
}
/* <<< factory EstimateDamage_VersusDefendingCard */

/* >>> factory EstimateDamage_FromDefendingPokemon */
static void adapt_EstimateDamage_FromDefendingPokemon(ProbeState *s)
{
    DamageCalculationResult r = EstimateDamage_FromDefendingPokemon(s->a);
    s->a = r.a;
    s->f = r.f;
    s->d = r.d;
    s->e = r.e;
    s->hl = r.hl;
}
/* <<< factory EstimateDamage_FromDefendingPokemon */

static void adapt_CalculateDamage_FromDefendingPokemon(ProbeState *s)
{
    DamageCalculationResult r = CalculateDamage_FromDefendingPokemon();
    s->a = r.a;
    s->f = r.f;
    s->d = r.d;
    s->e = r.e;
    s->hl = r.hl;
}

const ProbeEntry probe_entries_damage_calculation[] = {
    {"CalculateDamage_VersusDefendingPokemon", adapt_CalculateDamage_VersusDefendingPokemon},
    {"EstimateDamage_VersusDefendingCard", adapt_EstimateDamage_VersusDefendingCard},
    {"EstimateDamage_FromDefendingPokemon", adapt_EstimateDamage_FromDefendingPokemon},
    {"CalculateDamage_FromDefendingPokemon", adapt_CalculateDamage_FromDefendingPokemon},
    {NULL, NULL},
};
