#include "home/mason_laboratory.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory Preload_DrMason */
static void adapt_Preload_DrMason(ProbeState *s)
{
	PreloadDrMasonResult result = Preload_DrMason();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Preload_DrMason */

const ProbeEntry probe_entries_mason_laboratory[] = {
	{ "Preload_DrMason", adapt_Preload_DrMason },
	{ NULL, NULL },
};
