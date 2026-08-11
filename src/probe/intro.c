#include "home/intro.h"
#include "probe.h"

static void adapt_LoadTitleScreenSprites(ProbeState *s)
{
    (void)s;
    LoadTitleScreenSprites();
}

const ProbeEntry probe_entries_intro[] = {
    {"LoadTitleScreenSprites", adapt_LoadTitleScreenSprites},
    {NULL, NULL},
};
