#include "home/script.h"
#include "probe.h"

static void adapt_GetMapScriptPointer(ProbeState *s)
{
	MapScriptResult r = GetMapScriptPointer((uint8_t)s->hl);
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}

const ProbeEntry probe_entries_script[] = {
	{ "GetMapScriptPointer", adapt_GetMapScriptPointer },
	{ NULL, NULL },
};
