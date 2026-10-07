/* >>> part includes */
#include "home/frames.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory DoAFrames */
static void adapt_DoAFrames(ProbeState *s)
{
	DoAFrames(s->a);
}
/* <<< factory DoAFrames */

/* >>> factory DoFrame */
static void adapt_DoFrame(ProbeState *s)
{
	DoFrame();
	(void)s;
}
/* <<< factory DoFrame */

/* >>> factory HandleDPadRepeat */
static void adapt_HandleDPadRepeat(ProbeState *s)
{
	s->hl = HandleDPadRepeat(s->hl);
}
/* <<< factory HandleDPadRepeat */

/* >>> part probe_entries_frames */
const ProbeEntry probe_entries_frames[] = {
	{ "DoAFrames", adapt_DoAFrames },
	{ "DoFrame", adapt_DoFrame },
	{ "HandleDPadRepeat", adapt_HandleDPadRepeat },
	{ NULL, NULL },
};
/* <<< part probe_entries_frames */
