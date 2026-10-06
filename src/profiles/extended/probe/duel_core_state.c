#include "home/duel_core_state.h"
#include "probe.h"

static void adapt_InitVariablesToBeginTurn(ProbeState *s)
{
	DuelCoreStateResult r = InitVariablesToBeginTurn();
	s->a = r.a;
}

static void adapt_SetAllPlayAreaPokemonCanEvolve(ProbeState *s)
{
	DuelCoreStateResult r = SetAllPlayAreaPokemonCanEvolve();
	s->a = r.a;
	s->c = r.c;
	s->hl = r.hl;
}

static void adapt_InitializeDuelVariables(ProbeState *s)
{
	DuelCoreStateWideResult r = InitializeDuelVariables();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}

static void adapt_InitTurnDuelistPrizes(ProbeState *s)
{
	DuelCoreStateWideResult r = InitTurnDuelistPrizes();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_TakeAPrizes(ProbeState *s)
{
	DuelCoreStateResult r = TakeAPrizes(s->a);
	if (s->a == 0)
		return;
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}

static void adapt_CheckIfTurnDuelistPlayAreaPokemonAreAllKnockedOut(ProbeState *s)
{
	DuelCoreStateResult r = CheckIfTurnDuelistPlayAreaPokemonAreAllKnockedOut();
	s->a = r.a;
	s->c = r.c;
	s->hl = r.hl;
}

static void adapt_CountKnockedOutPokemon(ProbeState *s)
{
	DuelCoreStateWideResult r = CountKnockedOutPokemon();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

const ProbeEntry probe_entries_duel_core_state[] = {
	{"InitVariablesToBeginTurn", adapt_InitVariablesToBeginTurn},
	{"SetAllPlayAreaPokemonCanEvolve", adapt_SetAllPlayAreaPokemonCanEvolve},
	{"InitializeDuelVariables", adapt_InitializeDuelVariables},
	{"InitTurnDuelistPrizes", adapt_InitTurnDuelistPrizes},
	{"TakeAPrizes", adapt_TakeAPrizes},
	{"CheckIfTurnDuelistPlayAreaPokemonAreAllKnockedOut", adapt_CheckIfTurnDuelistPlayAreaPokemonAreAllKnockedOut},
	{"CountKnockedOutPokemon", adapt_CountKnockedOutPokemon},
	{NULL, NULL},
};
