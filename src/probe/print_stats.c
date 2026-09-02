#include "home/print_stats.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory DrawPauseMenuPlayerPortrait */
static void adapt_DrawPauseMenuPlayerPortrait(ProbeState *s)
{
	DrawPauseMenuPlayerPortrait(s->b, s->c);
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

/* >>> factory PrintPlayTime_SkipUpdateTime */
static void adapt_PrintPlayTime_SkipUpdateTime(ProbeState *s)
{
	PrintPlayTime_SkipUpdateTime(s->b, s->c);
}
/* <<< factory PrintPlayTime_SkipUpdateTime */

/* >>> factory PrintAlbumProgress */
static void adapt_PrintAlbumProgress(ProbeState *s)
{
	PrintAlbumProgress(s->b, s->c);
}
/* <<< factory PrintAlbumProgress */

/* >>> factory PrintPlayTime */
static void adapt_PrintPlayTime(ProbeState *s)
{
	PrintPlayTime(s->b, s->c);
}
/* <<< factory PrintPlayTime */

/* >>> factory PrintMedalCount */
static void adapt_PrintMedalCount(ProbeState *s)
{
	PrintMedalCount(s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory PrintMedalCount */

/* >>> factory DrawCollectedMedals */
static void adapt_DrawCollectedMedals(ProbeState *s)
{
	DrawCollectedMedals();
}
/* <<< factory DrawCollectedMedals */

const ProbeEntry probe_entries_print_stats[] = {
	{ "DrawPauseMenuPlayerPortrait", adapt_DrawPauseMenuPlayerPortrait },
	{ "FlashReceivedMedal", adapt_FlashReceivedMedal },
	{ "ConvertWordToNumericalDigits", adapt_ConvertWordToNumericalDigits },
	{ "PrintAlbumProgress_SkipGetProgress", adapt_PrintAlbumProgress_SkipGetProgress },
	{ "PrintPlayTime_SkipUpdateTime", adapt_PrintPlayTime_SkipUpdateTime },
	{ "PrintAlbumProgress", adapt_PrintAlbumProgress },
	{ "PrintPlayTime", adapt_PrintPlayTime },
	{ "PrintMedalCount", adapt_PrintMedalCount },
	{ "DrawCollectedMedals", adapt_DrawCollectedMedals },
	{ NULL, NULL },
};
