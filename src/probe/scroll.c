#include "home/scroll.h"
#include "probe.h"

static void adapt_Func_3e44(ProbeState *s)
{
	Func_3e44();
	(void)s;
}

static void adapt_ApplyBackgroundScroll(ProbeState *s)
{
	ApplyBackgroundScroll();
	(void)s;
}

static void adapt_GetNextBackgroundScroll(ProbeState *s)
{
	s->a = GetNextBackgroundScroll(s->a);
}

static void adapt_EnableInt_LYCoincidence(ProbeState *s)
{
	EnableInt_LYCoincidence();
	(void)s;
}

static void adapt_DisableInt_LYCoincidence(ProbeState *s)
{
	DisableInt_LYCoincidence();
	(void)s;
}

const ProbeEntry probe_entries_scroll[] = {
	{ "ApplyBackgroundScroll", adapt_ApplyBackgroundScroll },
	{ "Func_3e44", adapt_Func_3e44 },
	{ "GetNextBackgroundScroll", adapt_GetNextBackgroundScroll },
	{ "EnableInt_LYCoincidence", adapt_EnableInt_LYCoincidence },
	{ "DisableInt_LYCoincidence", adapt_DisableInt_LYCoincidence },
	{ NULL, NULL },
};
