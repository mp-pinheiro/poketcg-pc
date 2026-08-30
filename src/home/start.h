#ifndef POKETCG_HOME_START_H
#define POKETCG_HOME_START_H

#include <stdint.h>

uint8_t ShowCardPopCGBDisclaimer(void);

/* >>> factory CheckIfHasSaveData */
typedef struct { uint8_t a; uint8_t f; } CheckIfHasSaveDataResult;
CheckIfHasSaveDataResult CheckIfHasSaveData(void);
/* <<< factory CheckIfHasSaveData */
/* >>> factory PrintStartMenuDescriptionText */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; } PrintStartMenuDescriptionTextResult;
PrintStartMenuDescriptionTextResult PrintStartMenuDescriptionText(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PrintStartMenuDescriptionText */
/* >>> factory AskToContinueFromDiaryWithDuelData */
typedef struct { uint8_t a; uint8_t f; } AskToContinueFromDiaryWithDuelDataResult;
AskToContinueFromDiaryWithDuelDataResult AskToContinueFromDiaryWithDuelData(void);
/* <<< factory AskToContinueFromDiaryWithDuelData */
/* >>> factory HandleStartMenu */
void HandleStartMenu(void);
/* <<< factory HandleStartMenu */
/* >>> factory DrawPlayerPortraitAndPrintNewGameText */
void DrawPlayerPortraitAndPrintNewGameText(void);
/* <<< factory DrawPlayerPortraitAndPrintNewGameText */
/* >>> factory DeleteSaveDataForNewGame */
void DeleteSaveDataForNewGame(void);
/* <<< factory DeleteSaveDataForNewGame */
/* >>> factory HandleTitleScreen */
void HandleTitleScreen(void);
/* <<< factory HandleTitleScreen */
#endif /* POKETCG_HOME_START_H */
