#include "home/empty_screen.h"
#include "probe.h"

static void adapt_EmptyScreen(ProbeState *s)
{
	EmptyScreen();
	(void)s;
}

static void adapt_BCCoordToBGMap0Address(ProbeState *s)
{
	uint16_t address = BCCoordToBGMap0Address(s->b, s->c);

	s->d = (uint8_t)(address >> 8);
	s->e = (uint8_t)address;
}

const ProbeEntry probe_entries_empty_screen[] = {
	{ "EmptyScreen", adapt_EmptyScreen },
	{ "BCCoordToBGMap0Address", adapt_BCCoordToBGMap0Address },
	{ NULL, NULL },
};
