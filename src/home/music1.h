#ifndef POKETCG_MUSIC1_H
#define POKETCG_MUSIC1_H

/* >>> part includes */
#include <stdint.h>
#include <stdbool.h>
/* <<< part includes */

/* >>> factory Music1_Init */
/* Entry points via trampolines. */
void Music1_Init(void);
/* <<< factory Music1_Init */
/* >>> factory Music1_Update */
void Music1_Update(void);
/* <<< factory Music1_Update */

/* >>> factory Music1_EmptyFunc */
/* Leaf routines. */
void Music1_EmptyFunc(void);
/* <<< factory Music1_EmptyFunc */
/* >>> factory Music1_f404e */
void Music1_f404e(uint8_t a);
/* <<< factory Music1_f404e */
/* >>> factory Music1_f4066 */
void Music1_f4066(void);
/* <<< factory Music1_f4066 */
/* >>> factory Music1_f406f */
void Music1_f406f(uint8_t a);
/* <<< factory Music1_f406f */
/* >>> factory Music1_PlaySong */
void Music1_PlaySong(uint8_t a);
/* <<< factory Music1_PlaySong */
/* >>> factory Music1_PlaySFX */
void Music1_PlaySFX(uint8_t a);
/* <<< factory Music1_PlaySFX */
/* >>> factory Music1_AssertSongFinished */
uint8_t Music1_AssertSongFinished(void);
/* <<< factory Music1_AssertSongFinished */
/* >>> factory Music1_AssertSFXFinished */
uint8_t Music1_AssertSFXFinished(void);
/* <<< factory Music1_AssertSFXFinished */
/* >>> factory Music1_CheckForEndOfSong */
void Music1_CheckForEndOfSong(void);
/* <<< factory Music1_CheckForEndOfSong */
/* >>> factory Music1_CheckForNewSound */
void Music1_CheckForNewSound(void);
/* <<< factory Music1_CheckForNewSound */
/* >>> factory Music1_CopyData */
void Music1_CopyData(uint16_t *hl, uint16_t *de, uint8_t n);
/* <<< factory Music1_CopyData */

/* >>> factory Music1_StopAllChannels */
/* Init / stop / begin. */
void Music1_StopAllChannels(void);
/* <<< factory Music1_StopAllChannels */
/* >>> factory Music1_BeginSong */
void Music1_BeginSong(uint8_t a);
/* <<< factory Music1_BeginSong */
/* >>> factory Music1_f4980 */
void Music1_f4980(void);
/* <<< factory Music1_f4980 */

/* >>> factory Music1_UpdateChannel1 */
/* Channel updates. */
void Music1_UpdateChannel1(void);
/* <<< factory Music1_UpdateChannel1 */
/* >>> factory Music1_UpdateChannel2 */
void Music1_UpdateChannel2(void);
/* <<< factory Music1_UpdateChannel2 */
/* >>> factory Music1_UpdateChannel3 */
void Music1_UpdateChannel3(void);
/* <<< factory Music1_UpdateChannel3 */
/* >>> factory Music1_UpdateChannel4 */
void Music1_UpdateChannel4(void);
/* <<< factory Music1_UpdateChannel4 */

/* >>> factory Music1_PlayNextNote */
/* PlayNextNote and command handlers. */
void Music1_PlayNextNote(uint16_t *hl, uint8_t ch);
/* <<< factory Music1_PlayNextNote */
/* >>> factory Music1_note */
void Music1_note(uint16_t *hl, uint8_t note, uint8_t instrument, uint8_t ch);
/* <<< factory Music1_note */
/* >>> factory Music1_speed */
void Music1_speed(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_speed */
/* >>> factory Music1_octave */
void Music1_octave(uint16_t caller_stream, uint8_t ch, uint8_t cmd);
/* <<< factory Music1_octave */
/* >>> factory Music1_inc_octave */
void Music1_inc_octave(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_inc_octave */
/* >>> factory Music1_dec_octave */
void Music1_dec_octave(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_dec_octave */
/* >>> factory Music1_tie */
void Music1_tie(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_tie */
/* >>> factory Music1_stereo_panning */
void Music1_stereo_panning(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_stereo_panning */
/* >>> factory Music1_MainLoop */
void Music1_MainLoop(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_MainLoop */
/* >>> factory Music1_EndMainLoop */
void Music1_EndMainLoop(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_EndMainLoop */
/* >>> factory Music1_Loop */
void Music1_Loop(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_Loop */
/* >>> factory Music1_EndLoop */
void Music1_EndLoop(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_EndLoop */
/* >>> factory Music1_jp */
void Music1_jp(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_jp */
/* >>> factory Music1_call */
void Music1_call(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_call */
/* >>> factory Music1_ret */
void Music1_ret(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_ret */
/* >>> factory Music1_frequency_offset */
void Music1_frequency_offset(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_frequency_offset */
/* >>> factory Music1_duty */
void Music1_duty(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_duty */
/* >>> factory Music1_volume */
void Music1_volume(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_volume */
/* >>> factory Music1_wave */
void Music1_wave(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_wave */
/* >>> factory Music1_cutoff */
void Music1_cutoff(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_cutoff */
/* >>> factory Music1_echo */
void Music1_echo(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_echo */
/* >>> factory Music1_vibrato_type */
void Music1_vibrato_type(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_vibrato_type */
/* >>> factory Music1_vibrato_delay */
void Music1_vibrato_delay(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_vibrato_delay */
/* >>> factory Music1_pitch_offset */
void Music1_pitch_offset(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_pitch_offset */
/* >>> factory Music1_adjust_pitch_offset */
void Music1_adjust_pitch_offset(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_adjust_pitch_offset */
/* >>> factory Music1_end */
void Music1_end(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_end */

/* >>> factory Music1_f4714 */
/* Channel output to APU. */
void Music1_f4714(void);
/* <<< factory Music1_f4714 */
/* >>> factory Music1_f475a */
void Music1_f475a(void);
/* <<< factory Music1_f475a */
/* >>> factory Music1_f479c */
void Music1_f479c(void);
/* <<< factory Music1_f479c */
/* >>> factory Music1_f480a */
void Music1_f480a(void);
/* <<< factory Music1_f480a */
/* >>> factory Music1_f4839 */
void Music1_f4839(void);
/* <<< factory Music1_f4839 */
/* >>> factory Music1_f485a */
void Music1_f485a(uint8_t ch);
/* <<< factory Music1_f485a */
/* >>> factory Music1_f4866 */
void Music1_f4866(void);
/* <<< factory Music1_f4866 */
/* >>> factory Music1_LoadWaveInstrument */
void Music1_LoadWaveInstrument(void);
/* <<< factory Music1_LoadWaveInstrument */

/* >>> factory Music1_UpdateVibrato */
/* Vibrato. */
uint16_t Music1_UpdateVibrato(uint8_t ch);
/* <<< factory Music1_UpdateVibrato */
/* >>> factory Music1_f490b */
void Music1_f490b(uint8_t ch, uint16_t de);
/* <<< factory Music1_f490b */
/* >>> factory Music1_f4967 */
void Music1_f4967(uint8_t ch);
/* <<< factory Music1_f4967 */

/* >>> factory Music1_PauseSong */
/* Pause / resume. */
void Music1_PauseSong(void);
/* <<< factory Music1_PauseSong */
/* >>> factory Music1_ResumeSong */
void Music1_ResumeSong(void);
/* <<< factory Music1_ResumeSong */
/* >>> factory Music1_BackupSong */
void Music1_BackupSong(void);
/* <<< factory Music1_BackupSong */
/* >>> factory Music1_LoadBackup */
void Music1_LoadBackup(void);
/* <<< factory Music1_LoadBackup */

/* >>> factory Music1_GetChannelStackPointer */
/* Stack helpers. */
uint16_t Music1_GetChannelStackPointer(uint8_t ch);
/* <<< factory Music1_GetChannelStackPointer */
/* >>> factory Music1_SetChannelStackPointer */
void Music1_SetChannelStackPointer(uint8_t ch, uint16_t sp);
/* <<< factory Music1_SetChannelStackPointer */

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
void Music1_PlayNextNote_pop(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music1_PlayNextNote_pop */
#endif /* POKETCG_MUSIC1_H */
