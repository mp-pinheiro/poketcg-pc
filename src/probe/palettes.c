/* >>> part includes */
#include "home/palettes.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory FlushAllPalettes */
static void adapt_FlushAllPalettes(ProbeState *s)
{
	(void)s;
	FlushAllPalettes();
}
/* <<< factory FlushAllPalettes */

/* >>> factory FlushPalette */
static void adapt_FlushPalette(ProbeState *s)
{
	FlushPalette(s->a);
}
/* <<< factory FlushPalette */

/* >>> factory SetBGP */
static void adapt_SetBGP(ProbeState *s)
{
	SetBGP(s->a);
}
/* <<< factory SetBGP */

/* >>> factory FlushPalette0 */
static void adapt_FlushPalette0(ProbeState *s)
{
	(void)s;
	FlushPalette0();
}
/* <<< factory FlushPalette0 */

/* >>> factory FlushPalettes */
static void adapt_FlushPalettes(ProbeState *s)
{
	FlushPalettes(s->a);
}
/* <<< factory FlushPalettes */

/* >>> factory SetOBP0 */
static void adapt_SetOBP0(ProbeState *s)
{
	SetOBP0(s->a);
}
/* <<< factory SetOBP0 */

/* >>> factory SetOBP1 */
static void adapt_SetOBP1(ProbeState *s)
{
	SetOBP1(s->a);
}
/* <<< factory SetOBP1 */

/* >>> factory FlushPalettesIfRequested */
static void adapt_FlushPalettesIfRequested(ProbeState *s)
{
	FlushPalettesIfRequestedResult r = FlushPalettesIfRequested_Registers(s->b, s->c, s->d, s->e);
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory FlushPalettesIfRequested */

/* >>> factory CopyCGBPalettes */
static void adapt_CopyCGBPalettes(ProbeState *s)
{
	CopyCGBPalettesResult r = CopyCGBPalettes(s->a, s->b);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory CopyCGBPalettes */

/* >>> factory FlushAllCGBPalettes */
static void adapt_FlushAllCGBPalettes(ProbeState *s)
{
	FlushAllCGBPalettesResult r = FlushAllCGBPalettes();
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory FlushAllCGBPalettes */

/* >>> part probe_entries_palettes */
const ProbeEntry probe_entries_palettes[] = {
	{ "FlushAllPalettes", adapt_FlushAllPalettes },
	{ "FlushPalette", adapt_FlushPalette },
	{ "SetBGP", adapt_SetBGP },
	{ "FlushPalette0", adapt_FlushPalette0 },
	{ "FlushPalettes", adapt_FlushPalettes },
	{ "SetOBP0", adapt_SetOBP0 },
	{ "SetOBP1", adapt_SetOBP1 },
	{ "FlushPalettesIfRequested", adapt_FlushPalettesIfRequested },
	{ "CopyCGBPalettes", adapt_CopyCGBPalettes },
	{ "FlushAllCGBPalettes", adapt_FlushAllCGBPalettes },
	{ NULL, NULL },
};
/* <<< part probe_entries_palettes */
