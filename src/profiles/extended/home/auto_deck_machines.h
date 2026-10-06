#ifndef POKETCG_HOME_AUTO_DECK_MACHINES_H
#define POKETCG_HOME_AUTO_DECK_MACHINES_H

#include <stdint.h>

/* >>> factory ReadAutoDeckConfiguration */
void ReadAutoDeckConfiguration(void);
/* <<< factory ReadAutoDeckConfiguration */
/* >>> factory CheckWhichDecksToDismantleToBuildSavedDeck */
typedef struct { uint8_t a; uint8_t f; } CheckWhichDecksToDismantleToBuildSavedDeckResult;
CheckWhichDecksToDismantleToBuildSavedDeckResult CheckWhichDecksToDismantleToBuildSavedDeck(void);
/* <<< factory CheckWhichDecksToDismantleToBuildSavedDeck */
#endif /* POKETCG_HOME_AUTO_DECK_MACHINES_H */
