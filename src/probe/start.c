#include "home/start.h"
#include "probe.h"

static void adapt_ShowCardPopCGBDisclaimer(ProbeState *s)
{
	s->f = ShowCardPopCGBDisclaimer();
}

/* >>> factory CheckIfHasSaveData */
static void adapt_CheckIfHasSaveData(ProbeState *s)
{
	CheckIfHasSaveDataResult r = CheckIfHasSaveData();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CheckIfHasSaveData */

const ProbeEntry probe_entries_start[] = {
	{ "ShowCardPopCGBDisclaimer", adapt_ShowCardPopCGBDisclaimer },
	{ "CheckIfHasSaveData", adapt_CheckIfHasSaveData },
	{ NULL, NULL },
};
