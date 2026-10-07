/* >>> part includes */
#include "home/setup.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory NoOp */
static void adapt_NoOp(ProbeState *s)
{
	(void)s;
	NoOp();
}
/* <<< factory NoOp */

/* >>> factory DetectConsole */
static void adapt_DetectConsole(ProbeState *s)
{
	DetectConsoleResult r = DetectConsole(s->a);
	s->a = r.a;
	s->b = r.b;
}
/* <<< factory DetectConsole */

/* >>> factory SetupPalettes */
static void adapt_SetupPalettes(ProbeState *s)
{
	SetupPalettesResult r = SetupPalettes(s->b, s->c, s->d, s->e);
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory SetupPalettes */

/* >>> factory FillTileMap */
static void adapt_FillTileMap(ProbeState *s)
{
	s->hl = FillTileMap();
}
/* <<< factory FillTileMap */

/* >>> factory SetupVRAM */
static void adapt_SetupVRAM(ProbeState *s)
{
	s->hl = SetupVRAM();
}
/* <<< factory SetupVRAM */

/* >>> factory SetupRegisters */
static void adapt_SetupRegisters(ProbeState *s)
{
	s->hl = SetupRegisters();
}
/* <<< factory SetupRegisters */

/* >>> factory ZeroRAM */
static void adapt_ZeroRAM(ProbeState *s)
{
	ZeroRAMResult r = ZeroRAM();
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory ZeroRAM */

/* >>> part probe_entries_setup */
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
/* <<< part probe_entries_setup */
