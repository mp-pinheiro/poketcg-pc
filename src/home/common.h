#ifndef POKETCG_HOME_COMMON_H
#define POKETCG_HOME_COMMON_H

#include <stdint.h>

/* >>> factory CountOppEnergyCardsInHand */
typedef struct { uint8_t a; uint8_t f; uint8_t b; } CountOppEnergyResult;
CountOppEnergyResult CountOppEnergyCardsInHand(uint8_t a, uint8_t b);
/* <<< factory CountOppEnergyCardsInHand */
/* >>> factory ConvertHPToDamageCounters_Bank8 */
uint8_t ConvertHPToDamageCounters_Bank8(uint8_t a);
/* <<< factory ConvertHPToDamageCounters_Bank8 */
/* >>> factory CalculateWordTensDigit */
uint16_t CalculateWordTensDigit(uint16_t hl);
/* <<< factory CalculateWordTensDigit */
#endif /* POKETCG_HOME_COMMON_H */
