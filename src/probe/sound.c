/* >>> part includes */
#include "home/sound.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory Func_37c5 */
static void adapt_Func_37c5(ProbeState *s)
{
	uint8_t carry_in = (uint8_t)((s->f & 0x10u) ? 1u : 0u);
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	TileConvertResult r = Func_37c5(s->hl, de, s->a, carry_in);
	s->hl = r.hl;
	s->a = r.a;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory Func_37c5 */

/* >>> factory Func_37a5 */
static void adapt_Func_37a5(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	TileConvertWrapResult r = Func_37a5(s->hl, de);
	s->hl = r.hl;
	s->a = r.a;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory Func_37a5 */

/* >>> part SetupSound */
static void adapt_SetupSound(ProbeState *s) { (void)s; SetupSound(); }
/* <<< part SetupSound */
/* >>> part StopMusic */
static void adapt_StopMusic(ProbeState *s) { (void)s; StopMusic(); }
/* <<< part StopMusic */
/* >>> part PlaySong */
static void adapt_PlaySong(ProbeState *s) { PlaySong(s->a); }
/* <<< part PlaySong */
/* >>> part AssertSongFinished */
static void adapt_AssertSongFinished(ProbeState *s) { s->a = AssertSongFinished(); }
/* <<< part AssertSongFinished */
/* >>> part AssertSFXFinished */
static void adapt_AssertSFXFinished(ProbeState *s) { s->a = AssertSFXFinished(); }
/* <<< part AssertSFXFinished */
/* >>> part PlaySFX_InvalidChoice */
static void adapt_PlaySFX_InvalidChoice(ProbeState *s) { (void)s; PlaySFX_InvalidChoice(); }
/* <<< part PlaySFX_InvalidChoice */
/* >>> part PlaySFX */
static void adapt_PlaySFX(ProbeState *s) { PlaySFX(s->a); }
/* <<< part PlaySFX */
/* >>> part PauseSong */
static void adapt_PauseSong(ProbeState *s) { (void)s; PauseSong(); }
/* <<< part PauseSong */
/* >>> part ResumeSong */
static void adapt_ResumeSong(ProbeState *s) { (void)s; ResumeSong(); }
/* <<< part ResumeSong */

/* >>> part probe_entries_sound */
const ProbeEntry probe_entries_sound[] = {
	{ "Func_37c5", adapt_Func_37c5 },
	{ "Func_37a5", adapt_Func_37a5 },
	{ "SetupSound", adapt_SetupSound },
	{ "StopMusic", adapt_StopMusic },
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
