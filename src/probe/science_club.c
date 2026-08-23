#include "home/science_club.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory Preload_Joseph */
static void adapt_Preload_Joseph(ProbeState *s)
{
	PreloadJosephResult r = Preload_Joseph();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Joseph */

const ProbeEntry probe_entries_science_club[] = {
	{ "Preload_Joseph", adapt_Preload_Joseph },
	{ NULL, NULL },
};
