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

const ProbeEntry probe_entries_main_menu[] = {
	{ "MainMenu_CardPop", adapt_MainMenu_CardPop },
	{ "MainMenu_NewGame", adapt_MainMenu_NewGame },
	{ NULL, NULL },
};
