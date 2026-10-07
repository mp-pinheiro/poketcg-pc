/* >>> factory PrintAlbumProgress_SkipGetProgress */
static void adapt_PrintAlbumProgress_SkipGetProgress(ProbeState *s)
{
	PrintAlbumProgress_SkipGetProgress(s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory PrintAlbumProgress_SkipGetProgress */
/* --- factory DrawCollectedMedals */
/* >>> part probe_entries_print_stats */
const ProbeEntry probe_entries_print_stats[] = {
	{ "DrawPauseMenuPlayerPortrait", adapt_DrawPauseMenuPlayerPortrait },
	{ "FlashReceivedMedal", adapt_FlashReceivedMedal },
	{ "ConvertWordToNumericalDigits", adapt_ConvertWordToNumericalDigits },
	{ "PrintAlbumProgress_SkipGetProgress", adapt_PrintAlbumProgress_SkipGetProgress },
	{ "PrintPlayTime_SkipUpdateTime", adapt_PrintPlayTime_SkipUpdateTime },
	{ "PrintAlbumProgress", adapt_PrintAlbumProgress },
	{ "PrintPlayTime", adapt_PrintPlayTime },
	{ "PrintMedalCount", adapt_PrintMedalCount },
	{ NULL, NULL },
};
/* <<< part probe_entries_print_stats */
