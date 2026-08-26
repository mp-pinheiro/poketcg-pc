#ifndef POKETCG_MUSIC1_H
#define POKETCG_MUSIC1_H

#include <stdint.h>
#include <stdbool.h>

/* Entry points via trampolines. */
void Music1_Init(void);
void Music1_Update(void);

/* Leaf routines. */
void Music1_EmptyFunc(void);
void Music1_f404e(uint8_t a);
void Music1_f4066(void);
void Music1_f406f(uint8_t a);
void Music1_PlaySong(uint8_t a);
void Music1_PlaySFX(uint8_t a);
uint8_t Music1_AssertSongFinished(void);
uint8_t Music1_AssertSFXFinished(void);
void Music1_CheckForEndOfSong(void);
void Music1_CheckForNewSound(void);
void Music1_CopyData(uint16_t *hl, uint16_t *de, uint8_t n);

/* Init / stop / begin. */
void Music1_StopAllChannels(void);
void Music1_BeginSong(uint8_t a);
void Music1_f4980(void);

/* Channel updates. */
void Music1_UpdateChannel1(void);
void Music1_UpdateChannel2(void);
void Music1_UpdateChannel3(void);
void Music1_UpdateChannel4(void);

/* PlayNextNote and command handlers. */
void Music1_PlayNextNote(uint16_t *hl, uint8_t ch);
void Music1_note(uint16_t *hl, uint8_t note, uint8_t instrument, uint8_t ch);
void Music1_speed(uint16_t caller_stream, uint8_t ch);
void Music1_octave(uint16_t caller_stream, uint8_t ch, uint8_t cmd);
void Music1_inc_octave(uint16_t caller_stream, uint8_t ch);
void Music1_dec_octave(uint16_t caller_stream, uint8_t ch);
void Music1_tie(uint16_t caller_stream, uint8_t ch);
void Music1_stereo_panning(uint16_t caller_stream, uint8_t ch);
void Music1_MainLoop(uint16_t caller_stream, uint8_t ch);
void Music1_EndMainLoop(uint16_t caller_stream, uint8_t ch);
void Music1_Loop(uint16_t caller_stream, uint8_t ch);
void Music1_EndLoop(uint16_t caller_stream, uint8_t ch);
void Music1_jp(uint16_t caller_stream, uint8_t ch);
void Music1_call(uint16_t caller_stream, uint8_t ch);
void Music1_ret(uint16_t caller_stream, uint8_t ch);
void Music1_frequency_offset(uint16_t caller_stream, uint8_t ch);
void Music1_duty(uint16_t caller_stream, uint8_t ch);
void Music1_volume(uint16_t caller_stream, uint8_t ch);
void Music1_wave(uint16_t caller_stream, uint8_t ch);
void Music1_cutoff(uint16_t caller_stream, uint8_t ch);
void Music1_echo(uint16_t caller_stream, uint8_t ch);
void Music1_vibrato_type(uint16_t caller_stream, uint8_t ch);
void Music1_vibrato_delay(uint16_t caller_stream, uint8_t ch);
void Music1_pitch_offset(uint16_t caller_stream, uint8_t ch);
void Music1_adjust_pitch_offset(uint16_t caller_stream, uint8_t ch);
void Music1_end(uint16_t caller_stream, uint8_t ch);

/* Channel output to APU. */
void Music1_f4714(void);
void Music1_f475a(void);
void Music1_f479c(void);
void Music1_f480a(void);
void Music1_f4839(void);
void Music1_f485a(uint8_t ch);
void Music1_f4866(void);
void Music1_LoadWaveInstrument(void);

/* Vibrato. */
void Music1_UpdateVibrato(uint8_t ch);
void Music1_f490b(uint8_t ch);
void Music1_f4967(uint8_t ch);

/* Pause / resume. */
void Music1_PauseSong(void);
void Music1_ResumeSong(void);
void Music1_BackupSong(void);
void Music1_LoadBackup(void);

/* Stack helpers. */
uint16_t Music1_GetChannelStackPointer(uint8_t ch);
void Music1_SetChannelStackPointer(uint8_t ch, uint16_t sp);

/* >>> factory _PauseSong */
void _PauseSong(void);
/* <<< factory _PauseSong */
/* >>> factory _ResumeSong */
void _ResumeSong(void);
/* <<< factory _ResumeSong */
/* >>> factory Music1_f400c */
void Music1_f400c(uint8_t a);
/* <<< factory Music1_f400c */
/* >>> factory Music1_f4018 */
void Music1_f4018(uint8_t a);
/* <<< factory Music1_f4018 */
/* >>> factory _AssertSFXFinished */
uint8_t _AssertSFXFinished(void);
uint8_t Music1_AssertSFXFinished(void);
/* <<< factory _AssertSFXFinished */
/* >>> factory _AssertSongFinished */
uint8_t _AssertSongFinished(void);
uint8_t Music1_AssertSongFinished(void);
/* <<< factory _AssertSongFinished */
/* >>> factory _PlaySFX */
void _PlaySFX(uint8_t a);
void Music1_PlaySFX(uint8_t a);
/* <<< factory _PlaySFX */
/* >>> factory _PlaySong */
void _PlaySong(uint8_t a);
void Music1_PlaySong(uint8_t a);
/* <<< factory _PlaySong */
/* >>> factory _SetupSound */
void _SetupSound(void);
void Music1_Init(void);
/* <<< factory _SetupSound */
/* >>> factory SoundTimerHandler */
void SoundTimerHandler(void);
/* <<< factory SoundTimerHandler */
/* >>> factory Music1_f4015 */
void Music1_f4015(void);
/* <<< factory Music1_f4015 */
/* >>> factory Music1_PlayNextNote_pop */
void Music1_PlayNextNote_pop(uint16_t *hl, uint8_t ch);
/* <<< factory Music1_PlayNextNote_pop */
#endif /* POKETCG_MUSIC1_H */
