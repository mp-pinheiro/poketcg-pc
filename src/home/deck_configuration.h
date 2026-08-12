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
#endif /* POKETCG_HOME_DECK_CONFIGURATION_H */
