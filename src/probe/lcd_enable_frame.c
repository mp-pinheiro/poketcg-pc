#include "home/lcd_enable_frame.h"
#include "probe.h"

static void adapt_DoFrameIfLCDEnabled(ProbeState *s)
{
	DoFrameIfLCDEnabled();
	(void)s;
}

const ProbeEntry probe_entries_lcd_enable_frame[] = {
	{ "DoFrameIfLCDEnabled", adapt_DoFrameIfLCDEnabled },
	{ NULL, NULL },
};
