#ifndef POKETCG_HOME_SOUND_H
#define POKETCG_HOME_SOUND_H

#include <stdint.h>

/* poketcg/src/home/sound.asm */

typedef struct { uint16_t hl, de; uint8_t a, carry; } TileConvertResult;
TileConvertResult Func_37c5(uint16_t hl, uint16_t de, uint8_t a, uint8_t carry_in);

typedef struct { uint16_t hl, de; uint8_t a; } TileConvertWrapResult;
TileConvertWrapResult Func_37a5(uint16_t hl, uint16_t de);

/* Audio wrappers — home/sound.asm farcall trampolines into bank $3d */
void SetupSound(void);
void StopMusic(void);
void PlaySong(uint8_t a);
uint8_t AssertSongFinished(void);
uint8_t AssertSFXFinished(void);
void PlaySFX_InvalidChoice(void);
void PlaySFX(uint8_t a);
void PauseSong(void);
void ResumeSong(void);
#endif /* POKETCG_HOME_SOUND_H */
