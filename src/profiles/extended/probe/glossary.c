/* >>> part includes */
#include "home/glossary.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory OpenGlossaryScreen */
static void adapt_OpenGlossaryScreen(ProbeState *s)
{
	(void)s;
	OpenGlossaryScreen();
}
/* <<< factory OpenGlossaryScreen */

/* >>> part probe_entries_glossary */
const ProbeEntry probe_entries_glossary[] = {
	{ "OpenGlossaryScreen", adapt_OpenGlossaryScreen },
	{ NULL, NULL },
};
/* <<< part probe_entries_glossary */
