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
/* >>> factory PickTwoAttachedEnergyCards */
typedef struct { uint8_t a; uint8_t b; uint8_t b_valid; } PickTwoResult;
PickTwoResult PickTwoAttachedEnergyCards(uint8_t a);
/* <<< factory PickTwoAttachedEnergyCards */
/* >>> factory ClearMemory_Bank8 */
void ClearMemory_Bank8(uint8_t a, uint16_t hl);
/* <<< factory ClearMemory_Bank8 */
/* >>> factory PickAttachedEnergyCardToRemove */
uint8_t PickAttachedEnergyCardToRemove(uint8_t a);
/* <<< factory PickAttachedEnergyCardToRemove */
/* >>> factory CopyListWithFFTerminatorFromHLToDE_Bank8 */
typedef struct { uint8_t a; uint8_t f; } CopyListBank8Result;
CopyListBank8Result CopyListWithFFTerminatorFromHLToDE_Bank8(uint16_t *hl, uint16_t *de);
/* <<< factory CopyListWithFFTerminatorFromHLToDE_Bank8 */
/* >>> factory LookForCardIDInPlayArea_Bank8 */
typedef struct { uint8_t a; uint8_t b; uint8_t f; } LookForCardIDInPlayAreaResult;
LookForCardIDInPlayAreaResult LookForCardIDInPlayArea_Bank8(uint8_t a, uint8_t b);
/* <<< factory LookForCardIDInPlayArea_Bank8 */
/* >>> factory CheckIfHasCardIDInHand */
typedef struct { uint8_t a; uint8_t f; } CheckIfHasCardIDInHandResult;
CheckIfHasCardIDInHandResult CheckIfHasCardIDInHand(uint8_t a);
/* <<< factory CheckIfHasCardIDInHand */
#endif /* POKETCG_HOME_COMMON_H */
