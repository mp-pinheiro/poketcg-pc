#include "home/lightning_club.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory LightningClubAfterDuel */
static void adapt_LightningClubAfterDuel(ProbeState *s)
{
	LightningClubAfterDuelResult r = LightningClubAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory LightningClubAfterDuel */

const ProbeEntry probe_entries_lightning_club[] = {
	{ "LightningClubAfterDuel", adapt_LightningClubAfterDuel },
	{ NULL, NULL },
};
