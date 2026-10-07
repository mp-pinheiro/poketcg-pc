/* >>> part includes */
#include "home/intro.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory LoadTitleScreenSprites */
static void adapt_LoadTitleScreenSprites(ProbeState *s)
{
    (void)s;
    LoadTitleScreenSprites();
}
/* <<< factory LoadTitleScreenSprites */

/* >>> factory PlayIntroSequence */
static void adapt_PlayIntroSequence(ProbeState *s)
{
	(void)s;
	PlayIntroSequence();
}
/* <<< factory PlayIntroSequence */

/* >>> part probe_entries_intro */
const ProbeEntry probe_entries_intro[] = {
    {"LoadTitleScreenSprites", adapt_LoadTitleScreenSprites},
	{ "PlayIntroSequence", adapt_PlayIntroSequence },
    {NULL, NULL},
};
/* <<< part probe_entries_intro */
