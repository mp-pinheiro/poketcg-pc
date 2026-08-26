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

/* >>> factory ShowMailMenuCursor */
static void adapt_ShowMailMenuCursor(ProbeState *s)
{
	(void)s;
	ShowMailMenuCursor();
}
/* <<< factory ShowMailMenuCursor */

/* >>> factory HideMailMenuCursor */
static void adapt_HideMailMenuCursor(ProbeState *s)
{
	(void)s;
	HideMailMenuCursor();
}
/* <<< factory HideMailMenuCursor */

/* >>> factory PrintEmptyPCPackName */
static void adapt_PrintEmptyPCPackName(ProbeState *s)
{
	PrintEmptyPCPackName(s->a);
}
/* <<< factory PrintEmptyPCPackName */

/* >>> factory UpdateMailMenuCursor */
static void adapt_UpdateMailMenuCursor(ProbeState *s)
{
	(void)s;
	UpdateMailMenuCursor();
}
/* <<< factory UpdateMailMenuCursor */

/* >>> factory PCMailHandleDPadInput */
static void adapt_PCMailHandleDPadInput(ProbeState *s)
{
	(void)s;
	PCMailHandleDPadInput();
}
/* <<< factory PCMailHandleDPadInput */

/* >>> factory GetPCPackNameTextID */
static void adapt_GetPCPackNameTextID(ProbeState *s)
{
	uint8_t input = s->a;
	uint16_t text_id = GetPCPackNameTextID(input);
	s->a = (uint8_t)(input << 1);
	s->f = 0u;
	if (s->a == 0u)
		s->f |= 0x80u;
	if ((uint8_t)(input & 0x0Fu) > 0x07u)
		s->f |= 0x20u;
	if ((input & 0x80u) != 0u)
		s->f |= 0x10u;
	s->d = (uint8_t)(text_id >> 8);
	s->e = (uint8_t)text_id;
}
/* <<< factory GetPCPackNameTextID */

const ProbeEntry probe_entries_mail[] = {
	{ "TryGivePCPack", adapt_TryGivePCPack },
	{ "GePCPackSelectionCoordinates", adapt_GePCPackSelectionCoordinates },
	{ "InitPCPacks", adapt_InitPCPacks },
	{ "DrawMailMenuCursor", adapt_DrawMailMenuCursor },
	{ "GetPCPackCoordinates", adapt_GetPCPackCoordinates },
	{ "ShowMailMenuCursor", adapt_ShowMailMenuCursor },
	{ "HideMailMenuCursor", adapt_HideMailMenuCursor },
	{ "PrintEmptyPCPackName", adapt_PrintEmptyPCPackName },
	{ "UpdateMailMenuCursor", adapt_UpdateMailMenuCursor },
	{ "PCMailHandleDPadInput", adapt_PCMailHandleDPadInput },
	{ "GetPCPackNameTextID", adapt_GetPCPackNameTextID },
	{ NULL, NULL },
};
