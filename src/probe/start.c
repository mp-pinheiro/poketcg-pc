#include "home/start.h"
#include "probe.h"

static void adapt_ShowCardPopCGBDisclaimer(ProbeState *s)
{
	s->f = ShowCardPopCGBDisclaimer();
}

const ProbeEntry probe_entries_start[] = {
	{ "ShowCardPopCGBDisclaimer", adapt_ShowCardPopCGBDisclaimer },
	{ NULL, NULL },
};
