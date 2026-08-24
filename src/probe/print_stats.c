#include "home/print_stats.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory DrawPauseMenuPlayerPortrait */
static void adapt_DrawPauseMenuPlayerPortrait(ProbeState *s)
{
	(void)s;
	DrawPauseMenuPlayerPortrait();
}
/* <<< factory DrawPauseMenuPlayerPortrait */

/* >>> factory FlashReceivedMedal */
static void adapt_FlashReceivedMedal(ProbeState *s)
{
	(void)s;
	FlashReceivedMedal();
}
/* <<< factory FlashReceivedMedal */

/* >>> factory ConvertWordToNumericalDigits */
static void adapt_ConvertWordToNumericalDigits(ProbeState *s)
{
	ConvertWordToNumericalDigitsResult r = ConvertWordToNumericalDigits(s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory ConvertWordToNumericalDigits */

/* >>> factory PrintAlbumProgress_SkipGetProgress */
static void adapt_PrintAlbumProgress_SkipGetProgress(ProbeState *s)
{
	PrintAlbumProgress_SkipGetProgress(s->b, s->c, s->d, s->e);
}
/* <<< factory PrintAlbumProgress_SkipGetProgress */

const ProbeEntry probe_entries_print_stats[] = {
	{ "DrawPauseMenuPlayerPortrait", adapt_DrawPauseMenuPlayerPortrait },
	{ "FlashReceivedMedal", adapt_FlashReceivedMedal },
	{ "ConvertWordToNumericalDigits", adapt_ConvertWordToNumericalDigits },
	{ "PrintAlbumProgress_SkipGetProgress", adapt_PrintAlbumProgress_SkipGetProgress },
	{ NULL, NULL },
};
