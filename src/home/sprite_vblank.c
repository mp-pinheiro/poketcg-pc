#include "home/sprite_vblank.h"

#include "mem.h"

uint8_t BackupVBlankFunctionTrampoline(uint16_t *hl, uint16_t *de)
{
	const uint8_t first = gb_read8(*hl);
	*hl = (uint16_t)(*hl + 1u);
	gb_write8(*de, first);
	*de = (uint16_t)(*de + 1u);

	const uint8_t second = gb_read8(*hl);
	*hl = (uint16_t)(*hl - 1u);
	gb_write8(*de, second);
	return second;
}
