#include "home/main_menu.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory MainMenu_CardPop */
static void adapt_MainMenu_CardPop(ProbeState *s)
{
	s->f = MainMenu_CardPop();
}
/* <<< factory MainMenu_CardPop */

/* >>> factory MainMenu_NewGame */
static void adapt_MainMenu_NewGame(ProbeState *s)
{
	(void)s;
	MainMenu_NewGame();
}
/* <<< factory MainMenu_NewGame */

/* >>> factory MainMenu_ContinueFromDiary */
static void adapt_MainMenu_ContinueFromDiary(ProbeState *s)
{
	(void)s;
	MainMenu_ContinueFromDiary();
}
/* <<< factory MainMenu_ContinueFromDiary */

/* >>> factory MainMenu_ContinueDuel */
static void adapt_MainMenu_ContinueDuel(ProbeState *s)
{
	(void)s;
	MainMenu_ContinueDuel();
}
/* <<< factory MainMenu_ContinueDuel */

/* >>> factory _GameLoop */
static void adapt__GameLoop(ProbeState *s)
{
	(void)s;
	_GameLoop();
}
/* <<< factory _GameLoop */

const ProbeEntry probe_entries_main_menu[] = {
	{ "MainMenu_CardPop", adapt_MainMenu_CardPop },
	{ "MainMenu_NewGame", adapt_MainMenu_NewGame },
	{ "MainMenu_ContinueFromDiary", adapt_MainMenu_ContinueFromDiary },
	{ "MainMenu_ContinueDuel", adapt_MainMenu_ContinueDuel },
	{ "_GameLoop", adapt__GameLoop },
	{ NULL, NULL },
};
