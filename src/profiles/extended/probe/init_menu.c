#include "home/init_menu.h"
#include "probe.h"

static void adapt_InitMenuScreen(ProbeState *s)
{
	InitMenuRegs result = InitMenuScreen();
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}

static void adapt_FlashWhiteScreen(ProbeState *s)
{
	InitMenuRegs result = FlashWhiteScreen();
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}

const ProbeEntry probe_entries_init_menu[] = {
	{ "InitMenuScreen", adapt_InitMenuScreen },
	{ "FlashWhiteScreen", adapt_FlashWhiteScreen },
	{ NULL, NULL },
};
