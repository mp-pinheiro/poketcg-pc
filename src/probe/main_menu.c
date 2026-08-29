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

const ProbeEntry probe_entries_main_menu[] = {
	{ "MainMenu_CardPop", adapt_MainMenu_CardPop },
	{ NULL, NULL },
};
