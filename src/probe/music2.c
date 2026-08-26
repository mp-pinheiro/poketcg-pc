#include "home/music2.h"
#include "probe.h"
#include "mem.h"
#include "generated/wram.h"

/* ── Leaf adapters ───────────────────────────────────────────────────── */

static void adapt_Music2_EmptyFunc(ProbeState *s)
{ (void)s; Music2_EmptyFunc(); }

static void adapt_Music2_f404e(ProbeState *s)
{ Music2_f404e(s->a); }

static void adapt_Music2_f4066(ProbeState *s)
{ (void)s; Music2_f4066(); }

static void adapt_Music2_f406f(ProbeState *s)
{ Music2_f406f(s->a); }

static void adapt_Music2_PlaySong(ProbeState *s)
{ Music2_PlaySong(s->a); }

static void adapt_Music2_PlaySFX(ProbeState *s)
{ Music2_PlaySFX(s->a); }

static void adapt_Music2_AssertSongFinished(ProbeState *s)
{ s->a = Music2_AssertSongFinished(); }

static void adapt_Music2_AssertSFXFinished(ProbeState *s)
{ s->a = Music2_AssertSFXFinished(); }

static void adapt_Music2_CheckForEndOfSong(ProbeState *s)
{ (void)s; Music2_CheckForEndOfSong(); }

static void adapt_Music2_CheckForNewSound(ProbeState *s)
{ (void)s; Music2_CheckForNewSound(); }

static void adapt_Music2_Init(ProbeState *s)
{ (void)s; Music2_Init(); }

static void adapt_Music2_Update(ProbeState *s)
{ (void)s; Music2_Update(); }

static void adapt_Music2_StopAllChannels(ProbeState *s)
{ (void)s; Music2_StopAllChannels(); }

static void adapt_Music2_f4980(ProbeState *s)
{ (void)s; Music2_f4980(); }

static void adapt_Music2_BeginSong(ProbeState *s)
{ Music2_BeginSong(s->a); }

static void adapt_Music2_CopyData(ProbeState *s)
{
	uint16_t de = (uint16_t)s->d << 8 | s->e;
	Music2_CopyData(&s->hl, &de, s->a);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

/* ── Channel updaters ────────────────────────────────────────────────── */

static void adapt_Music2_UpdateChannel1(ProbeState *s)
{ (void)s; Music2_UpdateChannel1(); }

static void adapt_Music2_UpdateChannel2(ProbeState *s)
{ (void)s; Music2_UpdateChannel2(); }

static void adapt_Music2_UpdateChannel3(ProbeState *s)
{ (void)s; Music2_UpdateChannel3(); }

static void adapt_Music2_UpdateChannel4(ProbeState *s)
{ (void)s; Music2_UpdateChannel4(); }

/* ── PlayNextNote ────────────────────────────────────────────────────── */

static void adapt_Music2_PlayNextNote(ProbeState *s)
/* music2.asm:578 `ld a,[hli]` overwrites a immediately; the channel arrives in
 * c, which every handler indexes with `add hl, bc`. */
{ Music2_PlayNextNote(&s->hl, s->c); }

/* ── Command handlers ────────────────────────────────────────────────── */

static void adapt_Music2_speed(ProbeState *s)
{ Music2_speed(s->stack[0], s->c); }

static void adapt_Music2_octave(ProbeState *s)
{ Music2_octave(s->stack[0], s->c, s->a); }

static void adapt_Music2_inc_octave(ProbeState *s)
{ Music2_inc_octave(s->stack[0], s->c); }

static void adapt_Music2_dec_octave(ProbeState *s)
{ Music2_dec_octave(s->stack[0], s->c); }

static void adapt_Music2_tie(ProbeState *s)
{ Music2_tie(s->stack[0], s->c); }

static void adapt_Music2_stereo_panning(ProbeState *s)
{ Music2_stereo_panning(s->stack[0], s->c); }

static void adapt_Music2_MainLoop(ProbeState *s)
{ Music2_MainLoop(s->stack[0], s->c); }

static void adapt_Music2_EndMainLoop(ProbeState *s)
{ Music2_EndMainLoop(s->stack[0], s->c); }

static void adapt_Music2_Loop(ProbeState *s)
{ Music2_Loop(s->stack[0], s->c); }

static void adapt_Music2_EndLoop(ProbeState *s)
{ Music2_EndLoop(s->stack[0], s->c); }

static void adapt_Music2_jp(ProbeState *s)
{ Music2_jp(s->stack[0], s->c); }

static void adapt_Music2_call(ProbeState *s)
{ Music2_call(s->stack[0], s->c); }

static void adapt_Music2_ret(ProbeState *s)
{ Music2_ret(s->stack[0], s->c); }

static void adapt_Music2_frequency_offset(ProbeState *s)
{ Music2_frequency_offset(s->stack[0], s->c); }

static void adapt_Music2_duty(ProbeState *s)
{ Music2_duty(s->stack[0], s->c); }

static void adapt_Music2_volume(ProbeState *s)
{ Music2_volume(s->stack[0], s->c); }

static void adapt_Music2_wave(ProbeState *s)
{ Music2_wave(s->stack[0], s->c); }

static void adapt_Music2_cutoff(ProbeState *s)
{ Music2_cutoff(s->stack[0], s->c); }

static void adapt_Music2_echo(ProbeState *s)
{ Music2_echo(s->stack[0], s->c); }

static void adapt_Music2_vibrato_type(ProbeState *s)
{ Music2_vibrato_type(s->stack[0], s->c); }

static void adapt_Music2_vibrato_delay(ProbeState *s)
{ Music2_vibrato_delay(s->stack[0], s->c); }

static void adapt_Music2_pitch_offset(ProbeState *s)
{ Music2_pitch_offset(s->stack[0], s->c); }

static void adapt_Music2_adjust_pitch_offset(ProbeState *s)
{ Music2_adjust_pitch_offset(s->stack[0], s->c); }

static void adapt_Music2_end(ProbeState *s)
{ Music2_end(s->stack[0], s->c); }

static void adapt_Music2_note(ProbeState *s)
{ Music2_note(&s->hl, s->a, s->b, s->c); }

/* ── Channel output ──────────────────────────────────────────────────── */

static void adapt_Music2_f4714(ProbeState *s)
{ (void)s; Music2_f4714(); }

static void adapt_Music2_f475a(ProbeState *s)
{ (void)s; Music2_f475a(); }

static void adapt_Music2_f479c(ProbeState *s)
{ (void)s; Music2_f479c(); }

static void adapt_Music2_f480a(ProbeState *s)
{ (void)s; Music2_f480a(); }

static void adapt_Music2_f4839(ProbeState *s)
{ (void)s; Music2_f4839(); }

static void adapt_Music2_f485a(ProbeState *s)
{ Music2_f485a(s->a); }

static void adapt_Music2_f4866(ProbeState *s)
{ (void)s; Music2_f4866(); }

static void adapt_Music2_LoadWaveInstrument(ProbeState *s)
{ (void)s; Music2_LoadWaveInstrument(); }

/* ── Vibrato ─────────────────────────────────────────────────────────── */

static void adapt_Music2_UpdateVibrato(ProbeState *s)
{
	uint8_t ch = s->c;
	Music2_UpdateVibrato(ch);
	s->e = gb_read8(wMusicCh1CurPitch_ADDR + ((uint16_t)ch << 1));
	s->d = gb_read8(wMusicCh1CurPitch_ADDR + ((uint16_t)ch << 1) + 1);
}

static void adapt_Music2_f490b(ProbeState *s)
{ Music2_f490b(s->a); }

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

static void adapt_Music2_GetChannelStackPointer(ProbeState *s)
{
	uint16_t sp = Music2_GetChannelStackPointer(s->c);
	s->hl = sp;
}

static void adapt_Music2_SetChannelStackPointer(ProbeState *s)
{
	Music2_SetChannelStackPointer(s->c, s->hl);
}

/* ── Pause / resume ──────────────────────────────────────────────────── */

static void adapt_Music2_PauseSong(ProbeState *s)
{ (void)s; Music2_PauseSong(); }

static void adapt_Music2_ResumeSong(ProbeState *s)
{ (void)s; Music2_ResumeSong(); }

static void adapt_Music2_BackupSong(ProbeState *s)
{ (void)s; Music2_BackupSong(); }

static void adapt_Music2_LoadBackup(ProbeState *s)
{ (void)s; Music2_LoadBackup(); }

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
	_SetupSound_2();
}
/* <<< factory _SetupSound_2 */

/* >>> factory SoundTimerHandler_2 */
static void adapt_SoundTimerHandler_2(ProbeState *s)
{
	SoundTimerHandler_2();
}
/* <<< factory SoundTimerHandler_2 */

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
	{ NULL, NULL },
};
