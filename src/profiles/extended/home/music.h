 #ifndef POKETCG_EXTENDED_HOME_MUSIC_H
 #define POKETCG_EXTENDED_HOME_MUSIC_H

/* >>> part includes */
 #include <stdint.h>
/* <<< part includes */

/* >>> part _SetupSound */
void _SetupSound(void);
/* <<< part _SetupSound */
/* >>> part SoundTimerHandler */
void SoundTimerHandler(void);
/* <<< part SoundTimerHandler */
/* >>> part _PlaySong */
void _PlaySong(uint8_t a);
/* <<< part _PlaySong */
/* >>> part _PlaySFX */
void _PlaySFX(uint8_t a);
/* <<< part _PlaySFX */
/* >>> part _AssertSongFinished */
uint8_t _AssertSongFinished(void);
/* <<< part _AssertSongFinished */
/* >>> part _AssertSFXFinished */
uint8_t _AssertSFXFinished(void);
/* <<< part _AssertSFXFinished */
/* >>> part _PauseSong */
void _PauseSong(void);
/* <<< part _PauseSong */
/* >>> part _ResumeSong */
void _ResumeSong(void);
/* <<< part _ResumeSong */

/* >>> part SetCurSong */
void SetCurSong(uint8_t a);
/* <<< part SetCurSong */
/* >>> part SetCurSFX */
void SetCurSFX(uint8_t a);
/* <<< part SetCurSFX */
/* >>> part Music_AssertSongFinished */
uint8_t Music_AssertSongFinished(void);
/* <<< part Music_AssertSongFinished */
/* >>> part Music_AssertSFXFinished */
uint8_t Music_AssertSFXFinished(void);
/* <<< part Music_AssertSFXFinished */
/* >>> part Music_SetupSound */
void Music_SetupSound(void);
/* <<< part Music_SetupSound */
/* >>> part MusicUpdate */
void MusicUpdate(void);
/* <<< part MusicUpdate */
/* >>> part CheckForNewSound */
void CheckForNewSound(void);
/* <<< part CheckForNewSound */
/* >>> part StopAllChannels */
void StopAllChannels(void);
/* <<< part StopAllChannels */
/* >>> part BeginSong */
void BeginSong(uint8_t a);
/* <<< part BeginSong */
/* >>> part MusicEmptyFunc */
void MusicEmptyFunc(void);
/* <<< part MusicEmptyFunc */
/* >>> part UpdateChannel1 */
void UpdateChannel1(void);
/* <<< part UpdateChannel1 */
/* >>> part UpdateChannel2 */
void UpdateChannel2(void);
/* <<< part UpdateChannel2 */
/* >>> part UpdateChannel3 */
void UpdateChannel3(void);
/* <<< part UpdateChannel3 */
/* >>> part UpdateChannel4 */
void UpdateChannel4(void);
/* <<< part UpdateChannel4 */
/* >>> factory GetMusicCommandAndArgs */
uint8_t GetMusicCommandAndArgs(uint16_t *hl);
/* <<< factory GetMusicCommandAndArgs */
/* >>> part PlayNextNote */
void PlayNextNote(uint16_t *hl, uint8_t ch);
/* <<< part PlayNextNote */
/* >>> part PlayNextNote_pop */
void PlayNextNote_pop(uint16_t caller_stream, uint8_t ch);
/* <<< part PlayNextNote_pop */
/* >>> part Music_note */
void Music_note(uint16_t *hl, uint8_t note, uint8_t instrument, uint8_t ch);
/* <<< part Music_note */
/* >>> part Music_speed */
void Music_speed(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_speed */
/* >>> part Music_octave */
void Music_octave(uint16_t caller_stream, uint8_t ch, uint8_t cmd);
/* <<< part Music_octave */
/* >>> part Music_inc_octave */
void Music_inc_octave(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_inc_octave */
/* >>> part Music_dec_octave */
void Music_dec_octave(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_dec_octave */
/* >>> part Music_tie */
void Music_tie(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_tie */
/* >>> part Music_stereo_panning */
void Music_stereo_panning(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_stereo_panning */
/* >>> part Music_MainLoop */
void Music_MainLoop(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_MainLoop */
/* >>> part Music_EndMainLoop */
void Music_EndMainLoop(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_EndMainLoop */
/* >>> part Music_Loop */
void Music_Loop(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_Loop */
/* >>> part Music_EndLoop */
void Music_EndLoop(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_EndLoop */
/* >>> part Music_jp */
void Music_jp(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_jp */
/* >>> part Music_call */
void Music_call(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_call */
/* >>> part Music_ret */
void Music_ret(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_ret */
/* >>> part Music_frequency_offset */
void Music_frequency_offset(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_frequency_offset */
/* >>> part Music_duty */
void Music_duty(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_duty */
/* >>> part Music_volume */
void Music_volume(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_volume */
/* >>> part Music_wave */
void Music_wave(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_wave */
/* >>> part Music_cutoff */
void Music_cutoff(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_cutoff */
/* >>> part Music_echo */
void Music_echo(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_echo */
/* >>> part Music_vibrato_type */
void Music_vibrato_type(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_vibrato_type */
/* >>> part Music_vibrato_delay */
void Music_vibrato_delay(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_vibrato_delay */
/* >>> part Music_pitch_offset */
void Music_pitch_offset(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_pitch_offset */
/* >>> part Music_adjust_pitch_offset */
void Music_adjust_pitch_offset(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_adjust_pitch_offset */
/* >>> part Music_end */
void Music_end(uint16_t caller_stream, uint8_t ch);
/* <<< part Music_end */

/* >>> part Music_f4714 */
void Music_f4714(void);
/* <<< part Music_f4714 */
/* >>> part Music_f475a */
void Music_f475a(void);
/* <<< part Music_f475a */
/* >>> part Music_f479c */
void Music_f479c(void);
/* <<< part Music_f479c */
/* >>> part Music_f480a */
void Music_f480a(void);
/* <<< part Music_f480a */
/* >>> part Music_f4839 */
void Music_f4839(void);
/* <<< part Music_f4839 */
/* >>> part Music_f485a */
void Music_f485a(uint8_t ch);
/* <<< part Music_f485a */
/* >>> part Music_f4866 */
void Music_f4866(void);
/* <<< part Music_f4866 */
/* >>> part LoadWaveInstrument */
void LoadWaveInstrument(void);
/* <<< part LoadWaveInstrument */
/* >>> factory UpdateVibrato */
uint16_t UpdateVibrato(uint8_t ch);
/* <<< factory UpdateVibrato */
/* >>> part Music_f490b */
void Music_f490b(uint8_t ch, uint16_t de);
/* <<< part Music_f490b */
/* >>> part MusicFrequencyResult */
typedef struct { uint8_t d; uint8_t e; } MusicFrequencyResult;
/* <<< part MusicFrequencyResult */
/* >>> part Music_f4980 */
void Music_f4980(void);
/* <<< part Music_f4980 */
/* >>> part CheckForEndOfSong */
void CheckForEndOfSong(void);
/* <<< part CheckForEndOfSong */
/* >>> factory Music_f4967 */
MusicFrequencyResult Music_f4967(uint8_t ch, uint16_t de);
/* <<< factory Music_f4967 */
/* >>> part Music_PauseSong */
void Music_PauseSong(void);
/* <<< part Music_PauseSong */
/* >>> part Music_ResumeSong */
void Music_ResumeSong(void);
/* <<< part Music_ResumeSong */
/* >>> part BackupSong */
void BackupSong(void);
/* <<< part BackupSong */
/* >>> part LoadBackup */
void LoadBackup(void);
/* <<< part LoadBackup */
/* >>> factory CopyData */
void CopyData(uint16_t *hl, uint16_t *de, uint8_t n);
/* <<< factory CopyData */
/* >>> factory GetChannelStackPointer */
uint16_t GetChannelStackPointer(uint8_t ch);
/* <<< factory GetChannelStackPointer */
/* >>> factory SetChannelStackPointer */
void SetChannelStackPointer(uint8_t ch, uint16_t sp);
/* <<< factory SetChannelStackPointer */

 #endif
