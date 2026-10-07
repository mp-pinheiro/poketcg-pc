#ifndef POKETCG_HOME_CARD_COLOR_H
#define POKETCG_HOME_CARD_COLOR_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory GetCardWeakness */
/* poketcg/src/home/card_color.asm */

uint8_t GetCardWeakness(uint8_t a);
/* <<< factory GetCardWeakness */
/* >>> factory GetArenaCardWeakness */
uint8_t GetArenaCardWeakness(void);
/* <<< factory GetArenaCardWeakness */
/* >>> factory GetPlayAreaCardWeakness */
uint8_t GetPlayAreaCardWeakness(uint8_t a);
/* <<< factory GetPlayAreaCardWeakness */
/* >>> factory GetCardResistance */
uint8_t GetCardResistance(uint8_t a);
/* <<< factory GetCardResistance */
/* >>> factory GetArenaCardResistance */
uint8_t GetArenaCardResistance(void);
/* <<< factory GetArenaCardResistance */
/* >>> factory GetPlayAreaCardResistance */
uint8_t GetPlayAreaCardResistance(uint8_t a);
/* <<< factory GetPlayAreaCardResistance */
/* >>> factory GetArenaCardColor */
uint8_t GetArenaCardColor(void);
/* <<< factory GetArenaCardColor */
/* >>> factory GetPlayAreaCardColor */
uint8_t GetPlayAreaCardColor(uint8_t a);
/* <<< factory GetPlayAreaCardColor */
/* >>> factory HandleEnergyBurn */
void HandleEnergyBurn(void);
/* <<< factory HandleEnergyBurn */

#endif /* POKETCG_HOME_CARD_COLOR_H */
