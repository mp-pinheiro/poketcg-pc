#ifndef POKETCG_HOME_DAMAGE_H
#define POKETCG_HOME_DAMAGE_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory AddToDamage */
/* poketcg/src/home/damage.asm */

void AddToDamage(uint8_t a);
/* <<< factory AddToDamage */
/* >>> factory SubtractFromDamage */
void SubtractFromDamage(uint8_t a);
/* <<< factory SubtractFromDamage */

#endif /* POKETCG_HOME_DAMAGE_H */
