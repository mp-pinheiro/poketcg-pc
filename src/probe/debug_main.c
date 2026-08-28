#include "home/debug_main.h"
#include "probe.h"

static void adapt_Func_126b3(ProbeState *s)
{
	Func126b3Result result = Func_126b3();
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}

/* >>> factory Func_12661 */
static void adapt_Func_12661(ProbeState *s)
{
	Func126b3Result result = Func_12661();

	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory Func_12661 */

const ProbeEntry probe_entries_debug_main[] = {
	{"Func_126b3", adapt_Func_126b3},
	{ "Func_12661", adapt_Func_12661 },
	{NULL, NULL},
};
