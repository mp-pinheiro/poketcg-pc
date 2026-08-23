#include "home/mason_laboratory.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory Preload_DrMason */
static void adapt_Preload_DrMason(ProbeState *s)
{
	PreloadDrMasonResult result = Preload_DrMason();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Preload_DrMason */

/* >>> factory MasonLaboratoryAfterDuel */
static void adapt_MasonLaboratoryAfterDuel(ProbeState *s)
{
	MasonLaboratoryAfterDuelResult r = MasonLaboratoryAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory MasonLaboratoryAfterDuel */

const ProbeEntry probe_entries_mason_laboratory[] = {
	{ "Preload_DrMason", adapt_Preload_DrMason },
	{ "MasonLaboratoryAfterDuel", adapt_MasonLaboratoryAfterDuel },
	{ NULL, NULL },
};
