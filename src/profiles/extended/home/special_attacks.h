#ifndef POKETCG_HOME_SPECIAL_ATTACKS_H
#define POKETCG_HOME_SPECIAL_ATTACKS_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part BasicPokemonDeckResult */
typedef struct {
	uint8_t a;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} BasicPokemonDeckResult;
/* <<< part BasicPokemonDeckResult */

/* >>> factory CheckIfAnyBasicPokemonInDeck */
BasicPokemonDeckResult CheckIfAnyBasicPokemonInDeck(void);
/* <<< factory CheckIfAnyBasicPokemonInDeck */

/* >>> factory CheckWhetherToSwitchToFirstAttack */
void CheckWhetherToSwitchToFirstAttack(void);
/* <<< factory CheckWhetherToSwitchToFirstAttack */
/* >>> factory HandleSpecialAIAttacks */
typedef struct { uint8_t a; uint8_t f; } HandleSpecialAIAttacksResult;
HandleSpecialAIAttacksResult HandleSpecialAIAttacks(void);
/* <<< factory HandleSpecialAIAttacks */
#endif
