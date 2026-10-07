#ifndef POKETCG_HOME_SOUND_H
#define POKETCG_HOME_SOUND_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part TileConvertResult */
/* poketcg/src/home/sound.asm */

typedef struct { uint16_t hl, de; uint8_t a, carry; } TileConvertResult;
/* <<< part TileConvertResult */
/* >>> factory Func_37c5 */
TileConvertResult Func_37c5(uint16_t hl, uint16_t de, uint8_t a, uint8_t carry_in);
/* <<< factory Func_37c5 */

/* >>> part TileConvertWrapResult */
typedef struct { uint16_t hl, de; uint8_t a; } TileConvertWrapResult;
/* <<< part TileConvertWrapResult */
/* >>> factory Func_37a5 */
TileConvertWrapResult Func_37a5(uint16_t hl, uint16_t de);
/* <<< factory Func_37a5 */

/* >>> part SetupSound */
/* Audio wrappers — home/sound.asm farcall trampolines into bank $3d */
void SetupSound(void);
/* <<< part SetupSound */
/* >>> part StopMusic */
void StopMusic(void);
/* <<< part StopMusic */
/* >>> part PlaySong */
void PlaySong(uint8_t a);
/* <<< part PlaySong */
/* >>> part AssertSongFinished */
uint8_t AssertSongFinished(void);
/* <<< part AssertSongFinished */
/* >>> part AssertSFXFinished */
uint8_t AssertSFXFinished(void);
/* <<< part AssertSFXFinished */
/* >>> part PlaySFX_InvalidChoice */
void PlaySFX_InvalidChoice(void);
/* <<< part PlaySFX_InvalidChoice */
/* >>> part PlaySFX */
void PlaySFX(uint8_t a);
/* <<< part PlaySFX */
/* >>> part PauseSong */
void PauseSong(void);
/* <<< part PauseSong */
/* >>> part ResumeSong */
void ResumeSong(void);
/* <<< part ResumeSong */
#endif /* POKETCG_HOME_SOUND_H */
