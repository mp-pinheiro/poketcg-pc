#include "home/clear_sram_bg_maps.h"
#include "generated/hram.h"
#include "probe.h"

/* Exit a is the SRAM bank the routine restored (the asm's `pop af` after the fill).
 * b/c/d/e/hl/f are left untouched so a C body that clobbers one shows up as a diff. */
static void adapt_ClearSRAMBGMaps(ProbeState *s)
{
	ClearSRAMBGMaps();
	s->a = hBankSRAM;
}

const ProbeEntry probe_entries_clear_sram_bg_maps[] = {
	{ "ClearSRAMBGMaps", adapt_ClearSRAMBGMaps },
	{ NULL, NULL },
};
