 #ifndef POKETCG_HOME_SOUND_H
 #define POKETCG_HOME_SOUND_H

/* >>> part includes */
 #include <stdint.h>
/* <<< part includes */

/* >>> factory SetupSound */
void SetupSound(void);
/* <<< factory SetupSound */
/* >>> factory PlaySong */
void PlaySong(uint8_t a);
/* <<< factory PlaySong */
/* >>> factory AssertSongFinished */
uint8_t AssertSongFinished(void);
/* <<< factory AssertSongFinished */
/* >>> factory AssertSFXFinished */
uint8_t AssertSFXFinished(void);
/* <<< factory AssertSFXFinished */
/* >>> factory PlaySFX_InvalidChoice */
void PlaySFX_InvalidChoice(void);
/* <<< factory PlaySFX_InvalidChoice */
/* >>> factory PlaySFX */
void PlaySFX(uint8_t a);
/* <<< factory PlaySFX */
/* >>> factory PauseSong */
void PauseSong(void);
/* <<< factory PauseSong */
/* >>> factory ResumeSong */
void ResumeSong(void);
/* <<< factory ResumeSong */

 #endif
