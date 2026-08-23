#ifndef POKETCG_HOME_STARTER_DECK_H
#define POKETCG_HOME_STARTER_DECK_H

#include <stdint.h>

/* >>> factory CopyDeckNameAndCards */
void CopyDeckNameAndCards(uint8_t a, uint16_t hl);
/* <<< factory CopyDeckNameAndCards */
/* >>> factory InitSaveData */
void InitSaveData(void);
/* <<< factory InitSaveData */
/* >>> factory _AddStarterDeck */
void _AddStarterDeck(uint8_t a);
/* <<< factory _AddStarterDeck */
#endif /* POKETCG_HOME_STARTER_DECK_H */
