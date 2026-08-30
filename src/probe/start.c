#include "home/start.h"
#include "probe.h"

static void adapt_ShowCardPopCGBDisclaimer(ProbeState *s)
{
	s->f = ShowCardPopCGBDisclaimer();
}

/* >>> factory CheckIfHasSaveData */
static void adapt_CheckIfHasSaveData(ProbeState *s)
{
	CheckIfHasSaveDataResult r = CheckIfHasSaveData();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CheckIfHasSaveData */

/* >>> factory PrintStartMenuDescriptionText */
static void adapt_PrintStartMenuDescriptionText(ProbeState *s)
{
	PrintStartMenuDescriptionTextResult r = PrintStartMenuDescriptionText(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory PrintStartMenuDescriptionText */

/* >>> factory AskToContinueFromDiaryWithDuelData */
static void adapt_AskToContinueFromDiaryWithDuelData(ProbeState *s)
{
	AskToContinueFromDiaryWithDuelDataResult result = AskToContinueFromDiaryWithDuelData();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AskToContinueFromDiaryWithDuelData */

/* >>> factory HandleStartMenu */
static void adapt_HandleStartMenu(ProbeState *s)
{
	(void)s;
	HandleStartMenu();
}
/* <<< factory HandleStartMenu */

/* >>> factory DrawPlayerPortraitAndPrintNewGameText */
static void adapt_DrawPlayerPortraitAndPrintNewGameText(ProbeState *s)
{
	(void)s;
	DrawPlayerPortraitAndPrintNewGameText();
}
/* <<< factory DrawPlayerPortraitAndPrintNewGameText */

/* >>> factory DeleteSaveDataForNewGame */
static void adapt_DeleteSaveDataForNewGame(ProbeState *s)
{
	(void)s;
	DeleteSaveDataForNewGame();
}
/* <<< factory DeleteSaveDataForNewGame */

/* >>> factory HandleTitleScreen */
static void adapt_HandleTitleScreen(ProbeState *s)
{
	(void)s;
	HandleTitleScreen();
}
/* <<< factory HandleTitleScreen */

const ProbeEntry probe_entries_start[] = {
	{ "ShowCardPopCGBDisclaimer", adapt_ShowCardPopCGBDisclaimer },
	{ "CheckIfHasSaveData", adapt_CheckIfHasSaveData },
	{ "PrintStartMenuDescriptionText", adapt_PrintStartMenuDescriptionText },
	{ "AskToContinueFromDiaryWithDuelData", adapt_AskToContinueFromDiaryWithDuelData },
	{ "HandleStartMenu", adapt_HandleStartMenu },
	{ "DrawPlayerPortraitAndPrintNewGameText", adapt_DrawPlayerPortraitAndPrintNewGameText },
	{ "DeleteSaveDataForNewGame", adapt_DeleteSaveDataForNewGame },
	{ "HandleTitleScreen", adapt_HandleTitleScreen },
	{ NULL, NULL },
};
