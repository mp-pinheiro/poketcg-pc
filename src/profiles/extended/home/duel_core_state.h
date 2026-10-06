#ifndef POKETCG_HOME_DUEL_CORE_STATE_H
#define POKETCG_HOME_DUEL_CORE_STATE_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
	uint8_t f;
} DuelCoreStateResult;

typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
	uint8_t f;
} DuelCoreStateWideResult;

DuelCoreStateResult InitVariablesToBeginTurn(void);
DuelCoreStateResult SetAllPlayAreaPokemonCanEvolve(void);
DuelCoreStateWideResult InitializeDuelVariables(void);
DuelCoreStateWideResult InitTurnDuelistPrizes(void);
DuelCoreStateResult TakeAPrizes(uint8_t a);
DuelCoreStateResult CheckIfTurnDuelistPlayAreaPokemonAreAllKnockedOut(void);
DuelCoreStateWideResult CountKnockedOutPokemon(void);

#endif
