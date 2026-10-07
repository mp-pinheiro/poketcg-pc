/* >>> part includes */
#include "home/init.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory InitAIDuelVars */
static void adapt_InitAIDuelVars(ProbeState *s)
{
	InitAIDuelVars();
	(void)s;
}
/* <<< factory InitAIDuelVars */

/* >>> factory InitAITurnVars */
static void adapt_InitAITurnVars(ProbeState *s)
{
	(void)s;
	InitAITurnVars();
}
/* <<< factory InitAITurnVars */

/* >>> part probe_entries_init */
const ProbeEntry probe_entries_init[] = {
	{ "InitAIDuelVars", adapt_InitAIDuelVars },
	{ "InitAITurnVars", adapt_InitAITurnVars },
	{ NULL, NULL },
};
/* <<< part probe_entries_init */
