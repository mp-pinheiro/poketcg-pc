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
/* >>> factory InitDeckBuildingParams */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint16_t de;
	uint16_t hl;
} InitDeckBuildingParamsResult;

InitDeckBuildingParamsResult InitDeckBuildingParams(uint16_t *hl, uint8_t f);
/* <<< factory InitDeckBuildingParams */
#endif /* POKETCG_HOME_DECK_SELECTION_H */
