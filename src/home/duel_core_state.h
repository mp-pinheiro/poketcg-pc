#ifndef POKETCG_HOME_DUEL_CORE_STATE_H
#define POKETCG_HOME_DUEL_CORE_STATE_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part DuelCoreStateResult */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
	uint8_t f;
} DuelCoreStateResult;
/* <<< part DuelCoreStateResult */

/* >>> part DuelCoreStateWideResult */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
	uint8_t f;
} DuelCoreStateWideResult;
/* <<< part DuelCoreStateWideResult */

/* >>> factory InitVariablesToBeginTurn */
DuelCoreStateResult InitVariablesToBeginTurn(void);
/* <<< factory InitVariablesToBeginTurn */
/* >>> factory SetAllPlayAreaPokemonCanEvolve */
DuelCoreStateResult SetAllPlayAreaPokemonCanEvolve(void);
/* <<< factory SetAllPlayAreaPokemonCanEvolve */
/* >>> factory InitializeDuelVariables */
DuelCoreStateWideResult InitializeDuelVariables(void);
/* <<< factory InitializeDuelVariables */
/* >>> factory InitTurnDuelistPrizes */
DuelCoreStateWideResult InitTurnDuelistPrizes(void);
/* <<< factory InitTurnDuelistPrizes */
/* >>> factory TakeAPrizes */
DuelCoreStateResult TakeAPrizes(uint8_t a);
/* <<< factory TakeAPrizes */
/* >>> factory CheckIfTurnDuelistPlayAreaPokemonAreAllKnockedOut */
DuelCoreStateResult CheckIfTurnDuelistPlayAreaPokemonAreAllKnockedOut(void);
/* <<< factory CheckIfTurnDuelistPlayAreaPokemonAreAllKnockedOut */
/* >>> factory CountKnockedOutPokemon */
DuelCoreStateWideResult CountKnockedOutPokemon(void);
/* <<< factory CountKnockedOutPokemon */

#endif
