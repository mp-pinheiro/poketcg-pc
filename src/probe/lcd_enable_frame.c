/* >>> part includes */
#include "home/lcd_enable_frame.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory DoFrameIfLCDEnabled */
static void adapt_DoFrameIfLCDEnabled(ProbeState *s)
{
	DoFrameIfLCDEnabled();
	(void)s;
}
/* <<< factory DoFrameIfLCDEnabled */

/* >>> part probe_entries_lcd_enable_frame */
const ProbeEntry probe_entries_lcd_enable_frame[] = {
	{ "DoFrameIfLCDEnabled", adapt_DoFrameIfLCDEnabled },
	{ NULL, NULL },
};
/* <<< part probe_entries_lcd_enable_frame */
