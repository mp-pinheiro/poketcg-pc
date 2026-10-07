/* >>> part includes */
#include "home/sound.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory SetupSound */
static void adapt_SetupSound(ProbeState *s)
{
	(void)s;
	SetupSound();
}
/* <<< factory SetupSound */

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
const ProbeEntry probe_entries_sound[] = {
	{ "SetupSound", adapt_SetupSound },
	{ "PlaySong", adapt_PlaySong },
	{ "AssertSongFinished", adapt_AssertSongFinished },
	{ "AssertSFXFinished", adapt_AssertSFXFinished },
	{ "PlaySFX_InvalidChoice", adapt_PlaySFX_InvalidChoice },
	{ "PlaySFX", adapt_PlaySFX },
	{ "PauseSong", adapt_PauseSong },
	{ "ResumeSong", adapt_ResumeSong },
	{ NULL, NULL },
};
/* <<< part probe_entries_sound */
