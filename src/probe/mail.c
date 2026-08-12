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

/* >>> factory InitPCPacks */

static void adapt_InitPCPacks(ProbeState *s)
{
	(void)s;
	InitPCPacks();
}
/* <<< factory InitPCPacks */

/* >>> factory DrawMailMenuCursor */

static void adapt_DrawMailMenuCursor(ProbeState *s)
{
	DrawMailMenuCursor(s->a);
}
/* <<< factory DrawMailMenuCursor */

/* >>> factory GetPCPackCoordinates */

static void adapt_GetPCPackCoordinates(ProbeState *s)
{
	PCPackCoordinates result = GetPCPackCoordinates(s->a);
	s->b = result.b;
	s->c = result.c;
}
/* <<< factory GetPCPackCoordinates */

const ProbeEntry probe_entries_mail[] = {
	{ "TryGivePCPack", adapt_TryGivePCPack },
	{ "GePCPackSelectionCoordinates", adapt_GePCPackSelectionCoordinates },
	{ "InitPCPacks", adapt_InitPCPacks },
	{ "DrawMailMenuCursor", adapt_DrawMailMenuCursor },
	{ "GetPCPackCoordinates", adapt_GetPCPackCoordinates },
	{ NULL, NULL },
};
