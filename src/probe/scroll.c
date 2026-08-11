#include "home/scroll.h"
#include "probe.h"

static void adapt_ApplyBackgroundScroll(ProbeState *s)
{
	ApplyBackgroundScroll();
	(void)s;
}

const ProbeEntry probe_entries_scroll[] = {
	{ "ApplyBackgroundScroll", adapt_ApplyBackgroundScroll },
	{ NULL, NULL },
};
