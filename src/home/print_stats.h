#ifndef POKETCG_HOME_PRINT_STATS_H
#define POKETCG_HOME_PRINT_STATS_H

#include <stdint.h>

/* >>> factory DrawPauseMenuPlayerPortrait */
void DrawPauseMenuPlayerPortrait(void);
void DrawPlayerPortrait(void);
/* <<< factory DrawPauseMenuPlayerPortrait */
/* >>> factory FlashReceivedMedal */
void FlashReceivedMedal(void);
/* <<< factory FlashReceivedMedal */
/* >>> factory ConvertWordToNumericalDigits */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } ConvertWordToNumericalDigitsResult;
ConvertWordToNumericalDigitsResult ConvertWordToNumericalDigits(uint16_t hl);
/* <<< factory ConvertWordToNumericalDigits */
/* >>> factory PrintAlbumProgress_SkipGetProgress */
void PrintAlbumProgress_SkipGetProgress(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory PrintAlbumProgress_SkipGetProgress */
/* >>> factory PrintPlayTime_SkipUpdateTime */
void PrintPlayTime_SkipUpdateTime(uint8_t b, uint8_t c);
/* <<< factory PrintPlayTime_SkipUpdateTime */
/* >>> factory PrintAlbumProgress */
void PrintAlbumProgress(uint8_t b, uint8_t c);
/* <<< factory PrintAlbumProgress */
/* >>> factory PrintPlayTime */
void PrintPlayTime(uint8_t b, uint8_t c);
/* <<< factory PrintPlayTime */
/* >>> factory PrintMedalCount */
void PrintMedalCount(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PrintMedalCount */
#endif /* POKETCG_HOME_PRINT_STATS_H */
