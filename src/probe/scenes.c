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

const ProbeEntry probe_entries_scenes[] = {
	{ "SetBoosterLogoOAM", adapt_SetBoosterLogoOAM },
	{ "_DrawPortrait", adapt__DrawPortrait },
	{ "LoadScene_LoadSGBPacket", adapt_LoadScene_LoadSGBPacket },
	{ "LoadScene_LoadCompressedSGBPacket", adapt_LoadScene_LoadCompressedSGBPacket },
	{ NULL, NULL },
};
