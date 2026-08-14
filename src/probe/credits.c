#include "home/credits.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory Func_1d758 */
static void adapt_Func_1d758(ProbeState *s)
{
	Func_1d758();
}
/* <<< factory Func_1d758 */

const ProbeEntry probe_entries_credits[] = {
	{ "Func_1d758", adapt_Func_1d758 },
	{ NULL, NULL },
};
