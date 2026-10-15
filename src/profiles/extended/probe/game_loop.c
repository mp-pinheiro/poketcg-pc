/* === part includes */

/* >>> factory CGBDisclaimer */
static void adapt_CGBDisclaimer(ProbeState *s)
{
	(void)s;
	CGBDisclaimer();
}
/* <<< factory CGBDisclaimer */

/* >>> part probe_entries_game_loop */
const ProbeEntry probe_entries_game_loop[] = {
	{ "CGBDisclaimer", adapt_CGBDisclaimer },
	{ NULL, NULL },
};
/* <<< part probe_entries_game_loop */
