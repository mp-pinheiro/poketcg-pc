#ifndef POKETCG_HOME_SPECIAL_ATTACKS_H
#define POKETCG_HOME_SPECIAL_ATTACKS_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} BasicPokemonDeckResult;

BasicPokemonDeckResult CheckIfAnyBasicPokemonInDeck(void);

/* >>> factory CheckWhetherToSwitchToFirstAttack */
void CheckWhetherToSwitchToFirstAttack(void);
/* <<< factory CheckWhetherToSwitchToFirstAttack */
/* >>> factory HandleSpecialAIAttacks */
typedef struct { uint8_t a; uint8_t f; } HandleSpecialAIAttacksResult;
HandleSpecialAIAttacksResult HandleSpecialAIAttacks(void);
/* <<< factory HandleSpecialAIAttacks */
#endif
