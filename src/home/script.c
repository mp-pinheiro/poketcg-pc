#include "home/script.h"

#include "generated/wram.h"
#include "mem.h"

#define MAP_SCRIPTS_BANK 4u
#define MAP_SCRIPTS 0x562Au

/* script.asm:62-95. Entry l = script selector; the entry is
 * MapScripts + wCurMap * 16 + l in bank 4. The pointer is read there and the
 * routine's bank is restored, so the returned value is a plain address.
 * Exit carry is set iff the pointer is non-zero (`scf / ccf` double-negation),
 * and a is lo | hi of the pointer. */
MapScriptResult GetMapScriptPointer(uint8_t l)
{
	uint16_t entry = (uint16_t)(MAP_SCRIPTS + (uint16_t)wCurMap * 16u + l);
	const uint8_t *p = rom_ptr(MAP_SCRIPTS_BANK, entry);
	uint16_t ptr = (uint16_t)(p[0] | (uint16_t)p[1] << 8);

	uint8_t a = (uint8_t)((uint8_t)ptr | (uint8_t)(ptr >> 8));
	uint8_t f = 0x10u; /* carry set when found */
	if (a == 0)
		f = 0x80u; /* `or h` set Z, `scf`+`ccf` left carry clear */
	return (MapScriptResult){a, f, ptr};
}
