#ifndef POKETCG_HOME_DAMAGE_CALCULATION_H
#define POKETCG_HOME_DAMAGE_CALCULATION_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part DamageCalculationResult */
typedef struct {
    uint8_t a;
    uint8_t f;
    uint8_t d;
    uint8_t e;
    uint16_t hl;
} DamageCalculationResult;
/* <<< part DamageCalculationResult */

/* >>> factory CalculateDamage_VersusDefendingPokemon */
DamageCalculationResult CalculateDamage_VersusDefendingPokemon(void);
/* <<< factory CalculateDamage_VersusDefendingPokemon */
/* >>> factory CalculateDamage_FromDefendingPokemon */
DamageCalculationResult CalculateDamage_FromDefendingPokemon(void);
/* <<< factory CalculateDamage_FromDefendingPokemon */

/* >>> factory EstimateDamage_VersusDefendingCard */
DamageCalculationResult EstimateDamage_VersusDefendingCard(uint8_t a);
/* <<< factory EstimateDamage_VersusDefendingCard */
/* >>> factory EstimateDamage_FromDefendingPokemon */
DamageCalculationResult EstimateDamage_FromDefendingPokemon(uint8_t a);
/* <<< factory EstimateDamage_FromDefendingPokemon */

#endif
