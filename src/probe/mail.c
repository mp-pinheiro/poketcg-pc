#include "home/mail.h"
#include "probe.h"

static void adapt_GePCPackSelectionCoordinates(ProbeState *s)
{
	PCPackCoordinates result = GePCPackSelectionCoordinates();
	s->b = result.b;
	s->c = result.c;
}

static void adapt_TryGivePCPack(ProbeState *s)
{
	TryGivePCPack(s->a);
}

const ProbeEntry probe_entries_mail[] = {
	{ "TryGivePCPack", adapt_TryGivePCPack },
	{ "GePCPackSelectionCoordinates", adapt_GePCPackSelectionCoordinates },
	{ NULL, NULL },
};
