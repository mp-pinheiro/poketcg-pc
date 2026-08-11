#include "home/debug_main.h"
#include "probe.h"

static void adapt_Func_126b3(ProbeState *s)
{
	Func126b3Result result = Func_126b3();
	s->a = result.a;
	s->f = result.f;
}

const ProbeEntry probe_entries_debug_main[] = {
	{"Func_126b3", adapt_Func_126b3},
	{NULL, NULL},
};
