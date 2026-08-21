#ifndef POKETCG_HOME_DECK_SELECTION_H
#define POKETCG_HOME_DECK_SELECTION_H

#include <stdint.h>

/* >>> factory GetPointerToDeckCards */
uint16_t GetPointerToDeckCards(void);
/* <<< factory GetPointerToDeckCards */
/* >>> factory ResetCheckMenuCursorPositionAndBlink */
typedef struct {
	uint8_t a;
	uint8_t f;
} ResetCheckMenuCursorPositionAndBlinkResult;

ResetCheckMenuCursorPositionAndBlinkResult ResetCheckMenuCursorPositionAndBlink(void);
/* <<< factory ResetCheckMenuCursorPositionAndBlink */
/* >>> factory GetPointerToDeckName */
uint16_t GetPointerToDeckName(void);
/* <<< factory GetPointerToDeckName */
#endif /* POKETCG_HOME_DECK_SELECTION_H */
