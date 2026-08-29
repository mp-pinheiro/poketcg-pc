#include "home/challenge_hall_entrance.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory Preload_Clerk9 */
static void adapt_Preload_Clerk9(ProbeState *s)
{
	PreloadClerk9Result result = Preload_Clerk9(s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory Preload_Clerk9 */

const ProbeEntry probe_entries_challenge_hall_entrance[] = {
	{ "Preload_Clerk9", adapt_Preload_Clerk9 },
	{ NULL, NULL },
};
