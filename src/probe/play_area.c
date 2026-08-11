#include "generated/wram.h"
#include "home/play_area.h"
#include "probe.h"

static void adapt_ZeroObjectPositionsAndToggleOAMCopy_Bank6(ProbeState *s)
{
	ZeroObjectPositionsAndToggleOAMCopy_Bank6();
	s->a = 1;
	s->f = 0xC0;
	s->c = 0;
	s->hl = (uint16_t)(wOAM_ADDR + 160u);
}

const ProbeEntry probe_entries_play_area[] = {
	{ "ZeroObjectPositionsAndToggleOAMCopy_Bank6", adapt_ZeroObjectPositionsAndToggleOAMCopy_Bank6 },
	{ NULL, NULL },
};
