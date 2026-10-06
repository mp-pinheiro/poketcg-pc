#include "home/wait_keys.h"
#include "probe.h"

static void adapt_WaitUntilKeysArePressed(ProbeState *s)
{
	WaitKeysResult result = WaitUntilKeysArePressed(s->a);
	s->a = result.a;
	s->f = result.f;
}

const ProbeEntry probe_entries_wait_keys[] = {
	{ "WaitUntilKeysArePressed", adapt_WaitUntilKeysArePressed },
	{ NULL, NULL },
};
