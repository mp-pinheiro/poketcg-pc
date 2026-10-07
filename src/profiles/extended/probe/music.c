/* >>> part includes */
#include "home/music.h"
#include "probe.h"
/* <<< part includes */

/* >>> part _SetupSound */
static void adapt__SetupSound(ProbeState *s) { (void)s; _SetupSound(); }
/* <<< part _SetupSound */
/* >>> part SoundTimerHandler */
static void adapt_SoundTimerHandler(ProbeState *s) { (void)s; SoundTimerHandler(); }
/* <<< part SoundTimerHandler */
/* >>> part _PlaySong */
static void adapt__PlaySong(ProbeState *s) { _PlaySong(s->a); }
/* <<< part _PlaySong */
/* >>> part _PlaySFX */
static void adapt__PlaySFX(ProbeState *s) { _PlaySFX(s->a); }
/* <<< part _PlaySFX */
/* >>> part _AssertSongFinished */
static void adapt__AssertSongFinished(ProbeState *s) { s->a = _AssertSongFinished(); }
/* <<< part _AssertSongFinished */
/* >>> part _AssertSFXFinished */
static void adapt__AssertSFXFinished(ProbeState *s) { s->a = _AssertSFXFinished(); }
/* <<< part _AssertSFXFinished */
/* >>> part _PauseSong */
static void adapt__PauseSong(ProbeState *s) { (void)s; _PauseSong(); }
/* <<< part _PauseSong */
/* >>> part _ResumeSong */
static void adapt__ResumeSong(ProbeState *s) { (void)s; _ResumeSong(); }
/* <<< part _ResumeSong */

/* >>> part SetCurSong */
static void adapt_SetCurSong(ProbeState *s) { SetCurSong(s->a); }
/* <<< part SetCurSong */
/* >>> part SetCurSFX */
static void adapt_SetCurSFX(ProbeState *s) { SetCurSFX(s->a); }
/* <<< part SetCurSFX */
/* >>> part Music_AssertSongFinished */
static void adapt_Music_AssertSongFinished(ProbeState *s) { s->a = Music_AssertSongFinished(); }
/* <<< part Music_AssertSongFinished */
/* >>> part Music_AssertSFXFinished */
static void adapt_Music_AssertSFXFinished(ProbeState *s) { s->a = Music_AssertSFXFinished(); }
/* <<< part Music_AssertSFXFinished */
/* >>> part Music_SetupSound */
static void adapt_Music_SetupSound(ProbeState *s) { (void)s; Music_SetupSound(); }
/* <<< part Music_SetupSound */
/* >>> part MusicUpdate */
static void adapt_MusicUpdate(ProbeState *s) { (void)s; MusicUpdate(); }
/* <<< part MusicUpdate */
/* >>> part CheckForNewSound */
static void adapt_CheckForNewSound(ProbeState *s) { (void)s; CheckForNewSound(); }
/* <<< part CheckForNewSound */
/* >>> part StopAllChannels */
static void adapt_StopAllChannels(ProbeState *s) { (void)s; StopAllChannels(); }
/* <<< part StopAllChannels */
/* >>> part BeginSong */
static void adapt_BeginSong(ProbeState *s) { BeginSong(s->a); }
/* <<< part BeginSong */
/* >>> part MusicEmptyFunc */
static void adapt_MusicEmptyFunc(ProbeState *s) { (void)s; MusicEmptyFunc(); }
/* <<< part MusicEmptyFunc */
/* >>> part UpdateChannel1 */
static void adapt_UpdateChannel1(ProbeState *s) { (void)s; UpdateChannel1(); }
/* <<< part UpdateChannel1 */
/* >>> part UpdateChannel2 */
static void adapt_UpdateChannel2(ProbeState *s) { (void)s; UpdateChannel2(); }
/* <<< part UpdateChannel2 */
/* >>> part UpdateChannel3 */
static void adapt_UpdateChannel3(ProbeState *s) { (void)s; UpdateChannel3(); }
/* <<< part UpdateChannel3 */
/* >>> part UpdateChannel4 */
static void adapt_UpdateChannel4(ProbeState *s) { (void)s; UpdateChannel4(); }
/* <<< part UpdateChannel4 */

/* >>> factory GetMusicCommandAndArgs */
static void adapt_GetMusicCommandAndArgs(ProbeState *s)
{
	s->a = GetMusicCommandAndArgs(&s->hl);
}
/* <<< factory GetMusicCommandAndArgs */

/* >>> part PlayNextNote */
static void adapt_PlayNextNote(ProbeState *s) { PlayNextNote(&s->hl, s->c); }
/* <<< part PlayNextNote */
/* >>> part PlayNextNote_pop */
static void adapt_PlayNextNote_pop(ProbeState *s) { PlayNextNote_pop(s->stack[0], s->c); }
/* <<< part PlayNextNote_pop */

/* >>> part Music_note */
static void adapt_Music_note(ProbeState *s)
{
	Music_note(&s->hl, s->a, s->b, s->c);
}
/* <<< part Music_note */

/* >>> part Music_speed */
static void adapt_Music_speed(ProbeState *s) { Music_speed(s->stack[0], s->c); }
/* <<< part Music_speed */
/* >>> part Music_octave */
static void adapt_Music_octave(ProbeState *s) { Music_octave(s->stack[0], s->c, s->a); }
/* <<< part Music_octave */
/* >>> part Music_inc_octave */
static void adapt_Music_inc_octave(ProbeState *s) { Music_inc_octave(s->stack[0], s->c); }
/* <<< part Music_inc_octave */
/* >>> part Music_dec_octave */
static void adapt_Music_dec_octave(ProbeState *s) { Music_dec_octave(s->stack[0], s->c); }
/* <<< part Music_dec_octave */
/* >>> part Music_tie */
static void adapt_Music_tie(ProbeState *s) { Music_tie(s->stack[0], s->c); }
/* <<< part Music_tie */
/* >>> part Music_stereo_panning */
static void adapt_Music_stereo_panning(ProbeState *s) { Music_stereo_panning(s->stack[0], s->c); }
/* <<< part Music_stereo_panning */
/* >>> part Music_MainLoop */
static void adapt_Music_MainLoop(ProbeState *s) { Music_MainLoop(s->stack[0], s->c); }
/* <<< part Music_MainLoop */
/* >>> part Music_EndMainLoop */
static void adapt_Music_EndMainLoop(ProbeState *s) { Music_EndMainLoop(s->stack[0], s->c); }
/* <<< part Music_EndMainLoop */
/* >>> part Music_Loop */
static void adapt_Music_Loop(ProbeState *s) { Music_Loop(s->stack[0], s->c); }
/* <<< part Music_Loop */
/* >>> part Music_EndLoop */
static void adapt_Music_EndLoop(ProbeState *s) { Music_EndLoop(s->stack[0], s->c); }
/* <<< part Music_EndLoop */
/* >>> part Music_jp */
static void adapt_Music_jp(ProbeState *s) { Music_jp(s->stack[0], s->c); }
/* <<< part Music_jp */
/* >>> part Music_call */
static void adapt_Music_call(ProbeState *s) { Music_call(s->stack[0], s->c); }
/* <<< part Music_call */
/* >>> part Music_ret */
static void adapt_Music_ret(ProbeState *s) { Music_ret(s->stack[0], s->c); }
/* <<< part Music_ret */
/* >>> part Music_frequency_offset */
static void adapt_Music_frequency_offset(ProbeState *s) { Music_frequency_offset(s->stack[0], s->c); }
/* <<< part Music_frequency_offset */
/* >>> part Music_duty */
static void adapt_Music_duty(ProbeState *s) { Music_duty(s->stack[0], s->c); }
/* <<< part Music_duty */
/* >>> part Music_volume */
static void adapt_Music_volume(ProbeState *s) { Music_volume(s->stack[0], s->c); }
/* <<< part Music_volume */
/* >>> part Music_wave */
static void adapt_Music_wave(ProbeState *s) { Music_wave(s->stack[0], s->c); }
/* <<< part Music_wave */
/* >>> part Music_cutoff */
static void adapt_Music_cutoff(ProbeState *s) { Music_cutoff(s->stack[0], s->c); }
/* <<< part Music_cutoff */
/* >>> part Music_echo */
static void adapt_Music_echo(ProbeState *s) { Music_echo(s->stack[0], s->c); }
/* <<< part Music_echo */
/* >>> part Music_vibrato_type */
static void adapt_Music_vibrato_type(ProbeState *s) { Music_vibrato_type(s->stack[0], s->c); }
/* <<< part Music_vibrato_type */
/* >>> part Music_vibrato_delay */
static void adapt_Music_vibrato_delay(ProbeState *s) { Music_vibrato_delay(s->stack[0], s->c); }
/* <<< part Music_vibrato_delay */
/* >>> part Music_pitch_offset */
static void adapt_Music_pitch_offset(ProbeState *s) { Music_pitch_offset(s->stack[0], s->c); }
/* <<< part Music_pitch_offset */
/* >>> part Music_adjust_pitch_offset */
static void adapt_Music_adjust_pitch_offset(ProbeState *s) { Music_adjust_pitch_offset(s->stack[0], s->c); }
/* <<< part Music_adjust_pitch_offset */
/* >>> part Music_end */
static void adapt_Music_end(ProbeState *s) { Music_end(s->stack[0], s->c); }
/* <<< part Music_end */

/* >>> part Music_f4714 */
static void adapt_Music_f4714(ProbeState *s) { (void)s; Music_f4714(); }
/* <<< part Music_f4714 */
/* >>> part Music_f475a */
static void adapt_Music_f475a(ProbeState *s) { (void)s; Music_f475a(); }
/* <<< part Music_f475a */
/* >>> part Music_f479c */
static void adapt_Music_f479c(ProbeState *s) { (void)s; Music_f479c(); }
/* <<< part Music_f479c */
/* >>> part Music_f480a */
static void adapt_Music_f480a(ProbeState *s) { (void)s; Music_f480a(); }
/* <<< part Music_f480a */
/* >>> part Music_f4839 */
static void adapt_Music_f4839(ProbeState *s) { (void)s; Music_f4839(); }
/* <<< part Music_f4839 */
/* >>> part Music_f485a */
static void adapt_Music_f485a(ProbeState *s) { Music_f485a(s->a); }
/* <<< part Music_f485a */
/* >>> part Music_f4866 */
static void adapt_Music_f4866(ProbeState *s) { (void)s; Music_f4866(); }
/* <<< part Music_f4866 */
/* >>> part LoadWaveInstrument */
static void adapt_LoadWaveInstrument(ProbeState *s) { (void)s; LoadWaveInstrument(); }
/* <<< part LoadWaveInstrument */

/* >>> factory UpdateVibrato */
static void adapt_UpdateVibrato(ProbeState *s)
{
	uint16_t frequency = UpdateVibrato(s->c);
	s->d = (uint8_t)(frequency >> 8u);
	s->e = (uint8_t)frequency;
}
/* <<< factory UpdateVibrato */

/* >>> part Music_f490b */
static void adapt_Music_f490b(ProbeState *s)
{
	Music_f490b(s->a, (uint16_t)((uint16_t)s->d << 8u | s->e));
}
/* <<< part Music_f490b */

/* >>> factory Music_f4967 */
static void adapt_Music_f4967(ProbeState *s)
{
	MusicFrequencyResult result = Music_f4967(s->c, (uint16_t)((uint16_t)s->d << 8u | s->e));
	s->d = result.d;
	s->e = result.e;
}
/* <<< factory Music_f4967 */

/* >>> part Music_f4980 */
static void adapt_Music_f4980(ProbeState *s) { (void)s; Music_f4980(); }
/* <<< part Music_f4980 */
/* >>> part CheckForEndOfSong */
static void adapt_CheckForEndOfSong(ProbeState *s) { (void)s; CheckForEndOfSong(); }
/* <<< part CheckForEndOfSong */
/* >>> part Music_PauseSong */
static void adapt_Music_PauseSong(ProbeState *s) { (void)s; Music_PauseSong(); }
/* <<< part Music_PauseSong */
/* >>> part Music_ResumeSong */
static void adapt_Music_ResumeSong(ProbeState *s) { (void)s; Music_ResumeSong(); }
/* <<< part Music_ResumeSong */
/* >>> part BackupSong */
static void adapt_BackupSong(ProbeState *s) { (void)s; BackupSong(); }
/* <<< part BackupSong */
/* >>> part LoadBackup */
static void adapt_LoadBackup(ProbeState *s) { (void)s; LoadBackup(); }
/* <<< part LoadBackup */

/* >>> factory CopyData */
static void adapt_CopyData(ProbeState *s)
{
	uint16_t de = (uint16_t)((uint16_t)s->d << 8u | s->e);
	CopyData(&s->hl, &de, s->a);
	s->d = (uint8_t)(de >> 8u);
	s->e = (uint8_t)de;
}
/* <<< factory CopyData */

/* >>> factory GetChannelStackPointer */
static void adapt_GetChannelStackPointer(ProbeState *s)
{
	s->hl = GetChannelStackPointer(s->c);
}
/* <<< factory GetChannelStackPointer */

/* >>> factory SetChannelStackPointer */
static void adapt_SetChannelStackPointer(ProbeState *s)
{
	SetChannelStackPointer(s->c, s->hl);
}
/* <<< factory SetChannelStackPointer */

/* >>> part probe_entries_music */
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
/* <<< part probe_entries_music */
