#include "home/debug.h"
#include "probe.h"

static void adapt_DebugSGBFrame(ProbeState *s)
{
	DebugSGBFrameResult result = DebugSGBFrame(s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}

static void adapt_DebugStandardBGCharacter(ProbeState *s)
{
	DebugStandardBGCharacterResult result = DebugStandardBGCharacter(
		s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
	s->e = result.e;
}

static void adapt_DebugQuit(ProbeState *s)
{
	DebugQuitResult result = DebugQuit(s->a, s->f);
	s->a = result.a;
	s->f = result.f;
}

const ProbeEntry probe_entries_debug[] = {
	{"DebugSGBFrame", adapt_DebugSGBFrame},
	{"DebugStandardBGCharacter", adapt_DebugStandardBGCharacter},
	{"DebugQuit", adapt_DebugQuit},
	{NULL, NULL},
};
