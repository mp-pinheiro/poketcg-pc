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
LookForCardIDInLocationBank8Result LookForCardIDInLocation_Bank8(uint8_t location, uint8_t card_id_byte);
/* <<< factory LookForCardIDInLocation_Bank8 */
/* >>> factory LookForCardIDInHandList_Bank8 */
typedef struct { uint8_t a; uint8_t f; } LookForCardIDInHandListResult;
LookForCardIDInHandListResult LookForCardIDInHandList_Bank8(uint8_t a);
/* <<< factory LookForCardIDInHandList_Bank8 */
/* >>> factory LookForCardIDInHandAndPlayArea */
typedef struct { uint8_t a; uint8_t f; } LookForCardIDInHandAndPlayAreaResult;
LookForCardIDInHandAndPlayAreaResult LookForCardIDInHandAndPlayArea(uint8_t a);
/* <<< factory LookForCardIDInHandAndPlayArea */
/* >>> factory LookForCardIDToTradeWithDifferentHandCard */
typedef struct { uint8_t a; uint8_t f; uint8_t e; } LookForCardIDToTradeWithDifferentHandCardResult;
LookForCardIDToTradeWithDifferentHandCardResult LookForCardIDToTradeWithDifferentHandCard(uint8_t a, uint8_t e);
/* <<< factory LookForCardIDToTradeWithDifferentHandCard */
/* >>> factory LookForCardIDInDeck_GivenCardIDInHand */
typedef struct { uint8_t a; uint8_t f; } LookForCardIDInDeck_GivenCardIDInHandResult;
LookForCardIDInDeck_GivenCardIDInHandResult LookForCardIDInDeck_GivenCardIDInHand(uint8_t a, uint8_t b);
/* <<< factory LookForCardIDInDeck_GivenCardIDInHand */
/* >>> factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */
typedef struct { uint8_t a; uint8_t f; } LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult;
LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(uint8_t a, uint8_t b);
/* <<< factory LookForCardIDInDeck_GivenCardIDInHandAndPlayArea */
/* >>> factory AddStarterDeck */
void AddStarterDeck(uint8_t a);
/* <<< factory AddStarterDeck */
/* >>> factory FindDuplicatePokemonCards */
typedef struct { uint8_t a; uint8_t f; } FindDuplicatePokemonCardsResult;
FindDuplicatePokemonCardsResult FindDuplicatePokemonCards(void);
/* <<< factory FindDuplicatePokemonCards */
/* >>> factory AIPickEnergyCardToDiscard */
uint8_t AIPickEnergyCardToDiscard(uint8_t a);
/* <<< factory AIPickEnergyCardToDiscard */
/* >>> factory HandleAIAntiMewtwoDeckStrategy */
typedef struct { uint8_t a; uint8_t f; } HandleAIAntiMewtwoDeckStrategyResult;
HandleAIAntiMewtwoDeckStrategyResult HandleAIAntiMewtwoDeckStrategy(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory HandleAIAntiMewtwoDeckStrategy */
/* >>> factory OpenBoosterPack */
void OpenBoosterPack(void);
/* <<< factory OpenBoosterPack */
/* >>> factory PreparePrinterConnection */
/* PreparePrinterConnection returns the farcalled callee's carry alone. It is
 * a bare uint8_t instead of a result struct because src/home/common.c also
 * includes home/printer.h, which already owns the name
 * PreparePrinterConnectionResult; a second anonymous-struct typedef under that
 * name would be a redefinition. */
uint8_t PreparePrinterConnection(uint16_t hl);
/* <<< factory PreparePrinterConnection */
/* >>> factory AICheckIfAttackIsHighRecoil */
typedef struct { uint8_t f; } AICheckIfAttackIsHighRecoilResult;
AICheckIfAttackIsHighRecoilResult AICheckIfAttackIsHighRecoil(void);
/* <<< factory AICheckIfAttackIsHighRecoil */
/* >>> factory PrintDeckConfiguration */
void PrintDeckConfiguration(uint8_t a);
/* <<< factory PrintDeckConfiguration */
/* >>> factory ShowPromotionalCardScreen */
void ShowPromotionalCardScreen(uint8_t a);
/* <<< factory ShowPromotionalCardScreen */
/* >>> factory RequestToPrintCard */
/* RequestToPrintCard returns the farcalled callee's carry alone. It is a bare
 * uint8_t instead of a result struct because src/home/common.c also includes
 * home/printer.h, which already owns the name RequestToPrintCardResult; a
 * second anonymous-struct typedef under that name would be a redefinition. */
uint8_t RequestToPrintCard(uint8_t a);
/* <<< factory RequestToPrintCard */
/* >>> factory PrintCardList */
/* PrintCardList returns the farcalled callee's carry alone. It is a bare
 * uint8_t instead of a result struct because src/home/common.c also includes
 * home/printer.h, which already owns the name PrintCardListResult; a second
 * anonymous-struct typedef under that name would be a redefinition. */
uint8_t PrintCardList(void);
/* <<< factory PrintCardList */
/* >>> factory ReceiveCard */
typedef struct { uint8_t a; uint8_t f; } ReceiveCardResult;
ReceiveCardResult ReceiveCard(void);
/* <<< factory ReceiveCard */
/* >>> factory ReceiveDeckConfiguration */
typedef struct { uint8_t a; uint8_t f; } ReceiveDeckConfigurationResult;
ReceiveDeckConfigurationResult ReceiveDeckConfiguration(void);
/* <<< factory ReceiveDeckConfiguration */
/* >>> factory DoCardPop */
void DoCardPop(void);
/* <<< factory DoCardPop */
/* >>> factory SendCard */
void SendCard(void);
/* <<< factory SendCard */
/* >>> factory SendDeckConfiguration */
void SendDeckConfiguration(void);
/* <<< factory SendDeckConfiguration */
#endif /* POKETCG_HOME_COMMON_H */
