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
/* >>> factory CheckIfCurDeckIsValid */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} CheckIfCurDeckIsValidResult;

CheckIfCurDeckIsValidResult CheckIfCurDeckIsValid(void);
/* <<< factory CheckIfCurDeckIsValid */
/* >>> factory CancelDeckSelectionSubMenu */
void CancelDeckSelectionSubMenu(void);
/* <<< factory CancelDeckSelectionSubMenu */
/* >>> factory CopyDeckFromSRAM */
typedef struct { uint8_t a; uint8_t f; uint16_t de; uint16_t hl; } CopyDeckFromSRAMResult;
CopyDeckFromSRAMResult CopyDeckFromSRAM(uint16_t de, uint16_t hl);
/* <<< factory CopyDeckFromSRAM */
/* >>> factory Func_9001 */
typedef struct { uint8_t a; uint8_t f; uint8_t d; uint8_t e; uint16_t hl; } Func_9001Result;
Func_9001Result Func_9001(uint16_t hl);
/* <<< factory Func_9001 */
/* >>> factory LoadHandCardsIcon */
typedef struct { uint16_t hl; uint8_t d; uint8_t e; } LoadHandCardsIconResult;
LoadHandCardsIconResult LoadHandCardsIcon(void);
/* <<< factory LoadHandCardsIcon */
/* >>> factory InitPromotionalCardAndDeckCounterSaveData */
LoadHandCardsIconResult InitPromotionalCardAndDeckCounterSaveData(void);
/* <<< factory InitPromotionalCardAndDeckCounterSaveData */
/* >>> factory PrepareMenuGraphics */
void PrepareMenuGraphics(void);
/* <<< factory PrepareMenuGraphics */
/* >>> factory EmptyScreenAndLoadFontDuelAndHandCardsIcons */
void EmptyScreenAndLoadFontDuelAndHandCardsIcons(void);
/* <<< factory EmptyScreenAndLoadFontDuelAndHandCardsIcons */
/* >>> factory PrintThereIsNoDeckHereText */
uint8_t PrintThereIsNoDeckHereText(void);
/* <<< factory PrintThereIsNoDeckHereText */
/* >>> factory WriteCardListsTerminatorBytes */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint16_t hl; } WriteCardListsTerminatorBytesResult;
WriteCardListsTerminatorBytesResult WriteCardListsTerminatorBytes(void);
/* <<< factory WriteCardListsTerminatorBytes */
/* >>> factory OpenDeckConfirmationMenu */
void OpenDeckConfirmationMenu(uint16_t de, uint16_t hl);
/* <<< factory OpenDeckConfirmationMenu */
/* >>> factory HandleStartButtonInDeckSelectionMenu */
typedef struct { uint8_t a; uint8_t f; } HandleStartButtonInDeckSelectionMenuResult;
HandleStartButtonInDeckSelectionMenuResult HandleStartButtonInDeckSelectionMenu(void);
/* <<< factory HandleStartButtonInDeckSelectionMenu */
/* >>> factory InputCurDeckName */
void InputCurDeckName(void);
/* <<< factory InputCurDeckName */
#endif /* POKETCG_HOME_DECK_SELECTION_H */
