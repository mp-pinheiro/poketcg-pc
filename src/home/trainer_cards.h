#ifndef POKETCG_HOME_TRAINER_CARDS_H
#define POKETCG_HOME_TRAINER_CARDS_H

#include <stdint.h>

/* >>> factory RemoveCardFromList */
void RemoveCardFromList(uint16_t *hl);
/* <<< factory RemoveCardFromList */
/* >>> factory FindDuplicateCards */
typedef struct { uint8_t a, f; } FindDupResult;
FindDupResult FindDuplicateCards(uint16_t hl);
/* <<< factory FindDuplicateCards */
/* >>> factory FindAndRemoveCardFromList */
void FindAndRemoveCardFromList(uint8_t a, uint16_t hl);
/* <<< factory FindAndRemoveCardFromList */
#endif /* POKETCG_HOME_TRAINER_CARDS_H */
