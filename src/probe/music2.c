/* >>> part includes */
#include "home/music2.h"
#include "probe.h"
#include "mem.h"
#include "generated/wram.h"
/* <<< part includes */

/* >>> factory Music2_EmptyFunc */
/* ── Leaf adapters ───────────────────────────────────────────────────── */

static void adapt_Music2_EmptyFunc(ProbeState *s)
{ (void)s; Music2_EmptyFunc(); }
/* <<< factory Music2_EmptyFunc */

/* >>> factory Music2_f404e */
static void adapt_Music2_f404e(ProbeState *s)
{ Music2_f404e(s->a); }
/* <<< factory Music2_f404e */

/* >>> factory Music2_f4066 */
static void adapt_Music2_f4066(ProbeState *s)
{ (void)s; Music2_f4066(); }
/* <<< factory Music2_f4066 */

/* >>> factory Music2_f406f */
static void adapt_Music2_f406f(ProbeState *s)
{ Music2_f406f(s->a); }
/* <<< factory Music2_f406f */

/* >>> factory Music2_PlaySong */
static void adapt_Music2_PlaySong(ProbeState *s)
{ Music2_PlaySong(s->a); }
/* <<< factory Music2_PlaySong */

/* >>> factory Music2_PlaySFX */
static void adapt_Music2_PlaySFX(ProbeState *s)
{ Music2_PlaySFX(s->a); }
/* <<< factory Music2_PlaySFX */

/* >>> factory Music2_AssertSongFinished */
static void adapt_Music2_AssertSongFinished(ProbeState *s)
{ s->a = Music2_AssertSongFinished(); }
/* <<< factory Music2_AssertSongFinished */

/* >>> factory Music2_AssertSFXFinished */
static void adapt_Music2_AssertSFXFinished(ProbeState *s)
{ s->a = Music2_AssertSFXFinished(); }
/* <<< factory Music2_AssertSFXFinished */

/* >>> factory Music2_CheckForEndOfSong */
static void adapt_Music2_CheckForEndOfSong(ProbeState *s)
{ (void)s; Music2_CheckForEndOfSong(); }
/* <<< factory Music2_CheckForEndOfSong */

/* >>> factory Music2_CheckForNewSound */
static void adapt_Music2_CheckForNewSound(ProbeState *s)
{ (void)s; Music2_CheckForNewSound(); }
/* <<< factory Music2_CheckForNewSound */

/* >>> factory Music2_Init */
static void adapt_Music2_Init(ProbeState *s)
{ (void)s; Music2_Init(); }
/* <<< factory Music2_Init */

/* >>> factory Music2_Update */
static void adapt_Music2_Update(ProbeState *s)
{ (void)s; Music2_Update(); }
/* <<< factory Music2_Update */

/* >>> factory Music2_StopAllChannels */
static void adapt_Music2_StopAllChannels(ProbeState *s)
{ (void)s; Music2_StopAllChannels(); }
/* <<< factory Music2_StopAllChannels */

/* >>> factory Music2_f4980 */
static void adapt_Music2_f4980(ProbeState *s)
{ (void)s; Music2_f4980(); }
/* <<< factory Music2_f4980 */

/* >>> factory Music2_BeginSong */
static void adapt_Music2_BeginSong(ProbeState *s)
{ Music2_BeginSong(s->a); }
/* <<< factory Music2_BeginSong */

/* >>> factory Music2_CopyData */
static void adapt_Music2_CopyData(ProbeState *s)
{
	uint16_t de = (uint16_t)s->d << 8 | s->e;
	Music2_CopyData(&s->hl, &de, s->a);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory Music2_CopyData */

/* >>> factory Music2_UpdateChannel1 */
/* ── Channel updaters ────────────────────────────────────────────────── */

static void adapt_Music2_UpdateChannel1(ProbeState *s)
{ (void)s; Music2_UpdateChannel1(); }
/* <<< factory Music2_UpdateChannel1 */

/* >>> factory Music2_UpdateChannel2 */
static void adapt_Music2_UpdateChannel2(ProbeState *s)
{ (void)s; Music2_UpdateChannel2(); }
/* <<< factory Music2_UpdateChannel2 */

/* >>> factory Music2_UpdateChannel3 */
static void adapt_Music2_UpdateChannel3(ProbeState *s)
{ (void)s; Music2_UpdateChannel3(); }
/* <<< factory Music2_UpdateChannel3 */

/* >>> factory Music2_UpdateChannel4 */
static void adapt_Music2_UpdateChannel4(ProbeState *s)
{ (void)s; Music2_UpdateChannel4(); }
/* <<< factory Music2_UpdateChannel4 */

/* >>> factory Music2_PlayNextNote */
/* ── PlayNextNote ────────────────────────────────────────────────────── */

/* music2.asm:578 `ld a,[hli]` overwrites a immediately; the channel arrives in
 * c, which every handler indexes with `add hl, bc`. */
static void adapt_Music2_PlayNextNote(ProbeState *s)
{ Music2_PlayNextNote(&s->hl, s->c); }
/* <<< factory Music2_PlayNextNote */

/* >>> factory Music2_speed */
/* ── Command handlers ────────────────────────────────────────────────── */

static void adapt_Music2_speed(ProbeState *s)
{ Music2_speed(s->stack[0], s->c); }
/* <<< factory Music2_speed */

/* >>> factory Music2_octave */
static void adapt_Music2_octave(ProbeState *s)
{ Music2_octave(s->stack[0], s->c, s->a); }
/* <<< factory Music2_octave */

/* >>> factory Music2_inc_octave */
static void adapt_Music2_inc_octave(ProbeState *s)
{ Music2_inc_octave(s->stack[0], s->c); }
/* <<< factory Music2_inc_octave */

/* >>> factory Music2_dec_octave */
static void adapt_Music2_dec_octave(ProbeState *s)
{ Music2_dec_octave(s->stack[0], s->c); }
/* <<< factory Music2_dec_octave */

/* >>> factory Music2_tie */
static void adapt_Music2_tie(ProbeState *s)
{ Music2_tie(s->stack[0], s->c); }
/* <<< factory Music2_tie */

/* >>> factory Music2_stereo_panning */
static void adapt_Music2_stereo_panning(ProbeState *s)
{ Music2_stereo_panning(s->stack[0], s->c); }
/* <<< factory Music2_stereo_panning */

/* >>> factory Music2_MainLoop */
static void adapt_Music2_MainLoop(ProbeState *s)
{ Music2_MainLoop(s->stack[0], s->c); }
/* <<< factory Music2_MainLoop */

/* >>> factory Music2_EndMainLoop */
static void adapt_Music2_EndMainLoop(ProbeState *s)
{ Music2_EndMainLoop(s->stack[0], s->c); }
/* <<< factory Music2_EndMainLoop */

/* >>> factory Music2_Loop */
static void adapt_Music2_Loop(ProbeState *s)
{ Music2_Loop(s->stack[0], s->c); }
/* <<< factory Music2_Loop */

/* >>> factory Music2_EndLoop */
static void adapt_Music2_EndLoop(ProbeState *s)
{ Music2_EndLoop(s->stack[0], s->c); }
/* <<< factory Music2_EndLoop */

/* >>> factory Music2_jp */
static void adapt_Music2_jp(ProbeState *s)
{ Music2_jp(s->stack[0], s->c); }
/* <<< factory Music2_jp */

/* >>> factory Music2_call */
static void adapt_Music2_call(ProbeState *s)
{ Music2_call(s->stack[0], s->c); }
/* <<< factory Music2_call */

/* >>> factory Music2_ret */
static void adapt_Music2_ret(ProbeState *s)
{ Music2_ret(s->stack[0], s->c); }
/* <<< factory Music2_ret */

/* >>> factory Music2_frequency_offset */
static void adapt_Music2_frequency_offset(ProbeState *s)
{ Music2_frequency_offset(s->stack[0], s->c); }
/* <<< factory Music2_frequency_offset */

/* >>> factory Music2_duty */
static void adapt_Music2_duty(ProbeState *s)
{ Music2_duty(s->stack[0], s->c); }
/* <<< factory Music2_duty */

/* >>> factory Music2_volume */
static void adapt_Music2_volume(ProbeState *s)
{ Music2_volume(s->stack[0], s->c); }
/* <<< factory Music2_volume */

/* >>> factory Music2_wave */
static void adapt_Music2_wave(ProbeState *s)
{ Music2_wave(s->stack[0], s->c); }
/* <<< factory Music2_wave */

/* >>> factory Music2_cutoff */
static void adapt_Music2_cutoff(ProbeState *s)
{ Music2_cutoff(s->stack[0], s->c); }
/* <<< factory Music2_cutoff */

/* >>> factory Music2_echo */
static void adapt_Music2_echo(ProbeState *s)
{ Music2_echo(s->stack[0], s->c); }
/* <<< factory Music2_echo */

/* >>> factory Music2_vibrato_type */
static void adapt_Music2_vibrato_type(ProbeState *s)
{ Music2_vibrato_type(s->stack[0], s->c); }
/* <<< factory Music2_vibrato_type */

/* >>> factory Music2_vibrato_delay */
static void adapt_Music2_vibrato_delay(ProbeState *s)
{ Music2_vibrato_delay(s->stack[0], s->c); }
/* <<< factory Music2_vibrato_delay */

/* >>> factory Music2_pitch_offset */
static void adapt_Music2_pitch_offset(ProbeState *s)
{ Music2_pitch_offset(s->stack[0], s->c); }
/* <<< factory Music2_pitch_offset */

/* >>> factory Music2_adjust_pitch_offset */
static void adapt_Music2_adjust_pitch_offset(ProbeState *s)
{ Music2_adjust_pitch_offset(s->stack[0], s->c); }
/* <<< factory Music2_adjust_pitch_offset */

/* >>> factory Music2_end */
static void adapt_Music2_end(ProbeState *s)
{ Music2_end(s->stack[0], s->c); }
/* <<< factory Music2_end */

/* >>> factory Music2_note */
static void adapt_Music2_note(ProbeState *s)
{ Music2_note(&s->hl, s->a, s->b, s->c); }
/* <<< factory Music2_note */

/* >>> factory Music2_f4714 */
/* ── Channel output ──────────────────────────────────────────────────── */

static void adapt_Music2_f4714(ProbeState *s)
{ (void)s; Music2_f4714(); }
/* <<< factory Music2_f4714 */

/* >>> factory Music2_f475a */
static void adapt_Music2_f475a(ProbeState *s)
{ (void)s; Music2_f475a(); }
/* <<< factory Music2_f475a */

/* >>> factory Music2_f479c */
static void adapt_Music2_f479c(ProbeState *s)
{ (void)s; Music2_f479c(); }
/* <<< factory Music2_f479c */

/* >>> factory Music2_f480a */
static void adapt_Music2_f480a(ProbeState *s)
{ (void)s; Music2_f480a(); }
/* <<< factory Music2_f480a */

/* >>> factory Music2_f4839 */
static void adapt_Music2_f4839(ProbeState *s)
{ (void)s; Music2_f4839(); }
/* <<< factory Music2_f4839 */

/* >>> factory Music2_f485a */
static void adapt_Music2_f485a(ProbeState *s)
{ Music2_f485a(s->a); }
/* <<< factory Music2_f485a */

/* >>> factory Music2_f4866 */
static void adapt_Music2_f4866(ProbeState *s)
{ (void)s; Music2_f4866(); }
/* <<< factory Music2_f4866 */

/* >>> factory Music2_LoadWaveInstrument */
static void adapt_Music2_LoadWaveInstrument(ProbeState *s)
{ (void)s; Music2_LoadWaveInstrument(); }
/* <<< factory Music2_LoadWaveInstrument */

/* >>> factory Music2_UpdateVibrato */
/* ── Vibrato ─────────────────────────────────────────────────────────── */

static void adapt_Music2_UpdateVibrato(ProbeState *s)
{
	uint16_t de = Music2_UpdateVibrato(s->c);

	s->e = (uint8_t)de;
	s->d = (uint8_t)(de >> 8);
}
/* <<< factory Music2_UpdateVibrato */

/* >>> factory Music2_f490b */
static void adapt_Music2_f490b(ProbeState *s)
{ Music2_f490b(s->a, (uint16_t)((uint16_t)s->d << 8 | s->e)); }
/* <<< factory Music2_f490b */

/* >>> factory Music2_f4967 */
static void adapt_Music2_f4967(ProbeState *s)
{
	uint16_t addr;
	uint8_t ch = s->c;
	addr = wMusicCh1CurPitch_ADDR + ((uint16_t)ch << 1);
	gb_write8(addr, s->e);
	gb_write8(addr + 1, s->d);
	Music2_f4967(ch);
	s->e = gb_read8(addr);
	s->d = gb_read8(addr + 1);
}
/* <<< factory Music2_f4967 */

/* >>> factory Music2_GetChannelStackPointer */
static void adapt_Music2_GetChannelStackPointer(ProbeState *s)
{
	uint16_t sp = Music2_GetChannelStackPointer(s->c);
	s->hl = sp;
}
/* <<< factory Music2_GetChannelStackPointer */

/* >>> factory Music2_SetChannelStackPointer */
static void adapt_Music2_SetChannelStackPointer(ProbeState *s)
{
	Music2_SetChannelStackPointer(s->c, s->hl);
}
/* <<< factory Music2_SetChannelStackPointer */

/* >>> factory Music2_PauseSong */
/* ── Pause / resume ──────────────────────────────────────────────────── */

static void adapt_Music2_PauseSong(ProbeState *s)
{ (void)s; Music2_PauseSong(); }
/* <<< factory Music2_PauseSong */

/* >>> factory Music2_ResumeSong */
static void adapt_Music2_ResumeSong(ProbeState *s)
{ (void)s; Music2_ResumeSong(); }
/* <<< factory Music2_ResumeSong */

/* >>> factory Music2_BackupSong */
static void adapt_Music2_BackupSong(ProbeState *s)
{ (void)s; Music2_BackupSong(); }
/* <<< factory Music2_BackupSong */

/* >>> factory Music2_LoadBackup */
static void adapt_Music2_LoadBackup(ProbeState *s)
{ (void)s; Music2_LoadBackup(); }
/* <<< factory Music2_LoadBackup */

/* >>> factory Music2_f400c_2 */
static void adapt_Music2_f400c_2(ProbeState *s)
{
	Music2_f400c_2(s->a);
}
/* <<< factory Music2_f400c_2 */

/* >>> factory Music2_f4018_2 */
static void adapt_Music2_f4018_2(ProbeState *s)
{
	Music2_f4018_2(s->a);
}
/* <<< factory Music2_f4018_2 */

/* >>> factory _AssertSFXFinished_2 */
static void adapt__AssertSFXFinished_2(ProbeState *s)
{
	s->a = _AssertSFXFinished_2();
}
/* <<< factory _AssertSFXFinished_2 */

/* >>> factory _AssertSongFinished_2 */
static void adapt__AssertSongFinished_2(ProbeState *s)
{
	s->a = _AssertSongFinished_2();
}
/* <<< factory _AssertSongFinished_2 */

/* >>> factory _PauseSong_2 */
static void adapt__PauseSong_2(ProbeState *s)
{
	(void)s;
	_PauseSong_2();
}
/* <<< factory _PauseSong_2 */

/* >>> factory _PlaySFX_2 */
static void adapt__PlaySFX_2(ProbeState *s)
{
	_PlaySFX_2(s->a);
}
/* <<< factory _PlaySFX_2 */

/* >>> factory _PlaySong_2 */
static void adapt__PlaySong_2(ProbeState *s)
{
	_PlaySong_2(s->a);
}
/* <<< factory _PlaySong_2 */

/* >>> factory _ResumeSong_2 */
static void adapt__ResumeSong_2(ProbeState *s)
{
	(void)s;
	_ResumeSong_2();
}
/* <<< factory _ResumeSong_2 */

/* >>> factory Music2_f4015_2 */
static void adapt_Music2_f4015_2(ProbeState *s)
{
	(void)s;
	Music2_f4015_2();
}
/* <<< factory Music2_f4015_2 */

/* >>> factory _SetupSound_2 */
static void adapt__SetupSound_2(ProbeState *s)
{
	(void)s;
	_SetupSound_2();
}
/* <<< factory _SetupSound_2 */

/* >>> factory SoundTimerHandler_2 */
static void adapt_SoundTimerHandler_2(ProbeState *s)
{
	(void)s;
	SoundTimerHandler_2();
}
/* <<< factory SoundTimerHandler_2 */

/* >>> factory Music2_PlayNextNote_pop */
static void adapt_Music2_PlayNextNote_pop(ProbeState *s)
{
	Music2_PlayNextNote_pop(s->stack[0], s->c);
}
/* <<< factory Music2_PlayNextNote_pop */

/* >>> part probe_entries_music2 */
const ProbeEntry probe_entries_music2[] = {
	{ "Music2_EmptyFunc",         adapt_Music2_EmptyFunc },
	{ "Music2_f404e",             adapt_Music2_f404e },
	{ "Music2_f4066",             adapt_Music2_f4066 },
	{ "Music2_f406f",             adapt_Music2_f406f },
	{ "Music2_PlaySong",          adapt_Music2_PlaySong },
	{ "Music2_PlaySFX",           adapt_Music2_PlaySFX },
	{ "Music2_AssertSongFinished", adapt_Music2_AssertSongFinished },
	{ "Music2_AssertSFXFinished", adapt_Music2_AssertSFXFinished },
	{ "Music2_CheckForEndOfSong", adapt_Music2_CheckForEndOfSong },
	{ "Music2_CheckForNewSound",  adapt_Music2_CheckForNewSound },
	{ "Music2_Init",              adapt_Music2_Init },
	{ "Music2_Update",            adapt_Music2_Update },
	{ "Music2_StopAllChannels",   adapt_Music2_StopAllChannels },
	{ "Music2_f4980",             adapt_Music2_f4980 },
	{ "Music2_BeginSong",         adapt_Music2_BeginSong },
	{ "Music2_CopyData",          adapt_Music2_CopyData },
	{ "Music2_UpdateChannel1",    adapt_Music2_UpdateChannel1 },
	{ "Music2_UpdateChannel2",    adapt_Music2_UpdateChannel2 },
	{ "Music2_UpdateChannel3",    adapt_Music2_UpdateChannel3 },
	{ "Music2_UpdateChannel4",    adapt_Music2_UpdateChannel4 },
	{ "Music2_PlayNextNote",      adapt_Music2_PlayNextNote },
	{ "Music2_speed",             adapt_Music2_speed },
	{ "Music2_octave",            adapt_Music2_octave },
	{ "Music2_inc_octave",        adapt_Music2_inc_octave },
	{ "Music2_dec_octave",        adapt_Music2_dec_octave },
	{ "Music2_tie",               adapt_Music2_tie },
	{ "Music2_stereo_panning",    adapt_Music2_stereo_panning },
	{ "Music2_MainLoop",          adapt_Music2_MainLoop },
	{ "Music2_EndMainLoop",       adapt_Music2_EndMainLoop },
	{ "Music2_Loop",              adapt_Music2_Loop },
	{ "Music2_EndLoop",           adapt_Music2_EndLoop },
	{ "Music2_jp",                adapt_Music2_jp },
	{ "Music2_call",              adapt_Music2_call },
	{ "Music2_ret",               adapt_Music2_ret },
	{ "Music2_frequency_offset",  adapt_Music2_frequency_offset },
	{ "Music2_duty",              adapt_Music2_duty },
	{ "Music2_volume",            adapt_Music2_volume },
	{ "Music2_wave",              adapt_Music2_wave },
	{ "Music2_cutoff",            adapt_Music2_cutoff },
	{ "Music2_echo",              adapt_Music2_echo },
	{ "Music2_vibrato_type",      adapt_Music2_vibrato_type },
	{ "Music2_vibrato_delay",     adapt_Music2_vibrato_delay },
	{ "Music2_pitch_offset",      adapt_Music2_pitch_offset },
	{ "Music2_adjust_pitch_offset", adapt_Music2_adjust_pitch_offset },
	{ "Music2_end",               adapt_Music2_end },
	{ "Music2_note",              adapt_Music2_note },
	{ "Music2_f4714",             adapt_Music2_f4714 },
	{ "Music2_f475a",             adapt_Music2_f475a },
	{ "Music2_f479c",             adapt_Music2_f479c },
	{ "Music2_f480a",             adapt_Music2_f480a },
	{ "Music2_f4839",             adapt_Music2_f4839 },
	{ "Music2_f485a",             adapt_Music2_f485a },
	{ "Music2_f4866",             adapt_Music2_f4866 },
	{ "Music2_LoadWaveInstrument", adapt_Music2_LoadWaveInstrument },
	{ "Music2_UpdateVibrato",     adapt_Music2_UpdateVibrato },
	{ "Music2_f490b",             adapt_Music2_f490b },
	{ "Music2_f4967",             adapt_Music2_f4967 },
	{ "Music2_PauseSong",         adapt_Music2_PauseSong },
	{ "Music2_ResumeSong",        adapt_Music2_ResumeSong },
	{ "Music2_BackupSong",        adapt_Music2_BackupSong },
	{ "Music2_LoadBackup",        adapt_Music2_LoadBackup },
	{ "Music2_GetChannelStackPointer", adapt_Music2_GetChannelStackPointer },
	{ "Music2_SetChannelStackPointer", adapt_Music2_SetChannelStackPointer },
	{ "Music2_f400c_2", adapt_Music2_f400c_2 },
	{ "Music2_f4018_2", adapt_Music2_f4018_2 },
	{ "_AssertSFXFinished_2", adapt__AssertSFXFinished_2 },
	{ "_AssertSongFinished_2", adapt__AssertSongFinished_2 },
	{ "_PauseSong_2", adapt__PauseSong_2 },
	{ "_PlaySFX_2", adapt__PlaySFX_2 },
	{ "_PlaySong_2", adapt__PlaySong_2 },
	{ "_ResumeSong_2", adapt__ResumeSong_2 },
	{ "Music2_f4015_2", adapt_Music2_f4015_2 },
	{ "_SetupSound_2", adapt__SetupSound_2 },
	{ "SoundTimerHandler_2", adapt_SoundTimerHandler_2 },
	{ "Music2_PlayNextNote_pop", adapt_Music2_PlayNextNote_pop },
	{ NULL, NULL },
};
/* <<< part probe_entries_music2 */
