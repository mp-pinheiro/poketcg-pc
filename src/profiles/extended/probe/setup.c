#include "home/setup.h"
#include "probe.h"

static void adapt_NoOp(ProbeState *s)
{
	(void)s;
	NoOp();
}

static void adapt_DetectConsole(ProbeState *s)
{
	DetectConsoleResult r = DetectConsole(s->a);
	s->a = r.a;
	s->b = r.b;
}

static void adapt_SetupPalettes(ProbeState *s)
{
	SetupPalettesResult r = SetupPalettes(s->b, s->c, s->d, s->e);
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}

static void adapt_FillTileMap(ProbeState *s)
{
	s->hl = FillTileMap();
}

static void adapt_SetupVRAM(ProbeState *s)
{
	s->hl = SetupVRAM();
}

static void adapt_SetupRegisters(ProbeState *s)
{
	s->hl = SetupRegisters();
}

static void adapt_ZeroRAM(ProbeState *s)
{
	ZeroRAMResult r = ZeroRAM();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}

const ProbeEntry probe_entries_setup[] = {
	{ "NoOp", adapt_NoOp },
	{ "DetectConsole", adapt_DetectConsole },
	{ "SetupPalettes", adapt_SetupPalettes },
	{ "FillTileMap", adapt_FillTileMap },
	{ "SetupVRAM", adapt_SetupVRAM },
	{ "SetupRegisters", adapt_SetupRegisters },
	{ "ZeroRAM", adapt_ZeroRAM },
	{ NULL, NULL },
};
