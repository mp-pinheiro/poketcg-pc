#ifndef POKETCG_HOME_PLAY_AREA_H
#define POKETCG_HOME_PLAY_AREA_H

#include <stdint.h>

void ZeroObjectPositionsAndToggleOAMCopy_Bank6(void);

/* >>> factory OpenInPlayAreaScreen_HandleInput */
typedef struct { uint8_t a; uint8_t f; } OpenInPlayAreaScreenHandleInputResult;
OpenInPlayAreaScreenHandleInputResult OpenInPlayAreaScreen_HandleInput(void);
/* <<< factory OpenInPlayAreaScreen_HandleInput */
/* >>> factory OpenInPlayAreaScreen_TurnHolderPlayArea */
void OpenInPlayAreaScreen_TurnHolderPlayArea(void);
/* <<< factory OpenInPlayAreaScreen_TurnHolderPlayArea */
/* >>> factory OpenInPlayAreaScreen_NonTurnHolderPlayArea */
/* >>> factory OpenInPlayAreaScreen_NonTurnHolderPlayArea */
void OpenInPlayAreaScreen_NonTurnHolderPlayArea(void);
/* <<< factory OpenInPlayAreaScreen_NonTurnHolderPlayArea */
#endif
