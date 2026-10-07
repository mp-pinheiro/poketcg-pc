/* --- factory Func_37c5 */
/* --- factory Func_37a5 */
/* >>> factory SetupSound */
static void adapt_SetupSound(ProbeState *s)
{
	(void)s;
	SetupSound();
}
/* <<< factory SetupSound */
/* --- part StopMusic */
/* >>> factory PlaySong */
static void adapt_PlaySong(ProbeState *s)
{
	PlaySong(s->a);
}
/* <<< factory PlaySong */
/* >>> factory AssertSongFinished */
static void adapt_AssertSongFinished(ProbeState *s)
{
	s->a = AssertSongFinished();
}
/* <<< factory AssertSongFinished */
/* >>> factory AssertSFXFinished */
static void adapt_AssertSFXFinished(ProbeState *s)
{
	s->a = AssertSFXFinished();
}
/* <<< factory AssertSFXFinished */
/* >>> factory PlaySFX_InvalidChoice */
static void adapt_PlaySFX_InvalidChoice(ProbeState *s)
{
	(void)s;
	PlaySFX_InvalidChoice();
}
/* <<< factory PlaySFX_InvalidChoice */
/* >>> factory PlaySFX */
static void adapt_PlaySFX(ProbeState *s)
{
	PlaySFX(s->a);
}
/* <<< factory PlaySFX */
/* >>> factory PauseSong */
static void adapt_PauseSong(ProbeState *s)
{
	(void)s;
	PauseSong();
}
/* <<< factory PauseSong */
/* >>> factory ResumeSong */
static void adapt_ResumeSong(ProbeState *s)
{
	(void)s;
	ResumeSong();
}
/* <<< factory ResumeSong */
/* >>> part probe_entries_sound */
/* <<< part probe_entries_sound */
