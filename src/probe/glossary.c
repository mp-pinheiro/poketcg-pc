#include "home/glossary.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory OpenGlossaryScreen */
static void adapt_OpenGlossaryScreen(ProbeState *s)
{
	(void)s;
	OpenGlossaryScreen();
}
/* <<< factory OpenGlossaryScreen */

const ProbeEntry probe_entries_glossary[] = {
	{ "OpenGlossaryScreen", adapt_OpenGlossaryScreen },
	{ NULL, NULL },
};
