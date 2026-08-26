#ifndef POKETCG_HOME_DAMAGE_CALCULATION_H
#define POKETCG_HOME_DAMAGE_CALCULATION_H

#include <stdint.h>

typedef struct {
    uint8_t a;
    uint8_t f;
    uint8_t d;
    uint8_t e;
    uint16_t hl;
} DamageCalculationResult;

DamageCalculationResult CalculateDamage_VersusDefendingPokemon(void);
DamageCalculationResult CalculateDamage_FromDefendingPokemon(void);

/* >>> factory EstimateDamage_VersusDefendingCard */
DamageCalculationResult EstimateDamage_VersusDefendingCard(uint8_t a);
/* <<< factory EstimateDamage_VersusDefendingCard */

#endif
