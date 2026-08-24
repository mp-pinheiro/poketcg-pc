#include "home/scenes.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory SetBoosterLogoOAM */
static void adapt_SetBoosterLogoOAM(ProbeState *s)
{
	SetBoosterLogoOAM();
}
/* <<< factory SetBoosterLogoOAM */

/* >>> factory _DrawPortrait */
static void adapt__DrawPortrait(ProbeState *s)
{
	(void)s;
	_DrawPortrait();
}
/* <<< factory _DrawPortrait */

/* >>> factory LoadScene_LoadSGBPacket */
static void adapt_LoadScene_LoadSGBPacket(ProbeState *s)
{
	LoadScene_LoadSGBPacketResult result = LoadScene_LoadSGBPacket(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory LoadScene_LoadSGBPacket */

/* >>> factory LoadScene_LoadCompressedSGBPacket */
static void adapt_LoadScene_LoadCompressedSGBPacket(ProbeState *s)
{
	LoadScene_LoadCompressedSGBPacketResult result = LoadScene_LoadCompressedSGBPacket(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory LoadScene_LoadCompressedSGBPacket */

/* >>> factory LoadScene_SetCardPopAttrBlk */
static void adapt_LoadScene_SetCardPopAttrBlk(ProbeState *s)
{
	LoadScene_SetCardPopAttrBlkResult result = LoadScene_SetCardPopAttrBlk(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory LoadScene_SetCardPopAttrBlk */

/* >>> factory LoadScene_SetGameBoyPrinterAttrBlk */
static void adapt_LoadScene_SetGameBoyPrinterAttrBlk(ProbeState *s)
{
	LoadScene_SetGameBoyPrinterAttrBlkResult r = LoadScene_SetGameBoyPrinterAttrBlk(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory LoadScene_SetGameBoyPrinterAttrBlk */

/* >>> factory _LoadScene */
static void adapt__LoadScene(ProbeState *s)
{
	_LoadScene(s->a, s->b, s->c);
}
/* <<< factory _LoadScene */

/* >>> factory LoadBoosterGfx */
static void adapt_LoadBoosterGfx(ProbeState *s)
{
	s->a = LoadBoosterGfx(s->a, s->b, s->c);
}
/* <<< factory LoadBoosterGfx */

const ProbeEntry probe_entries_scenes[] = {
	{ "SetBoosterLogoOAM", adapt_SetBoosterLogoOAM },
	{ "_DrawPortrait", adapt__DrawPortrait },
	{ "LoadScene_LoadSGBPacket", adapt_LoadScene_LoadSGBPacket },
	{ "LoadScene_LoadCompressedSGBPacket", adapt_LoadScene_LoadCompressedSGBPacket },
	{ "LoadScene_SetCardPopAttrBlk", adapt_LoadScene_SetCardPopAttrBlk },
	{ "LoadScene_SetGameBoyPrinterAttrBlk", adapt_LoadScene_SetGameBoyPrinterAttrBlk },
	{ "_LoadScene", adapt__LoadScene },
	{ "LoadBoosterGfx", adapt_LoadBoosterGfx },
	{ NULL, NULL },
};
