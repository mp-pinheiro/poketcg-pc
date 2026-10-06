 #ifndef POKETCG_EXTENDED_HOME_MUSIC_H
 #define POKETCG_EXTENDED_HOME_MUSIC_H

 #include <stdint.h>

void _SetupSound(void);
void SoundTimerHandler(void);
void _PlaySong(uint8_t a);
void _PlaySFX(uint8_t a);
uint8_t _AssertSongFinished(void);
uint8_t _AssertSFXFinished(void);
void _PauseSong(void);
void _ResumeSong(void);

void SetCurSong(uint8_t a);
void SetCurSFX(uint8_t a);
uint8_t Music_AssertSongFinished(void);
uint8_t Music_AssertSFXFinished(void);
void Music_SetupSound(void);
void MusicUpdate(void);
void CheckForNewSound(void);
void StopAllChannels(void);
void BeginSong(uint8_t a);
void MusicEmptyFunc(void);
void UpdateChannel1(void);
void UpdateChannel2(void);
void UpdateChannel3(void);
void UpdateChannel4(void);
uint8_t GetMusicCommandAndArgs(uint16_t *hl);
void PlayNextNote(uint16_t *hl, uint8_t ch);
void PlayNextNote_pop(uint16_t caller_stream, uint8_t ch);
void Music_note(uint16_t *hl, uint8_t note, uint8_t instrument, uint8_t ch);
void Music_speed(uint16_t caller_stream, uint8_t ch);
void Music_octave(uint16_t caller_stream, uint8_t ch, uint8_t cmd);
void Music_inc_octave(uint16_t caller_stream, uint8_t ch);
void Music_dec_octave(uint16_t caller_stream, uint8_t ch);
void Music_tie(uint16_t caller_stream, uint8_t ch);
void Music_stereo_panning(uint16_t caller_stream, uint8_t ch);
void Music_MainLoop(uint16_t caller_stream, uint8_t ch);
void Music_EndMainLoop(uint16_t caller_stream, uint8_t ch);
void Music_Loop(uint16_t caller_stream, uint8_t ch);
void Music_EndLoop(uint16_t caller_stream, uint8_t ch);
void Music_jp(uint16_t caller_stream, uint8_t ch);
void Music_call(uint16_t caller_stream, uint8_t ch);
void Music_ret(uint16_t caller_stream, uint8_t ch);
void Music_frequency_offset(uint16_t caller_stream, uint8_t ch);
void Music_duty(uint16_t caller_stream, uint8_t ch);
void Music_volume(uint16_t caller_stream, uint8_t ch);
void Music_wave(uint16_t caller_stream, uint8_t ch);
void Music_cutoff(uint16_t caller_stream, uint8_t ch);
void Music_echo(uint16_t caller_stream, uint8_t ch);
void Music_vibrato_type(uint16_t caller_stream, uint8_t ch);
void Music_vibrato_delay(uint16_t caller_stream, uint8_t ch);
void Music_pitch_offset(uint16_t caller_stream, uint8_t ch);
void Music_adjust_pitch_offset(uint16_t caller_stream, uint8_t ch);
void Music_end(uint16_t caller_stream, uint8_t ch);

void Music_f4714(void);
void Music_f475a(void);
void Music_f479c(void);
void Music_f480a(void);
void Music_f4839(void);
void Music_f485a(uint8_t ch);
void Music_f4866(void);
void LoadWaveInstrument(void);
uint16_t UpdateVibrato(uint8_t ch);
void Music_f490b(uint8_t ch, uint16_t de);
typedef struct { uint8_t d; uint8_t e; } MusicFrequencyResult;
void Music_f4980(void);
void CheckForEndOfSong(void);
MusicFrequencyResult Music_f4967(uint8_t ch, uint16_t de);
void Music_PauseSong(void);
void Music_ResumeSong(void);
void BackupSong(void);
void LoadBackup(void);
void CopyData(uint16_t *hl, uint16_t *de, uint8_t n);
uint16_t GetChannelStackPointer(uint8_t ch);
void SetChannelStackPointer(uint8_t ch, uint16_t sp);

 #endif
