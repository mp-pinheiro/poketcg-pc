/* >>> part includes */
#include "home/wait_keys.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory WaitUntilKeysArePressed */
static void adapt_WaitUntilKeysArePressed(ProbeState *s)
{
	WaitKeysResult result = WaitUntilKeysArePressed(s->a);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory WaitUntilKeysArePressed */

/* >>> part probe_entries_wait_keys */
const ProbeEntry probe_entries_wait_keys[] = {
	{ "WaitUntilKeysArePressed", adapt_WaitUntilKeysArePressed },
	{ NULL, NULL },
};
/* <<< part probe_entries_wait_keys */
