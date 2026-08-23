#include "home/grass_club_entrance.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory FindEndOfDuelScript */
static void adapt_FindEndOfDuelScript(ProbeState *s)
{
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory FindEndOfDuelScript */

const ProbeEntry probe_entries_grass_club_entrance[] = {
	{ "FindEndOfDuelScript", adapt_FindEndOfDuelScript },
	{ NULL, NULL },
};
