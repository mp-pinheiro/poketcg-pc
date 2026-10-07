#ifndef POKETCG_MUSIC2_H
#define POKETCG_MUSIC2_H

/* >>> part includes */
#include <stdint.h>
#include <stdbool.h>
/* <<< part includes */

/* >>> factory Music2_Init */
/* Entry points via trampolines. */
void Music2_Init(void);
/* <<< factory Music2_Init */
/* >>> factory Music2_Update */
void Music2_Update(void);
/* <<< factory Music2_Update */

/* >>> factory Music2_EmptyFunc */
/* Leaf routines. */
void Music2_EmptyFunc(void);
/* <<< factory Music2_EmptyFunc */
/* >>> factory Music2_f404e */
void Music2_f404e(uint8_t a);
/* <<< factory Music2_f404e */
/* >>> factory Music2_f4066 */
void Music2_f4066(void);
/* <<< factory Music2_f4066 */
/* >>> factory Music2_f406f */
void Music2_f406f(uint8_t a);
/* <<< factory Music2_f406f */
/* >>> factory Music2_PlaySong */
void Music2_PlaySong(uint8_t a);
/* <<< factory Music2_PlaySong */
/* >>> factory Music2_PlaySFX */
void Music2_PlaySFX(uint8_t a);
/* <<< factory Music2_PlaySFX */
/* >>> factory Music2_AssertSongFinished */
uint8_t Music2_AssertSongFinished(void);
/* <<< factory Music2_AssertSongFinished */
/* >>> factory Music2_AssertSFXFinished */
uint8_t Music2_AssertSFXFinished(void);
/* <<< factory Music2_AssertSFXFinished */
/* >>> factory Music2_CheckForEndOfSong */
void Music2_CheckForEndOfSong(void);
/* <<< factory Music2_CheckForEndOfSong */
/* >>> factory Music2_CheckForNewSound */
void Music2_CheckForNewSound(void);
/* <<< factory Music2_CheckForNewSound */
/* >>> factory Music2_CopyData */
void Music2_CopyData(uint16_t *hl, uint16_t *de, uint8_t n);
/* <<< factory Music2_CopyData */

/* >>> factory Music2_StopAllChannels */
/* Init / stop / begin. */
void Music2_StopAllChannels(void);
/* <<< factory Music2_StopAllChannels */
/* >>> factory Music2_BeginSong */
void Music2_BeginSong(uint8_t a);
/* <<< factory Music2_BeginSong */
/* >>> factory Music2_f4980 */
void Music2_f4980(void);
/* <<< factory Music2_f4980 */

/* >>> factory Music2_UpdateChannel1 */
/* Channel updates. */
void Music2_UpdateChannel1(void);
/* <<< factory Music2_UpdateChannel1 */
/* >>> factory Music2_UpdateChannel2 */
void Music2_UpdateChannel2(void);
/* <<< factory Music2_UpdateChannel2 */
/* >>> factory Music2_UpdateChannel3 */
void Music2_UpdateChannel3(void);
/* <<< factory Music2_UpdateChannel3 */
/* >>> factory Music2_UpdateChannel4 */
void Music2_UpdateChannel4(void);
/* <<< factory Music2_UpdateChannel4 */

/* >>> factory Music2_PlayNextNote */
/* PlayNextNote and command handlers. */
void Music2_PlayNextNote(uint16_t *hl, uint8_t ch);
/* <<< factory Music2_PlayNextNote */
/* >>> factory Music2_note */
void Music2_note(uint16_t *hl, uint8_t note, uint8_t instrument, uint8_t ch);
/* <<< factory Music2_note */
/* >>> factory Music2_speed */
void Music2_speed(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_speed */
/* >>> factory Music2_octave */
void Music2_octave(uint16_t caller_stream, uint8_t ch, uint8_t cmd);
/* <<< factory Music2_octave */
/* >>> factory Music2_inc_octave */
void Music2_inc_octave(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_inc_octave */
/* >>> factory Music2_dec_octave */
void Music2_dec_octave(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_dec_octave */
/* >>> factory Music2_tie */
void Music2_tie(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_tie */
/* >>> factory Music2_stereo_panning */
void Music2_stereo_panning(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_stereo_panning */
/* >>> factory Music2_MainLoop */
void Music2_MainLoop(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_MainLoop */
/* >>> factory Music2_EndMainLoop */
void Music2_EndMainLoop(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_EndMainLoop */
/* >>> factory Music2_Loop */
void Music2_Loop(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_Loop */
/* >>> factory Music2_EndLoop */
void Music2_EndLoop(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_EndLoop */
/* >>> factory Music2_jp */
void Music2_jp(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_jp */
/* >>> factory Music2_call */
void Music2_call(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_call */
/* >>> factory Music2_ret */
void Music2_ret(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_ret */
/* >>> factory Music2_frequency_offset */
void Music2_frequency_offset(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_frequency_offset */
/* >>> factory Music2_duty */
void Music2_duty(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_duty */
/* >>> factory Music2_volume */
void Music2_volume(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_volume */
/* >>> factory Music2_wave */
void Music2_wave(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_wave */
/* >>> factory Music2_cutoff */
void Music2_cutoff(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_cutoff */
/* >>> factory Music2_echo */
void Music2_echo(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_echo */
/* >>> factory Music2_vibrato_type */
void Music2_vibrato_type(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_vibrato_type */
/* >>> factory Music2_vibrato_delay */
void Music2_vibrato_delay(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_vibrato_delay */
/* >>> factory Music2_pitch_offset */
void Music2_pitch_offset(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_pitch_offset */
/* >>> factory Music2_adjust_pitch_offset */
void Music2_adjust_pitch_offset(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_adjust_pitch_offset */
/* >>> factory Music2_end */
void Music2_end(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_end */

/* >>> factory Music2_f4714 */
/* Channel output to APU. */
void Music2_f4714(void);
/* <<< factory Music2_f4714 */
/* >>> factory Music2_f475a */
void Music2_f475a(void);
/* <<< factory Music2_f475a */
/* >>> factory Music2_f479c */
void Music2_f479c(void);
/* <<< factory Music2_f479c */
/* >>> factory Music2_f480a */
void Music2_f480a(void);
/* <<< factory Music2_f480a */
/* >>> factory Music2_f4839 */
void Music2_f4839(void);
/* <<< factory Music2_f4839 */
/* >>> factory Music2_f485a */
void Music2_f485a(uint8_t ch);
/* <<< factory Music2_f485a */
/* >>> factory Music2_f4866 */
void Music2_f4866(void);
/* <<< factory Music2_f4866 */
/* >>> factory Music2_LoadWaveInstrument */
void Music2_LoadWaveInstrument(void);
/* <<< factory Music2_LoadWaveInstrument */

/* >>> factory Music2_UpdateVibrato */
/* Vibrato. */
uint16_t Music2_UpdateVibrato(uint8_t ch);
/* <<< factory Music2_UpdateVibrato */
/* >>> factory Music2_f490b */
void Music2_f490b(uint8_t ch, uint16_t de);
/* <<< factory Music2_f490b */
/* >>> factory Music2_f4967 */
void Music2_f4967(uint8_t ch);
/* <<< factory Music2_f4967 */

/* >>> factory Music2_PauseSong */
/* Pause / resume. */
void Music2_PauseSong(void);
/* <<< factory Music2_PauseSong */
/* >>> factory Music2_ResumeSong */
void Music2_ResumeSong(void);
/* <<< factory Music2_ResumeSong */
/* >>> factory Music2_BackupSong */
void Music2_BackupSong(void);
/* <<< factory Music2_BackupSong */
/* >>> factory Music2_LoadBackup */
void Music2_LoadBackup(void);
/* <<< factory Music2_LoadBackup */

/* >>> factory Music2_GetChannelStackPointer */
/* Stack helpers. */
uint16_t Music2_GetChannelStackPointer(uint8_t ch);
/* <<< factory Music2_GetChannelStackPointer */
/* >>> factory Music2_SetChannelStackPointer */
void Music2_SetChannelStackPointer(uint8_t ch, uint16_t sp);
/* <<< factory Music2_SetChannelStackPointer */

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
/* >>> factory _PlaySFX_2 */
void _PlaySFX_2(uint8_t a);
/* <<< factory _PlaySFX_2 */
/* >>> factory _PlaySong_2 */
void _PlaySong_2(uint8_t a);
/* <<< factory _PlaySong_2 */
/* >>> factory _ResumeSong_2 */
void _ResumeSong_2(void);
/* <<< factory _ResumeSong_2 */
/* >>> factory Music2_f4015_2 */
void Music2_f4015_2(void);
/* <<< factory Music2_f4015_2 */
/* >>> factory _SetupSound_2 */
void _SetupSound_2(void);
/* <<< factory _SetupSound_2 */
/* >>> factory SoundTimerHandler_2 */
void SoundTimerHandler_2(void);
/* <<< factory SoundTimerHandler_2 */
/* >>> factory Music2_PlayNextNote_pop */
void Music2_PlayNextNote_pop(uint16_t caller_stream, uint8_t ch);
/* <<< factory Music2_PlayNextNote_pop */
#endif /* POKETCG_MUSIC2_H */
