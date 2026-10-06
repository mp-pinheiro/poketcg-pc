#include "home/intro.h"
#include "probe.h"

static void adapt_LoadTitleScreenSprites(ProbeState *s)
{
    (void)s;
    LoadTitleScreenSprites();
}

/* >>> factory PlayIntroSequence */
static void adapt_PlayIntroSequence(ProbeState *s)
{
	(void)s;
	PlayIntroSequence();
}
/* <<< factory PlayIntroSequence */

const ProbeEntry probe_entries_intro[] = {
    {"LoadTitleScreenSprites", adapt_LoadTitleScreenSprites},
	{ "PlayIntroSequence", adapt_PlayIntroSequence },
    {NULL, NULL},
};
