#ifndef POKETCG_HOME_CORE_H
#define POKETCG_HOME_CORE_H

#include <stdint.h>

/* >>> factory SetLineSeparation */
void SetLineSeparation(uint8_t a);
/* <<< factory SetLineSeparation */
/* >>> factory PlayAreaScreenMenuFunction */
uint8_t PlayAreaScreenMenuFunction(void);
/* <<< factory PlayAreaScreenMenuFunction */
/* >>> factory SwitchAttackPage */
void SwitchAttackPage(void);
/* <<< factory SwitchAttackPage */
/* >>> factory CopyCGBCardPalette */
void CopyCGBCardPalette(uint8_t a);
/* <<< factory CopyCGBCardPalette */
/* >>> factory CreateCardAttrBlkPacket_DataSet */
uint16_t CreateCardAttrBlkPacket_DataSet(uint16_t hl, uint8_t a, uint8_t d, uint8_t e);
/* <<< factory CreateCardAttrBlkPacket_DataSet */
/* >>> factory SaveDuelDataToDE */
void SaveDuelDataToDE(uint16_t de);
/* <<< factory SaveDuelDataToDE */
/* >>> factory LoadSavedDuelDataFromDE */
void LoadSavedDuelDataFromDE(uint16_t de);
/* <<< factory LoadSavedDuelDataFromDE */
/* >>> factory SetBGP7OrSGB2ToCardPalette */
void SetBGP7OrSGB2ToCardPalette(void);
/* <<< factory SetBGP7OrSGB2ToCardPalette */
/* >>> factory JPWriteByteToBGMap0 */
void JPWriteByteToBGMap0(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory JPWriteByteToBGMap0 */
/* >>> factory ZeroObjectPositionsAndToggleOAMCopy */
void ZeroObjectPositionsAndToggleOAMCopy(void);
/* <<< factory ZeroObjectPositionsAndToggleOAMCopy */
/* >>> factory LoadPlayerDeck */
void LoadPlayerDeck(void);
/* <<< factory LoadPlayerDeck */
/* >>> factory PrintPracticeDuelDrMasonInstructions */
void PrintPracticeDuelDrMasonInstructions(uint16_t hl);
/* <<< factory PrintPracticeDuelDrMasonInstructions */
/* >>> factory PrintPracticeDuelInstructionsTextBoxLabel */
void PrintPracticeDuelInstructionsTextBoxLabel(void);
/* <<< factory PrintPracticeDuelInstructionsTextBoxLabel */
/* >>> factory SwitchCardPage */
typedef struct { uint8_t a; uint8_t carry; } CardPageResult;
CardPageResult SwitchCardPage(uint8_t a);
/* <<< factory SwitchCardPage */
/* >>> factory CardPageSwitch_00 */
CardPageResult CardPageSwitch_00(void);
/* <<< factory CardPageSwitch_00 */
/* >>> factory LoadLoaded1CardGfx */
void LoadLoaded1CardGfx(uint16_t de);
/* <<< factory LoadLoaded1CardGfx */
/* >>> factory SetSGB3ToCardPalette */
void SetSGB3ToCardPalette(void);
/* <<< factory SetSGB3ToCardPalette */
/* >>> factory LookForCardIDInPlayArea_Bank5 */
typedef struct { uint8_t a; uint8_t b; uint8_t f; } LookResult;
LookResult LookForCardIDInPlayArea_Bank5(uint8_t a, uint8_t b);
/* <<< factory LookForCardIDInPlayArea_Bank5 */
/* >>> factory ClearMemory_Bank5 */
void ClearMemory_Bank5(uint8_t a, uint16_t hl);
/* <<< factory ClearMemory_Bank5 */
/* >>> factory CheckCardPageExists */
typedef struct { uint8_t a; uint8_t zero; } CardPageExistsResult;
CardPageExistsResult CheckCardPageExists(uint16_t *hl);
/* <<< factory CheckCardPageExists */
/* >>> factory CardPageSwitch_PokemonEnd */
CardPageResult CardPageSwitch_PokemonEnd(void);
/* <<< factory CardPageSwitch_PokemonEnd */
/* >>> factory SetCardListInfoBoxText */
void SetCardListInfoBoxText(uint16_t hl);
/* <<< factory SetCardListInfoBoxText */
/* >>> factory LoadCardNameToTxRam2 */
void LoadCardNameToTxRam2(uint8_t a);
/* <<< factory LoadCardNameToTxRam2 */
/* >>> factory LoadCardNameToTxRam2_b */
void LoadCardNameToTxRam2_b(uint8_t a);
/* <<< factory LoadCardNameToTxRam2_b */
/* >>> factory GetAnimCoordsAndFlags */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; } AnimCoordsResult;
AnimCoordsResult GetAnimCoordsAndFlags(void);
/* <<< factory GetAnimCoordsAndFlags */
/* >>> factory PlayBufferedDuelAnimations */
typedef struct { uint8_t a; uint8_t f; } AnimBufferResult;
AnimBufferResult PlayBufferedDuelAnimations(void);
/* <<< factory PlayBufferedDuelAnimations */
/* >>> factory CopyListWithFFTerminatorFromHLToDE_Bank5 */
typedef struct { uint8_t a; uint8_t f; } CopyListResult;
CopyListResult CopyListWithFFTerminatorFromHLToDE_Bank5(uint16_t *hl, uint16_t *de);
/* <<< factory CopyListWithFFTerminatorFromHLToDE_Bank5 */
/* >>> factory CheckEnergyFlagsNeededInList */
typedef struct { uint8_t a; uint8_t carry; } EnergyFlagsResult;
EnergyFlagsResult CheckEnergyFlagsNeededInList(uint8_t a);
/* <<< factory CheckEnergyFlagsNeededInList */
#endif /* POKETCG_HOME_CORE_H */
