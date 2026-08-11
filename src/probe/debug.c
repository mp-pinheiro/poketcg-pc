#include "home/debug.h"
#include "probe.h"

static void adapt_DebugSGBFrame(ProbeState *s)
{
	DebugResult result = DebugSGBFrame();
	s->a = result.a;
	s->f = result.f;
}

static void adapt_DebugStandardBGCharacter(ProbeState *s)
{
	DebugResult result = DebugStandardBGCharacter();
	s->a = result.a;
	s->f = result.f;
}

static void adapt_DebugQuit(ProbeState *s)
{
	DebugResult result = DebugQuit(s->a);
	s->a = result.a;
	s->f = result.f;
}

const ProbeEntry probe_entries_debug[] = {
	{ "DebugSGBFrame", adapt_DebugSGBFrame },
	{ "DebugStandardBGCharacter", adapt_DebugStandardBGCharacter },
	{ "DebugQuit", adapt_DebugQuit },
	{ NULL, NULL },
};
