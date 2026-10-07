/* >>> part includes */
#include "home/game_loop.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory SetupResetBackUpRamScreen */
static void adapt_SetupResetBackUpRamScreen(ProbeState *s)
{
	(void)s;
	SetupResetBackUpRamScreen();
}
/* <<< factory SetupResetBackUpRamScreen */

/* >>> factory InitSaveDataAndSetUppercase */
static void adapt_InitSaveDataAndSetUppercase(ProbeState *s)
{
	(void)s;
	InitSaveDataAndSetUppercase();
}
/* <<< factory InitSaveDataAndSetUppercase */

/* >>> factory GameLoop */
static void adapt_GameLoop(ProbeState *s)
{
	(void)s;
	GameLoop();
}
/* <<< factory GameLoop */

/* >>> part probe_entries_game_loop */
const ProbeEntry probe_entries_game_loop[] = {
	{ "SetupResetBackUpRamScreen", adapt_SetupResetBackUpRamScreen },
	{ "InitSaveDataAndSetUppercase", adapt_InitSaveDataAndSetUppercase },
	{ "GameLoop", adapt_GameLoop },
	{ NULL, NULL },
};
/* <<< part probe_entries_game_loop */
