#include "home/music1.h"
#include "probe.h"
#include "mem.h"
#include "generated/wram.h"

/* ── Leaf adapters ───────────────────────────────────────────────────── */

static void adapt_Music1_EmptyFunc(ProbeState *s)
{ (void)s; Music1_EmptyFunc(); }

static void adapt_Music1_f404e(ProbeState *s)
{ Music1_f404e(s->a); }

static void adapt_Music1_f4066(ProbeState *s)
{ (void)s; Music1_f4066(); }

static void adapt_Music1_f406f(ProbeState *s)
{ Music1_f406f(s->a); }

static void adapt_Music1_PlaySong(ProbeState *s)
{ Music1_PlaySong(s->a); }

static void adapt_Music1_PlaySFX(ProbeState *s)
{ Music1_PlaySFX(s->a); }

static void adapt_Music1_AssertSongFinished(ProbeState *s)
{ s->a = Music1_AssertSongFinished(); }

static void adapt_Music1_AssertSFXFinished(ProbeState *s)
{ s->a = Music1_AssertSFXFinished(); }

static void adapt_Music1_CheckForEndOfSong(ProbeState *s)
{ (void)s; Music1_CheckForEndOfSong(); }

static void adapt_Music1_CheckForNewSound(ProbeState *s)
{ (void)s; Music1_CheckForNewSound(); }

static void adapt_Music1_Init(ProbeState *s)
{ (void)s; Music1_Init(); }

static void adapt_Music1_Update(ProbeState *s)
{ (void)s; Music1_Update(); }

static void adapt_Music1_StopAllChannels(ProbeState *s)
{ (void)s; Music1_StopAllChannels(); }

static void adapt_Music1_f4980(ProbeState *s)
{ (void)s; Music1_f4980(); }

static void adapt_Music1_BeginSong(ProbeState *s)
{ Music1_BeginSong(s->a); }

static void adapt_Music1_CopyData(ProbeState *s)
{
	uint16_t de = (uint16_t)s->d << 8 | s->e;
	Music1_CopyData(&s->hl, &de, s->a);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

/* ── Channel updaters ────────────────────────────────────────────────── */

static void adapt_Music1_UpdateChannel1(ProbeState *s)
{ (void)s; Music1_UpdateChannel1(); }

static void adapt_Music1_UpdateChannel2(ProbeState *s)
{ (void)s; Music1_UpdateChannel2(); }

static void adapt_Music1_UpdateChannel3(ProbeState *s)
{ (void)s; Music1_UpdateChannel3(); }

static void adapt_Music1_UpdateChannel4(ProbeState *s)
{ (void)s; Music1_UpdateChannel4(); }

/* ── PlayNextNote ────────────────────────────────────────────────────── */

static void adapt_Music1_PlayNextNote(ProbeState *s)
{ Music1_PlayNextNote(&s->hl, s->a); }

/* ── Command handlers ────────────────────────────────────────────────── */

static void adapt_Music1_speed(ProbeState *s)
{ Music1_speed(s->stack[0], s->c); }

static void adapt_Music1_octave(ProbeState *s)
{ Music1_octave(&s->hl, s->a, s->b); }

static void adapt_Music1_inc_octave(ProbeState *s)
{ Music1_inc_octave(s->stack[0], s->c); }

static void adapt_Music1_dec_octave(ProbeState *s)
{ Music1_dec_octave(s->stack[0], s->c); }

static void adapt_Music1_tie(ProbeState *s)
{ Music1_tie(s->stack[0], s->c); }

static void adapt_Music1_stereo_panning(ProbeState *s)
{ Music1_stereo_panning(s->stack[0], s->c); }

static void adapt_Music1_MainLoop(ProbeState *s)
{ Music1_MainLoop(s->stack[0], s->c); }

static void adapt_Music1_EndMainLoop(ProbeState *s)
{ Music1_EndMainLoop(s->stack[0], s->c); }

static void adapt_Music1_Loop(ProbeState *s)
{ Music1_Loop(s->stack[0], s->c); }

static void adapt_Music1_EndLoop(ProbeState *s)
{ Music1_EndLoop(s->stack[0], s->c); }

static void adapt_Music1_jp(ProbeState *s)
{ Music1_jp(s->stack[0], s->c); }

static void adapt_Music1_call(ProbeState *s)
{ Music1_call(&s->hl, s->a); }

static void adapt_Music1_ret(ProbeState *s)
{ Music1_ret(&s->hl, s->a); }

static void adapt_Music1_frequency_offset(ProbeState *s)
{ Music1_frequency_offset(&s->hl, s->a); }

static void adapt_Music1_duty(ProbeState *s)
{ Music1_duty(s->stack[0], s->c); }

static void adapt_Music1_volume(ProbeState *s)
{ Music1_volume(&s->hl, s->a); }

static void adapt_Music1_wave(ProbeState *s)
{ Music1_wave(&s->hl, s->a); }

static void adapt_Music1_cutoff(ProbeState *s)
{ Music1_cutoff(&s->hl, s->a); }

static void adapt_Music1_echo(ProbeState *s)
{ Music1_echo(&s->hl, s->a); }

static void adapt_Music1_vibrato_type(ProbeState *s)
{ Music1_vibrato_type(&s->hl, s->a); }

static void adapt_Music1_vibrato_delay(ProbeState *s)
{ Music1_vibrato_delay(&s->hl, s->a); }

static void adapt_Music1_pitch_offset(ProbeState *s)
{ Music1_pitch_offset(&s->hl, s->a); }

static void adapt_Music1_adjust_pitch_offset(ProbeState *s)
{ Music1_adjust_pitch_offset(&s->hl, s->a); }

static void adapt_Music1_end(ProbeState *s)
{ Music1_end(&s->hl, s->a); }

static void adapt_Music1_note(ProbeState *s)
{ Music1_note(&s->hl, s->a, s->b, s->c); }

/* ── Channel output ──────────────────────────────────────────────────── */

static void adapt_Music1_f4714(ProbeState *s)
{ (void)s; Music1_f4714(); }

static void adapt_Music1_f475a(ProbeState *s)
{ (void)s; Music1_f475a(); }

static void adapt_Music1_f479c(ProbeState *s)
{ (void)s; Music1_f479c(); }

static void adapt_Music1_f480a(ProbeState *s)
{ (void)s; Music1_f480a(); }

static void adapt_Music1_f4839(ProbeState *s)
{ (void)s; Music1_f4839(); }

static void adapt_Music1_f485a(ProbeState *s)
{ Music1_f485a(s->a); }

static void adapt_Music1_f4866(ProbeState *s)
{ (void)s; Music1_f4866(); }

static void adapt_Music1_LoadWaveInstrument(ProbeState *s)
{ (void)s; Music1_LoadWaveInstrument(); }

/* ── Vibrato ─────────────────────────────────────────────────────────── */

static void adapt_Music1_UpdateVibrato(ProbeState *s)
{
	uint8_t ch = s->c;
	Music1_UpdateVibrato(ch);
	s->e = gb_read8(wMusicCh1CurPitch_ADDR + ((uint16_t)ch << 1));
	s->d = gb_read8(wMusicCh1CurPitch_ADDR + ((uint16_t)ch << 1) + 1);
}

static void adapt_Music1_f490b(ProbeState *s)
{ Music1_f490b(s->a); }

static void adapt_Music1_f4967(ProbeState *s)
{
	uint16_t addr;
	uint8_t ch = s->c;
	addr = wMusicCh1CurPitch_ADDR + ((uint16_t)ch << 1);
	gb_write8(addr, s->e);
	gb_write8(addr + 1, s->d);
	Music1_f4967(ch);
	s->e = gb_read8(addr);
	s->d = gb_read8(addr + 1);
}

static void adapt_Music1_GetChannelStackPointer(ProbeState *s)
{
	uint16_t sp = Music1_GetChannelStackPointer(s->c);
	s->hl = sp;
}

static void adapt_Music1_SetChannelStackPointer(ProbeState *s)
{
	Music1_SetChannelStackPointer(s->c, s->hl);
}

/* ── Pause / resume ──────────────────────────────────────────────────── */

static void adapt_Music1_PauseSong(ProbeState *s)
{ (void)s; Music1_PauseSong(); }

static void adapt_Music1_ResumeSong(ProbeState *s)
{ (void)s; Music1_ResumeSong(); }

static void adapt_Music1_BackupSong(ProbeState *s)
{ (void)s; Music1_BackupSong(); }

static void adapt_Music1_LoadBackup(ProbeState *s)
{ (void)s; Music1_LoadBackup(); }

/* >>> factory _PauseSong */
static void adapt__PauseSong(ProbeState *s)
{
	(void)s;
	_PauseSong();
}
/* <<< factory _PauseSong */

/* >>> factory _ResumeSong */
static void adapt__ResumeSong(ProbeState *s)
{
	(void)s;
	_ResumeSong();
}
/* <<< factory _ResumeSong */

/* >>> factory Music1_f400c */
static void adapt_Music1_f400c(ProbeState *s)
{
	Music1_f400c(s->a);
}
/* <<< factory Music1_f400c */

/* >>> factory Music1_f4018 */
static void adapt_Music1_f4018(ProbeState *s)
{
	Music1_f4018(s->a);
}
/* <<< factory Music1_f4018 */

/* >>> factory _AssertSFXFinished */
static void adapt__AssertSFXFinished(ProbeState *s)
{
	s->a = _AssertSFXFinished();
}
/* <<< factory _AssertSFXFinished */

/* >>> factory _AssertSongFinished */
static void adapt__AssertSongFinished(ProbeState *s)
{
	s->a = _AssertSongFinished();
}
/* <<< factory _AssertSongFinished */

/* >>> factory _PlaySFX */
static void adapt__PlaySFX(ProbeState *s)
{
	_PlaySFX(s->a);
}
/* <<< factory _PlaySFX */

/* >>> factory _PlaySong */
static void adapt__PlaySong(ProbeState *s)
{
	_PlaySong(s->a);
}
/* <<< factory _PlaySong */

/* >>> factory _SetupSound */
static void adapt__SetupSound(ProbeState *s)
{
	_SetupSound();
}
/* <<< factory _SetupSound */

/* >>> factory SoundTimerHandler */
static void adapt_SoundTimerHandler(ProbeState *s)
{
	(void)s;
	SoundTimerHandler();
}
/* <<< factory SoundTimerHandler */

/* >>> factory Music1_f4015 */
static void adapt_Music1_f4015(ProbeState *s)
{
	(void)s;
	Music1_f4015();
}
/* <<< factory Music1_f4015 */

const ProbeEntry probe_entries_music1[] = {
	{ "Music1_EmptyFunc",         adapt_Music1_EmptyFunc },
	{ "Music1_f404e",             adapt_Music1_f404e },
	{ "Music1_f4066",             adapt_Music1_f4066 },
	{ "Music1_f406f",             adapt_Music1_f406f },
	{ "Music1_PlaySong",          adapt_Music1_PlaySong },
	{ "Music1_PlaySFX",           adapt_Music1_PlaySFX },
	{ "Music1_AssertSongFinished", adapt_Music1_AssertSongFinished },
	{ "Music1_AssertSFXFinished", adapt_Music1_AssertSFXFinished },
	{ "Music1_CheckForEndOfSong", adapt_Music1_CheckForEndOfSong },
	{ "Music1_CheckForNewSound",  adapt_Music1_CheckForNewSound },
	{ "Music1_Init",              adapt_Music1_Init },
	{ "Music1_Update",            adapt_Music1_Update },
	{ "Music1_StopAllChannels",   adapt_Music1_StopAllChannels },
	{ "Music1_f4980",             adapt_Music1_f4980 },
	{ "Music1_BeginSong",         adapt_Music1_BeginSong },
	{ "Music1_CopyData",          adapt_Music1_CopyData },
	{ "Music1_UpdateChannel1",    adapt_Music1_UpdateChannel1 },
	{ "Music1_UpdateChannel2",    adapt_Music1_UpdateChannel2 },
	{ "Music1_UpdateChannel3",    adapt_Music1_UpdateChannel3 },
	{ "Music1_UpdateChannel4",    adapt_Music1_UpdateChannel4 },
	{ "Music1_PlayNextNote",      adapt_Music1_PlayNextNote },
	{ "Music1_speed",             adapt_Music1_speed },
	{ "Music1_octave",            adapt_Music1_octave },
	{ "Music1_inc_octave",        adapt_Music1_inc_octave },
	{ "Music1_dec_octave",        adapt_Music1_dec_octave },
	{ "Music1_tie",               adapt_Music1_tie },
	{ "Music1_stereo_panning",    adapt_Music1_stereo_panning },
	{ "Music1_MainLoop",          adapt_Music1_MainLoop },
	{ "Music1_EndMainLoop",       adapt_Music1_EndMainLoop },
	{ "Music1_Loop",              adapt_Music1_Loop },
	{ "Music1_EndLoop",           adapt_Music1_EndLoop },
	{ "Music1_jp",                adapt_Music1_jp },
	{ "Music1_call",              adapt_Music1_call },
	{ "Music1_ret",               adapt_Music1_ret },
	{ "Music1_frequency_offset",  adapt_Music1_frequency_offset },
	{ "Music1_duty",              adapt_Music1_duty },
	{ "Music1_volume",            adapt_Music1_volume },
	{ "Music1_wave",              adapt_Music1_wave },
	{ "Music1_cutoff",            adapt_Music1_cutoff },
	{ "Music1_echo",              adapt_Music1_echo },
	{ "Music1_vibrato_type",      adapt_Music1_vibrato_type },
	{ "Music1_vibrato_delay",     adapt_Music1_vibrato_delay },
	{ "Music1_pitch_offset",      adapt_Music1_pitch_offset },
	{ "Music1_adjust_pitch_offset", adapt_Music1_adjust_pitch_offset },
	{ "Music1_end",               adapt_Music1_end },
	{ "Music1_note",              adapt_Music1_note },
	{ "Music1_f4714",             adapt_Music1_f4714 },
	{ "Music1_f475a",             adapt_Music1_f475a },
	{ "Music1_f479c",             adapt_Music1_f479c },
	{ "Music1_f480a",             adapt_Music1_f480a },
	{ "Music1_f4839",             adapt_Music1_f4839 },
	{ "Music1_f485a",             adapt_Music1_f485a },
	{ "Music1_f4866",             adapt_Music1_f4866 },
	{ "Music1_LoadWaveInstrument", adapt_Music1_LoadWaveInstrument },
	{ "Music1_UpdateVibrato",     adapt_Music1_UpdateVibrato },
	{ "Music1_f490b",             adapt_Music1_f490b },
	{ "Music1_f4967",             adapt_Music1_f4967 },
	{ "Music1_PauseSong",         adapt_Music1_PauseSong },
	{ "Music1_ResumeSong",        adapt_Music1_ResumeSong },
	{ "Music1_BackupSong",        adapt_Music1_BackupSong },
	{ "Music1_LoadBackup",        adapt_Music1_LoadBackup },
	{ "Music1_GetChannelStackPointer", adapt_Music1_GetChannelStackPointer },
	{ "Music1_SetChannelStackPointer", adapt_Music1_SetChannelStackPointer },
	{ "_PauseSong", adapt__PauseSong },
	{ "_ResumeSong", adapt__ResumeSong },
	{ "Music1_f400c", adapt_Music1_f400c },
	{ "Music1_f4018", adapt_Music1_f4018 },
	{ "_AssertSFXFinished", adapt__AssertSFXFinished },
	{ "_AssertSongFinished", adapt__AssertSongFinished },
	{ "_PlaySFX", adapt__PlaySFX },
	{ "_PlaySong", adapt__PlaySong },
	{ "_SetupSound", adapt__SetupSound },
	{ "SoundTimerHandler", adapt_SoundTimerHandler },
	{ "Music1_f4015", adapt_Music1_f4015 },
	{ NULL, NULL },
};
