#include "home/labels.h"
#include "probe.h"

static void adapt_PrintLabels(ProbeState *s)
{
	LabelsResult r = PrintLabels(s->hl, s->d, s->e);
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

const ProbeEntry probe_entries_labels[] = {
	{ "PrintLabels", adapt_PrintLabels },
	{ NULL, NULL },
};
