#ifndef POKETCG_HOME_CARD_COLOR_H
#define POKETCG_HOME_CARD_COLOR_H

#include <stdint.h>

/* poketcg/src/home/card_color.asm */

uint8_t GetCardWeakness(uint8_t a);
uint8_t GetArenaCardWeakness(void);
uint8_t GetPlayAreaCardWeakness(uint8_t a);
uint8_t GetCardResistance(uint8_t a);
uint8_t GetArenaCardResistance(void);
uint8_t GetPlayAreaCardResistance(uint8_t a);
uint8_t GetArenaCardColor(void);

#endif /* POKETCG_HOME_CARD_COLOR_H */
