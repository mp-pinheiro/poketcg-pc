#ifndef POKETCG_HOME_COMMON_H
#define POKETCG_HOME_COMMON_H

#include <stdint.h>
#include "home/card_id.h"

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
/* f is the exit F register: the `cp` that chose the exit, which a caller
 * that pushes af around its own work (AIDecide_SuperEnergyRemoval) keeps. */
typedef struct { uint8_t a; uint8_t b; uint8_t b_valid; uint8_t f; uint8_t d; } PickTwoResult;
PickTwoResult PickTwoAttachedEnergyCards(uint8_t a);
/* <<< factory PickTwoAttachedEnergyCards */
/* >>> factory ClearMemory_Bank8 */
void ClearMemory_Bank8(uint8_t a, uint16_t hl);
/* <<< factory ClearMemory_Bank8 */
/* >>> factory PickAttachedEnergyCardToRemove */
/* d is the energy list's page while it stays empty, else GetCardIDFromDeckIndex's 0. */
typedef struct { uint8_t a; uint8_t d; } PickEnergyResult;
PickEnergyResult PickAttachedEnergyCardToRemove(uint8_t a);
/* <<< factory PickAttachedEnergyCardToRemove */
/* >>> factory CopyListWithFFTerminatorFromHLToDE_Bank8 */
typedef struct { uint8_t a; uint8_t f; } CopyListBank8Result;
CopyListBank8Result CopyListWithFFTerminatorFromHLToDE_Bank8(uint16_t *hl, uint16_t *de);
/* <<< factory CopyListWithFFTerminatorFromHLToDE_Bank8 */
/* >>> factory LookForCardIDInPlayArea_Bank8 */
typedef struct { uint8_t a; uint8_t b; uint8_t f; } LookForCardIDInPlayAreaResult;
LookForCardIDInPlayAreaResult LookForCardIDInPlayArea_Bank8(CardId de, uint8_t b);
/* <<< factory LookForCardIDInPlayArea_Bank8 */
/* >>> factory CheckIfHasCardIDInHand */
typedef struct { uint8_t a; uint8_t f; } CheckIfHasCardIDInHandResult;
CheckIfHasCardIDInHandResult CheckIfHasCardIDInHand(CardId de);
/* <<< factory CheckIfHasCardIDInHand */
/* >>> factory FindBasicEnergyCardsInLocation */
typedef struct { uint8_t a; uint8_t f; uint8_t d; uint8_t e; uint16_t hl; } FindBasicEnergyCardsInLocationResult;
FindBasicEnergyCardsInLocationResult FindBasicEnergyCardsInLocation(uint8_t a);
/* <<< factory FindBasicEnergyCardsInLocation */
/* >>> factory CalculateBDividedByA_Bank8 */
typedef struct { uint8_t a; uint8_t f; } CalculateBDividedByA_Bank8Result;
CalculateBDividedByA_Bank8Result CalculateBDividedByA_Bank8(uint8_t a, uint8_t b);
/* <<< factory CalculateBDividedByA_Bank8 */
/* >>> factory CheckIfPlayerHasPokemonOtherThanMewtwoLv53 */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} CheckIfPlayerHasPokemonOtherThanMewtwoLv53Result;
CheckIfPlayerHasPokemonOtherThanMewtwoLv53Result CheckIfPlayerHasPokemonOtherThanMewtwoLv53(uint8_t b, uint8_t c, uint8_t d, uint16_t hl);
/* <<< factory CheckIfPlayerHasPokemonOtherThanMewtwoLv53 */
/* >>> factory RemoveFromListDifferentCardOfGivenType */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } RemoveFromListDifferentCardOfGivenTypeResult;
RemoveFromListDifferentCardOfGivenTypeResult RemoveFromListDifferentCardOfGivenType(
	uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory RemoveFromListDifferentCardOfGivenType */
/* >>> factory CountPokemonCardsInHandAndInPlayArea */
uint8_t CountPokemonCardsInHandAndInPlayArea(uint8_t c);
/* <<< factory CountPokemonCardsInHandAndInPlayArea */
/* >>> factory LookForCardIDInLocation_Bank8 */
typedef struct { uint8_t a; uint8_t f; } LookForCardIDInLocationBank8Result;
LookForCardIDInLocationBank8Result LookForCardIDInLocation_Bank8(uint8_t location, CardId de);
/* <<< factory LookForCardIDInLocation_Bank8 */
/* >>> factory LookForCardIDInHandList_Bank8 */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } LookForCardIDInHandListResult;
LookForCardIDInHandListResult LookForCardIDInHandList_Bank8(CardId de);
/* <<< factory LookForCardIDInHandList_Bank8 */
/* >>> factory LookForCardIDInHandAndPlayArea */
typedef struct { uint8_t a; uint8_t f; } LookForCardIDInHandAndPlayAreaResult;
LookForCardIDInHandAndPlayAreaResult LookForCardIDInHandAndPlayArea(CardId de);
/* <<< factory LookForCardIDInHandAndPlayArea */
/* >>> factory LookForCardIDToTradeWithDifferentHandCard */
typedef struct { uint8_t a; uint8_t f; uint8_t e; uint8_t d; } LookForCardIDToTradeWithDifferentHandCardResult;
LookForCardIDToTradeWithDifferentHandCardResult LookForCardIDToTradeWithDifferentHandCard(CardId de, CardId bc);
/* <<< factory LookForCardIDToTradeWithDifferentHandCard */
/* >>> factory LookForCardIDInDeck_GivenCardIDInHand */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } LookForCardIDInDeck_GivenCardIDInHandResult;
LookForCardIDInDeck_GivenCardIDInHandResult LookForCardIDInDeck_GivenCardIDInHand(CardId de, CardId bc);
/* <<< factory LookForCardIDInDeck_GivenCardIDInHand */
/* >>> factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult;
LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(CardId de, CardId bc);
/* <<< factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */
/* >>> factory AddStarterDeck */
void AddStarterDeck(uint8_t a);
/* <<< factory AddStarterDeck */
/* >>> factory FindDuplicatePokemonCards */
typedef struct { uint8_t a; uint8_t f; uint8_t d; } FindDuplicatePokemonCardsResult;
FindDuplicatePokemonCardsResult FindDuplicatePokemonCards(void);
/* <<< factory FindDuplicatePokemonCards */
/* >>> factory AIPickEnergyCardToDiscard */
PickEnergyResult AIPickEnergyCardToDiscard(uint8_t a);
/* <<< factory AIPickEnergyCardToDiscard */
/* >>> factory HandleAIAntiMewtwoDeckStrategy */
typedef struct { uint8_t a; uint8_t f; } HandleAIAntiMewtwoDeckStrategyResult;
HandleAIAntiMewtwoDeckStrategyResult HandleAIAntiMewtwoDeckStrategy(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory HandleAIAntiMewtwoDeckStrategy */
/* >>> factory OpenBoosterPack */
void OpenBoosterPack(void);
/* <<< factory OpenBoosterPack */
/* >>> factory AICheckIfAttackIsHighRecoil */
typedef struct { uint8_t f; uint8_t d; } AICheckIfAttackIsHighRecoilResult;
AICheckIfAttackIsHighRecoilResult AICheckIfAttackIsHighRecoil(void);
/* <<< factory AICheckIfAttackIsHighRecoil */
/* >>> factory ShowPromotionalCardScreen */
void ShowPromotionalCardScreen(CardId de);
/* <<< factory ShowPromotionalCardScreen */
#endif /* POKETCG_HOME_COMMON_H */
