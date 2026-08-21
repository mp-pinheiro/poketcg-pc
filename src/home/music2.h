#ifndef POKETCG_MUSIC2_H
#define POKETCG_MUSIC2_H

#include <stdint.h>
#include <stdbool.h>

/* Entry points via trampolines. */
void Music2_Init(void);
void Music2_Update(void);

/* Leaf routines. */
void Music2_EmptyFunc(void);
void Music2_f404e(uint8_t a);
void Music2_f4066(void);
void Music2_f406f(uint8_t a);
void Music2_PlaySong(uint8_t a);
void Music2_PlaySFX(uint8_t a);
uint8_t Music2_AssertSongFinished(void);
uint8_t Music2_AssertSFXFinished(void);
void Music2_CheckForEndOfSong(void);
void Music2_CheckForNewSound(void);
void Music2_CopyData(uint16_t *hl, uint16_t *de, uint8_t n);

/* Init / stop / begin. */
void Music2_StopAllChannels(void);
void Music2_BeginSong(uint8_t a);
void Music2_f4980(void);

/* Channel updates. */
void Music2_UpdateChannel1(void);
void Music2_UpdateChannel2(void);
void Music2_UpdateChannel3(void);
void Music2_UpdateChannel4(void);

/* PlayNextNote and command handlers. */
void Music2_PlayNextNote(uint16_t *hl, uint8_t ch);
void Music2_note(uint16_t *hl, uint8_t note, uint8_t instrument, uint8_t ch);
void Music2_speed(uint16_t *hl, uint8_t ch);
void Music2_octave(uint16_t *hl, uint8_t ch, uint8_t idx);
void Music2_inc_octave(uint16_t *hl, uint8_t ch);
void Music2_dec_octave(uint16_t *hl, uint8_t ch);
void Music2_tie(uint16_t *hl, uint8_t ch);
void Music2_stereo_panning(uint16_t *hl, uint8_t ch);
void Music2_MainLoop(uint16_t *hl, uint8_t ch);
void Music2_EndMainLoop(uint16_t *hl, uint8_t ch);
void Music2_Loop(uint16_t *hl, uint8_t ch);
void Music2_EndLoop(uint16_t *hl, uint8_t ch);
void Music2_jp(uint16_t *hl, uint8_t ch);
void Music2_call(uint16_t *hl, uint8_t ch);
void Music2_ret(uint16_t *hl, uint8_t ch);
void Music2_frequency_offset(uint16_t *hl, uint8_t ch);
void Music2_duty(uint16_t *hl, uint8_t ch);
void Music2_volume(uint16_t *hl, uint8_t ch);
void Music2_wave(uint16_t *hl, uint8_t ch);
void Music2_cutoff(uint16_t *hl, uint8_t ch);
void Music2_echo(uint16_t *hl, uint8_t ch);
void Music2_vibrato_type(uint16_t *hl, uint8_t ch);
void Music2_vibrato_delay(uint16_t *hl, uint8_t ch);
void Music2_pitch_offset(uint16_t *hl, uint8_t ch);
void Music2_adjust_pitch_offset(uint16_t *hl, uint8_t ch);
void Music2_end(uint16_t *hl, uint8_t ch);

/* Channel output to APU. */
void Music2_f4714(void);
void Music2_f475a(void);
void Music2_f479c(void);
void Music2_f480a(void);
void Music2_f4839(void);
void Music2_f485a(uint8_t ch);
void Music2_f4866(void);
void Music2_LoadWaveInstrument(void);

/* Vibrato. */
void Music2_UpdateVibrato(uint8_t ch);
void Music2_f490b(uint8_t ch);
void Music2_f4967(uint8_t ch);

/* Pause / resume. */
void Music2_PauseSong(void);
void Music2_ResumeSong(void);
void Music2_BackupSong(void);
void Music2_LoadBackup(void);

/* Stack helpers. */
uint16_t Music2_GetChannelStackPointer(uint8_t ch);
void Music2_SetChannelStackPointer(uint8_t ch, uint16_t sp);

/* >>> factory Music2_f400c_2 */
void Music2_f400c_2(uint8_t a);
/* <<< factory Music2_f400c_2 */
/* >>> factory Music2_f4018_2 */
void Music2_f4018_2(uint8_t a);
/* <<< factory Music2_f4018_2 */
/* >>> factory _AssertSFXFinished_2 */
uint8_t _AssertSFXFinished_2(void);
/* <<< factory _AssertSFXFinished_2 */
/* >>> factory _AssertSongFinished_2 */
uint8_t _AssertSongFinished_2(void);
/* <<< factory _AssertSongFinished_2 */
/* >>> factory _PauseSong_2 */
void _PauseSong_2(void);
void Music2_PauseSong(void);
void Music2_ResumeSong(void);
/* <<< factory _PauseSong_2 */
#endif /* POKETCG_MUSIC2_H */
