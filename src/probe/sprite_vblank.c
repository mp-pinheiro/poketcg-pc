#include "home/sprite_vblank.h"
#include "probe.h"

static void adapt_BackupVBlankFunctionTrampoline(ProbeState *s)
{
	uint16_t de = (uint16_t)((uint16_t)(s->d << 8) | s->e);
	s->a = BackupVBlankFunctionTrampoline(&s->hl, &de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}

const ProbeEntry probe_entries_sprite_vblank[] = {
	{"BackupVBlankFunctionTrampoline", adapt_BackupVBlankFunctionTrampoline},
	{NULL, NULL},
};
