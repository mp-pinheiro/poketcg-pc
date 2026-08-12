#include "home/game_loop.h"
#include "probe.h"

static void adapt_SetupResetBackUpRamScreen(ProbeState *s)
{
	(void)s;
	SetupResetBackUpRamScreen();
}

const ProbeEntry probe_entries_game_loop[] = {
	{ "SetupResetBackUpRamScreen", adapt_SetupResetBackUpRamScreen },
	{ NULL, NULL },
};
