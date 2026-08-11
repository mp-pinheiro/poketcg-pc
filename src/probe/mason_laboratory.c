#include "home/mason_laboratory.h"
#include "probe.h"

static void adapt_Script_Tech1(ProbeState *s)
{
	(void)s;
	Script_Tech1();
}

static void adapt_Preload_DrMason(ProbeState *s)
{
	PreloadDrMasonResult r = Preload_DrMason();
	s->a = r.a;
	s->f = r.f;
}

const ProbeEntry probe_entries_mason_laboratory[] = {
	{ "Script_Tech1", adapt_Script_Tech1 },
	{ "Preload_DrMason", adapt_Preload_DrMason },
	{ NULL, NULL },
};
