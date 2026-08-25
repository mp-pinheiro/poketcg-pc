#include "home/debug_player_coordinates.h"
#include "probe.h"

static void adapt_JumpSetWindowOff(ProbeState *s)
{
	JumpSetWindowOff();
	(void)s;
}

/* >>> factory Func_1c003 */
static void adapt_Func_1c003(ProbeState *s)
{
	Func_1c003();
}
/* <<< factory Func_1c003 */

const ProbeEntry probe_entries_debug_player_coordinates[] = {
	{ "JumpSetWindowOff", adapt_JumpSetWindowOff },
	{ "Func_1c003", adapt_Func_1c003 },
	{ NULL, NULL },
};
