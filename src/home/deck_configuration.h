#ifndef POKETCG_HOME_DECK_CONFIGURATION_H
#define POKETCG_HOME_DECK_CONFIGURATION_H

#include <stdint.h>

/* >>> factory DecrementDeckCardsInCollection */
uint16_t DecrementDeckCardsInCollection(uint16_t hl);
/* <<< factory DecrementDeckCardsInCollection */
/* >>> factory AddDeckToCollection */
uint16_t AddDeckToCollection(uint16_t hl);
/* <<< factory AddDeckToCollection */
/* >>> factory CopyListFromHLToDE */
void CopyListFromHLToDE(uint16_t *hl, uint16_t *de);
/* <<< factory CopyListFromHLToDE */
/* >>> factory CalculateOnesAndTensDigits */
void CalculateOnesAndTensDigits(uint8_t a);
/* <<< factory CalculateOnesAndTensDigits */
/* >>> factory InitCardSelectionParams */
uint8_t InitCardSelectionParams(uint8_t a, uint16_t *hl);
/* <<< factory InitCardSelectionParams */
/* >>> factory ClearMemory_Bank2 */
void ClearMemory_Bank2(uint8_t a, uint16_t hl);
/* <<< factory ClearMemory_Bank2 */
/* >>> factory CheckIfHasOtherValidDecks */
uint8_t CheckIfHasOtherValidDecks(void);
/* <<< factory CheckIfHasOtherValidDecks */
/* >>> factory FillDEWithA */
void FillDEWithA(uint8_t a, uint8_t b, uint16_t de);
/* <<< factory FillDEWithA */
/* >>> factory DrawHandCardsTileAtDE */
void DrawHandCardsTileAtDE(uint16_t de);
/* <<< factory DrawHandCardsTileAtDE */
/* >>> factory CountNumberOfCardsOfType */
uint8_t CountNumberOfCardsOfType(uint8_t a);
/* <<< factory CountNumberOfCardsOfType */
#endif /* POKETCG_HOME_DECK_CONFIGURATION_H */
