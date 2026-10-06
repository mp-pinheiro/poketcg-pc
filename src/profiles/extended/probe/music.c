#include "home/music.h"
#include "probe.h"

static void adapt__SetupSound(ProbeState *s) { (void)s; _SetupSound(); }
static void adapt_SoundTimerHandler(ProbeState *s) { (void)s; SoundTimerHandler(); }
static void adapt__PlaySong(ProbeState *s) { _PlaySong(s->a); }
static void adapt__PlaySFX(ProbeState *s) { _PlaySFX(s->a); }
static void adapt__AssertSongFinished(ProbeState *s) { s->a = _AssertSongFinished(); }
static void adapt__AssertSFXFinished(ProbeState *s) { s->a = _AssertSFXFinished(); }
static void adapt__PauseSong(ProbeState *s) { (void)s; _PauseSong(); }
static void adapt__ResumeSong(ProbeState *s) { (void)s; _ResumeSong(); }

static void adapt_SetCurSong(ProbeState *s) { SetCurSong(s->a); }
static void adapt_SetCurSFX(ProbeState *s) { SetCurSFX(s->a); }
static void adapt_Music_AssertSongFinished(ProbeState *s) { s->a = Music_AssertSongFinished(); }
static void adapt_Music_AssertSFXFinished(ProbeState *s) { s->a = Music_AssertSFXFinished(); }
static void adapt_Music_SetupSound(ProbeState *s) { (void)s; Music_SetupSound(); }
static void adapt_MusicUpdate(ProbeState *s) { (void)s; MusicUpdate(); }
static void adapt_CheckForNewSound(ProbeState *s) { (void)s; CheckForNewSound(); }
static void adapt_StopAllChannels(ProbeState *s) { (void)s; StopAllChannels(); }
static void adapt_BeginSong(ProbeState *s) { BeginSong(s->a); }
static void adapt_MusicEmptyFunc(ProbeState *s) { (void)s; MusicEmptyFunc(); }
static void adapt_UpdateChannel1(ProbeState *s) { (void)s; UpdateChannel1(); }
static void adapt_UpdateChannel2(ProbeState *s) { (void)s; UpdateChannel2(); }
static void adapt_UpdateChannel3(ProbeState *s) { (void)s; UpdateChannel3(); }
static void adapt_UpdateChannel4(ProbeState *s) { (void)s; UpdateChannel4(); }

static void adapt_GetMusicCommandAndArgs(ProbeState *s)
{
	s->a = GetMusicCommandAndArgs(&s->hl);
}

static void adapt_PlayNextNote(ProbeState *s) { PlayNextNote(&s->hl, s->c); }
static void adapt_PlayNextNote_pop(ProbeState *s) { PlayNextNote_pop(s->stack[0], s->c); }

static void adapt_Music_note(ProbeState *s)
{
	Music_note(&s->hl, s->a, s->b, s->c);
}

static void adapt_Music_speed(ProbeState *s) { Music_speed(s->stack[0], s->c); }
static void adapt_Music_octave(ProbeState *s) { Music_octave(s->stack[0], s->c, s->a); }
static void adapt_Music_inc_octave(ProbeState *s) { Music_inc_octave(s->stack[0], s->c); }
static void adapt_Music_dec_octave(ProbeState *s) { Music_dec_octave(s->stack[0], s->c); }
static void adapt_Music_tie(ProbeState *s) { Music_tie(s->stack[0], s->c); }
static void adapt_Music_stereo_panning(ProbeState *s) { Music_stereo_panning(s->stack[0], s->c); }
static void adapt_Music_MainLoop(ProbeState *s) { Music_MainLoop(s->stack[0], s->c); }
static void adapt_Music_EndMainLoop(ProbeState *s) { Music_EndMainLoop(s->stack[0], s->c); }
static void adapt_Music_Loop(ProbeState *s) { Music_Loop(s->stack[0], s->c); }
static void adapt_Music_EndLoop(ProbeState *s) { Music_EndLoop(s->stack[0], s->c); }
static void adapt_Music_jp(ProbeState *s) { Music_jp(s->stack[0], s->c); }
static void adapt_Music_call(ProbeState *s) { Music_call(s->stack[0], s->c); }
static void adapt_Music_ret(ProbeState *s) { Music_ret(s->stack[0], s->c); }
static void adapt_Music_frequency_offset(ProbeState *s) { Music_frequency_offset(s->stack[0], s->c); }
static void adapt_Music_duty(ProbeState *s) { Music_duty(s->stack[0], s->c); }
static void adapt_Music_volume(ProbeState *s) { Music_volume(s->stack[0], s->c); }
static void adapt_Music_wave(ProbeState *s) { Music_wave(s->stack[0], s->c); }
static void adapt_Music_cutoff(ProbeState *s) { Music_cutoff(s->stack[0], s->c); }
static void adapt_Music_echo(ProbeState *s) { Music_echo(s->stack[0], s->c); }
static void adapt_Music_vibrato_type(ProbeState *s) { Music_vibrato_type(s->stack[0], s->c); }
static void adapt_Music_vibrato_delay(ProbeState *s) { Music_vibrato_delay(s->stack[0], s->c); }
static void adapt_Music_pitch_offset(ProbeState *s) { Music_pitch_offset(s->stack[0], s->c); }
static void adapt_Music_adjust_pitch_offset(ProbeState *s) { Music_adjust_pitch_offset(s->stack[0], s->c); }
static void adapt_Music_end(ProbeState *s) { Music_end(s->stack[0], s->c); }

static void adapt_Music_f4714(ProbeState *s) { (void)s; Music_f4714(); }
static void adapt_Music_f475a(ProbeState *s) { (void)s; Music_f475a(); }
static void adapt_Music_f479c(ProbeState *s) { (void)s; Music_f479c(); }
static void adapt_Music_f480a(ProbeState *s) { (void)s; Music_f480a(); }
static void adapt_Music_f4839(ProbeState *s) { (void)s; Music_f4839(); }
static void adapt_Music_f485a(ProbeState *s) { Music_f485a(s->a); }
static void adapt_Music_f4866(ProbeState *s) { (void)s; Music_f4866(); }
static void adapt_LoadWaveInstrument(ProbeState *s) { (void)s; LoadWaveInstrument(); }

static void adapt_UpdateVibrato(ProbeState *s)
{
	uint16_t frequency = UpdateVibrato(s->c);
	s->d = (uint8_t)(frequency >> 8u);
	s->e = (uint8_t)frequency;
}

static void adapt_Music_f490b(ProbeState *s)
{
	Music_f490b(s->a, (uint16_t)((uint16_t)s->d << 8u | s->e));
}

static void adapt_Music_f4967(ProbeState *s)
{
	MusicFrequencyResult result = Music_f4967(s->c, (uint16_t)((uint16_t)s->d << 8u | s->e));
	s->d = result.d;
	s->e = result.e;
}

static void adapt_Music_f4980(ProbeState *s) { (void)s; Music_f4980(); }
static void adapt_CheckForEndOfSong(ProbeState *s) { (void)s; CheckForEndOfSong(); }
static void adapt_Music_PauseSong(ProbeState *s) { (void)s; Music_PauseSong(); }
static void adapt_Music_ResumeSong(ProbeState *s) { (void)s; Music_ResumeSong(); }
static void adapt_BackupSong(ProbeState *s) { (void)s; BackupSong(); }
static void adapt_LoadBackup(ProbeState *s) { (void)s; LoadBackup(); }

static void adapt_CopyData(ProbeState *s)
{
	uint16_t de = (uint16_t)((uint16_t)s->d << 8u | s->e);
	CopyData(&s->hl, &de, s->a);
	s->d = (uint8_t)(de >> 8u);
	s->e = (uint8_t)de;
}

static void adapt_GetChannelStackPointer(ProbeState *s)
{
	s->hl = GetChannelStackPointer(s->c);
}

static void adapt_SetChannelStackPointer(ProbeState *s)
{
	SetChannelStackPointer(s->c, s->hl);
}

const ProbeEntry probe_entries_music[] = {
	{ "_SetupSound", adapt__SetupSound },
	{ "SoundTimerHandler", adapt_SoundTimerHandler },
	{ "_PlaySong", adapt__PlaySong },
	{ "_PlaySFX", adapt__PlaySFX },
	{ "_AssertSongFinished", adapt__AssertSongFinished },
	{ "_AssertSFXFinished", adapt__AssertSFXFinished },
	{ "_PauseSong", adapt__PauseSong },
	{ "_ResumeSong", adapt__ResumeSong },
	{ "SetCurSong", adapt_SetCurSong },
	{ "SetCurSFX", adapt_SetCurSFX },
	{ "Music_AssertSongFinished", adapt_Music_AssertSongFinished },
	{ "Music_AssertSFXFinished", adapt_Music_AssertSFXFinished },
	{ "Music_SetupSound", adapt_Music_SetupSound },
	{ "MusicUpdate", adapt_MusicUpdate },
	{ "CheckForNewSound", adapt_CheckForNewSound },
	{ "StopAllChannels", adapt_StopAllChannels },
	{ "BeginSong", adapt_BeginSong },
	{ "MusicEmptyFunc", adapt_MusicEmptyFunc },
	{ "UpdateChannel1", adapt_UpdateChannel1 },
	{ "UpdateChannel2", adapt_UpdateChannel2 },
	{ "UpdateChannel3", adapt_UpdateChannel3 },
	{ "UpdateChannel4", adapt_UpdateChannel4 },
	{ "GetMusicCommandAndArgs", adapt_GetMusicCommandAndArgs },
	{ "PlayNextNote", adapt_PlayNextNote },
	{ "Music_note", adapt_Music_note },
	{ "Music_speed", adapt_Music_speed },
	{ "Music_octave", adapt_Music_octave },
	{ "Music_inc_octave", adapt_Music_inc_octave },
	{ "Music_dec_octave", adapt_Music_dec_octave },
	{ "Music_tie", adapt_Music_tie },
	{ "Music_stereo_panning", adapt_Music_stereo_panning },
	{ "Music_MainLoop", adapt_Music_MainLoop },
	{ "Music_EndMainLoop", adapt_Music_EndMainLoop },
	{ "Music_Loop", adapt_Music_Loop },
	{ "Music_EndLoop", adapt_Music_EndLoop },
	{ "Music_jp", adapt_Music_jp },
	{ "Music_call", adapt_Music_call },
	{ "Music_ret", adapt_Music_ret },
	{ "Music_frequency_offset", adapt_Music_frequency_offset },
	{ "Music_duty", adapt_Music_duty },
	{ "Music_volume", adapt_Music_volume },
	{ "Music_wave", adapt_Music_wave },
	{ "Music_cutoff", adapt_Music_cutoff },
	{ "Music_echo", adapt_Music_echo },
	{ "Music_vibrato_type", adapt_Music_vibrato_type },
	{ "Music_vibrato_delay", adapt_Music_vibrato_delay },
	{ "Music_pitch_offset", adapt_Music_pitch_offset },
	{ "Music_adjust_pitch_offset", adapt_Music_adjust_pitch_offset },
	{ "Music_end", adapt_Music_end },
	{ "GetChannelStackPointer", adapt_GetChannelStackPointer },
	{ "SetChannelStackPointer", adapt_SetChannelStackPointer },
	{ "PlayNextNote_pop", adapt_PlayNextNote_pop },
	{ "Music_f4714", adapt_Music_f4714 },
	{ "Music_f475a", adapt_Music_f475a },
	{ "Music_f479c", adapt_Music_f479c },
	{ "LoadWaveInstrument", adapt_LoadWaveInstrument },
	{ "Music_f480a", adapt_Music_f480a },
	{ "Music_f4839", adapt_Music_f4839 },
	{ "Music_f485a", adapt_Music_f485a },
	{ "Music_f4866", adapt_Music_f4866 },
	{ "UpdateVibrato", adapt_UpdateVibrato },
	{ "Music_f490b", adapt_Music_f490b },
	{ "Music_f4967", adapt_Music_f4967 },
	{ "Music_f4980", adapt_Music_f4980 },
	{ "CheckForEndOfSong", adapt_CheckForEndOfSong },
	{ "Music_PauseSong", adapt_Music_PauseSong },
	{ "Music_ResumeSong", adapt_Music_ResumeSong },
	{ "BackupSong", adapt_BackupSong },
	{ "LoadBackup", adapt_LoadBackup },
	{ "CopyData", adapt_CopyData },
	{ NULL, NULL },
};
