#include "home/frames.h"
#include "probe.h"

static void adapt_DoAFrames(ProbeState *s)
{
	DoAFrames(s->a);
}

static void adapt_DoFrame(ProbeState *s)
{
	DoFrame();
	(void)s;
}

static void adapt_HandleDPadRepeat(ProbeState *s)
{
	s->hl = HandleDPadRepeat(s->hl);
}

const ProbeEntry probe_entries_frames[] = {
	{ "DoAFrames", adapt_DoAFrames },
	{ "DoFrame", adapt_DoFrame },
	{ "HandleDPadRepeat", adapt_HandleDPadRepeat },
	{ NULL, NULL },
};
