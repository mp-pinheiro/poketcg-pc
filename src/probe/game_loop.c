#include "home/game_loop.h"
#include "probe.h"

static void adapt_SetupResetBackUpRamScreen(ProbeState *s)
{
	(void)s;
	SetupResetBackUpRamScreen();
}

/* >>> factory InitSaveDataAndSetUppercase */
static void adapt_InitSaveDataAndSetUppercase(ProbeState *s)
{
	(void)s;
	InitSaveDataAndSetUppercase();
}
/* <<< factory InitSaveDataAndSetUppercase */

const ProbeEntry probe_entries_game_loop[] = {
	{ "SetupResetBackUpRamScreen", adapt_SetupResetBackUpRamScreen },
	{ "InitSaveDataAndSetUppercase", adapt_InitSaveDataAndSetUppercase },
	{ NULL, NULL },
};
