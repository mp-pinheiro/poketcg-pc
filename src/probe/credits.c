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

/* >>> factory Func_1d765 */
static void adapt_Func_1d765(ProbeState *s)
{
	s->a = Func_1d765();
}
/* <<< factory Func_1d765 */

const ProbeEntry probe_entries_credits[] = {
	{ "Func_1d758", adapt_Func_1d758 },
	{ "Func_1d765", adapt_Func_1d765 },
	{ NULL, NULL },
};
