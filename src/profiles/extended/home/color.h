#ifndef POKETCG_HOME_COLOR_H
#define POKETCG_HOME_COLOR_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part FadeColorResult */
typedef struct { uint8_t a, c; } FadeColorResult;
/* <<< part FadeColorResult */

/* >>> factory FadeScreenToWhite */
void FadeScreenToWhite(void);
/* <<< factory FadeScreenToWhite */
/* >>> factory FadeScreenFromWhite_BackupPalsAndSetWhite */
void FadeScreenFromWhite_BackupPalsAndSetWhite(void);
/* <<< factory FadeScreenFromWhite_BackupPalsAndSetWhite */
/* >>> factory SetWhitePalettes */
void SetWhitePalettes(void);
/* <<< factory SetWhitePalettes */
/* >>> factory Func_10d17 */
void Func_10d17(void);
/* <<< factory Func_10d17 */
/* >>> factory Func_10d50 */
void Func_10d50(void);
/* <<< factory Func_10d50 */
/* >>> factory FadeScreenFromWhite */
uint8_t FadeScreenFromWhite(void);
/* <<< factory FadeScreenFromWhite */
/* >>> factory FadeScreenToTempPals */
uint8_t FadeScreenToTempPals(void);
/* <<< factory FadeScreenToTempPals */
/* >>> factory RestoreFirstColorInOBPals */
void RestoreFirstColorInOBPals(void);
/* <<< factory RestoreFirstColorInOBPals */
/* >>> factory FadeDMGPalettes */
void FadeDMGPalettes(void);
/* <<< factory FadeDMGPalettes */
/* >>> factory FadeDMGPalettes_CalculateMixPalette */
uint8_t FadeDMGPalettes_CalculateMixPalette(uint8_t b, uint8_t c);
/* <<< factory FadeDMGPalettes_CalculateMixPalette */
/* >>> factory FadeDMGPalettes_GetMixShadeValue */
uint8_t FadeDMGPalettes_GetMixShadeValue(uint8_t b, uint8_t c);
/* <<< factory FadeDMGPalettes_GetMixShadeValue */
/* >>> factory FadeOBPalIntoTemp */
void FadeOBPalIntoTemp(void);
/* <<< factory FadeOBPalIntoTemp */
/* >>> factory FadeBGPalIntoTemp1 */
void FadeBGPalIntoTemp1(void);
/* <<< factory FadeBGPalIntoTemp1 */
/* >>> factory FadeBGPalIntoTemp2 */
void FadeBGPalIntoTemp2(void);
/* <<< factory FadeBGPalIntoTemp2 */
/* >>> factory FadeBGPalIntoTemp3 */
void FadeBGPalIntoTemp3(void);
/* <<< factory FadeBGPalIntoTemp3 */
/* >>> factory FadePalIntoAnother_GetFadedColor */
FadeColorResult FadePalIntoAnother_GetFadedColor(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory FadePalIntoAnother_GetFadedColor */
/* >>> factory FadePalIntoAnother_FadeColor */
uint8_t FadePalIntoAnother_FadeColor(uint8_t a, uint16_t hl);
/* <<< factory FadePalIntoAnother_FadeColor */
/* >>> factory FlashScreenToWhite */
void FlashScreenToWhite(uint8_t c);
/* <<< factory FlashScreenToWhite */
/* >>> factory CopyPalsToSRAMBuffer */
void CopyPalsToSRAMBuffer(void);
/* <<< factory CopyPalsToSRAMBuffer */
/* >>> factory LoadPalsFromSRAMBuffer */
void LoadPalsFromSRAMBuffer(void);
/* <<< factory LoadPalsFromSRAMBuffer */
/* >>> factory Func_10d74 */
void Func_10d74(void);
/* <<< factory Func_10d74 */

#endif
