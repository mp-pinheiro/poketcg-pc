#include "home/labels.h"
#include "probe.h"

static void adapt_PrintLabels(ProbeState *s)
{
	LabelsResult r = PrintLabels(s->hl, s->d, s->e);
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

/* >>> factory InitAndPrintMenu */
static void adapt_InitAndPrintMenu(ProbeState *s)
{
	InitAndPrintMenu(s->hl, s->a);
}
/* <<< factory InitAndPrintMenu */

const ProbeEntry probe_entries_labels[] = {
	{ "PrintLabels", adapt_PrintLabels },
	{ "InitAndPrintMenu", adapt_InitAndPrintMenu },
	{ NULL, NULL },
};
