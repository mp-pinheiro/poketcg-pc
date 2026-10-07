/* >>> part includes */
#include "home/sprite_vblank.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory BackupVBlankFunctionTrampoline */
static void adapt_BackupVBlankFunctionTrampoline(ProbeState *s)
{
	uint16_t de = (uint16_t)((uint16_t)(s->d << 8) | s->e);
	s->a = BackupVBlankFunctionTrampoline(&s->hl, &de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory BackupVBlankFunctionTrampoline */

/* >>> factory SetSpriteAnimationsAsVBlankFunction */
static void adapt_SetSpriteAnimationsAsVBlankFunction(ProbeState *s)
{
	(void)s;
	SetSpriteAnimationsAsVBlankFunction();
}
/* <<< factory SetSpriteAnimationsAsVBlankFunction */

/* >>> factory RestoreVBlankFunction */
static void adapt_RestoreVBlankFunction(ProbeState *s)
{
	(void)s;
	RestoreVBlankFunction();
}
/* <<< factory RestoreVBlankFunction */

/* >>> part probe_entries_sprite_vblank */
const ProbeEntry probe_entries_sprite_vblank[] = {
	{"BackupVBlankFunctionTrampoline", adapt_BackupVBlankFunctionTrampoline},
	{ "SetSpriteAnimationsAsVBlankFunction", adapt_SetSpriteAnimationsAsVBlankFunction },
	{ "RestoreVBlankFunction", adapt_RestoreVBlankFunction },
	{NULL, NULL},
};
/* <<< part probe_entries_sprite_vblank */
