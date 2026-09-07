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

/* >>> factory Preload_Isaac */
static void adapt_Preload_Isaac(ProbeState *s)
{
	PreloadIsaacResult r = Preload_Isaac();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Preload_Isaac */

const ProbeEntry probe_entries_lightning_club[] = {
	{ "LightningClubAfterDuel", adapt_LightningClubAfterDuel },
	{ "Preload_Isaac", adapt_Preload_Isaac },
	{ NULL, NULL },
};
