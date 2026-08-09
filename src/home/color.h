#ifndef POKETCG_HOME_COLOR_H
#define POKETCG_HOME_COLOR_H

#include <stdint.h>

typedef struct { uint8_t a, c; } FadeColorResult;

void LoadConsolePaletteData(void);
void FadeScreenToWhite(void);
void FadeScreenFromWhite_BackupPalsAndSetWhite(void);
void SetWhitePalettes(void);
void Func_10d17(void);
void Func_10d50(void);
uint8_t FadeScreenFromWhite(void);
uint8_t FadeScreenToTempPals(void);
void RestoreFirstColorInOBPals(void);
void FadeDMGPalettes(void);
uint8_t FadeDMGPalettes_CalculateMixPalette(uint8_t b, uint8_t c);
uint8_t FadeDMGPalettes_GetMixShadeValue(uint8_t b, uint8_t c);
void FadeOBPalIntoTemp(void);
void FadeBGPalIntoTemp1(void);
void FadeBGPalIntoTemp2(void);
void FadeBGPalIntoTemp3(void);
FadeColorResult FadePalIntoAnother_GetFadedColor(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
uint8_t FadePalIntoAnother_FadeColor(uint8_t a, uint16_t hl);
void FlashScreenToWhite(uint8_t c);
void CopyPalsToSRAMBuffer(void);
void LoadPalsFromSRAMBuffer(void);
void Func_10d74(void);

#endif
