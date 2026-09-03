#ifndef POKETCG_HOME_DUEL_MENUS_H
#define POKETCG_HOME_DUEL_MENUS_H

#include <stdint.h>

/* >>> factory DrawPlayersPrizeAndBenchCards */
void DrawPlayersPrizeAndBenchCards(void);
/* <<< factory DrawPlayersPrizeAndBenchCards */
/* >>> factory DrawPlayAreaToPlacePrizeCards */
void DrawPlayAreaToPlacePrizeCards(void);
/* <<< factory DrawPlayAreaToPlacePrizeCards */
/* >>> factory DrawYourOrOppPlayAreaScreen_Bank0 */
void DrawYourOrOppPlayAreaScreen_Bank0(uint16_t hl);
/* <<< factory DrawYourOrOppPlayAreaScreen_Bank0 */
/* >>> factory DrawAIPeekScreen */
typedef struct { uint8_t a; uint8_t f; } DrawAIPeekScreenResult;
DrawAIPeekScreenResult DrawAIPeekScreen(uint8_t a, uint8_t f);
/* <<< factory DrawAIPeekScreen */
/* >>> factory SelectPrizeCards */
void SelectPrizeCards(uint8_t a);
/* <<< factory SelectPrizeCards */
/* >>> factory HandlePeekSelection */
typedef struct { uint8_t a; uint8_t f; } HandlePeekSelectionV2Result;
HandlePeekSelectionV2Result HandlePeekSelection(uint8_t f);
/* <<< factory HandlePeekSelection */
/* >>> factory OpenDuelCheckMenu */
void OpenDuelCheckMenu(void);
/* <<< factory OpenDuelCheckMenu */
/* >>> factory OpenInPlayAreaScreen_FromSelectButton */
/* duel_menus.asm:11-20. BankswitchROM sets no flags (switch_rom.asm:90-93),
 * so the wrapper's carry is exactly the screen's. */
uint8_t OpenInPlayAreaScreen_FromSelectButton(void);
/* <<< factory OpenInPlayAreaScreen_FromSelectButton */
#endif /* POKETCG_HOME_DUEL_MENUS_H */
