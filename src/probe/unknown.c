#include "home/unknown.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory Func_18661 */
static void adapt_Func_18661(ProbeState *s)
{
	CheckMenuInputResult r = Func_18661();

	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Func_18661 */

const ProbeEntry probe_entries_unknown[] = {
	{ "Func_18661", adapt_Func_18661 },
	{ NULL, NULL },
};
