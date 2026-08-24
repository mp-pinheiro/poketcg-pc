#include "home/fire_club_lobby.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory FindExtraInteractableObjects */
static void adapt_FindExtraInteractableObjects(ProbeState *s)
{
	FindExtraInteractableObjectsResult r = FindExtraInteractableObjects(s->hl);
	s->hl = r.hl;
	s->d = r.d;
	s->e = r.e;
	if (r.carry) {
		s->b = r.b;
		s->c = r.c;
	}
}
/* <<< factory FindExtraInteractableObjects */

const ProbeEntry probe_entries_fire_club_lobby[] = {
	{ "FindExtraInteractableObjects", adapt_FindExtraInteractableObjects },
	{ NULL, NULL },
};
