#ifndef POKETCG_HOME_BOOSTER_PACKS_H
#define POKETCG_HOME_BOOSTER_PACKS_H

#include <stdint.h>

/* >>> factory GetCurrentRarityAmount */
typedef struct { uint8_t a; uint16_t hl; } RarityAmount;
RarityAmount GetCurrentRarityAmount(void);
/* <<< factory GetCurrentRarityAmount */
/* >>> factory GetBoosterCardType */
uint8_t GetBoosterCardType(uint8_t a);
/* <<< factory GetBoosterCardType */
/* >>> factory CalculateTypeChances */
uint8_t CalculateTypeChances(void);
/* <<< factory CalculateTypeChances */
#endif /* POKETCG_HOME_BOOSTER_PACKS_H */
