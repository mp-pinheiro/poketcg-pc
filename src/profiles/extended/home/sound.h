 #ifndef POKETCG_HOME_SOUND_H
 #define POKETCG_HOME_SOUND_H

 #include <stdint.h>

void SetupSound(void);
void PlaySong(uint8_t a);
uint8_t AssertSongFinished(void);
uint8_t AssertSFXFinished(void);
void PlaySFX_InvalidChoice(void);
void PlaySFX(uint8_t a);
void PauseSong(void);
void ResumeSong(void);

 #endif
