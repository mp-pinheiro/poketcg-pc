#include "home/list.h"

#include "generated/wram.h"
#include "mem.h"

/* poketcg/src/home/list.asm:2 */
void SetListPointer(uint16_t de)
{
	gb_write8(wListPointer_ADDR, (uint8_t)de);
	gb_write8((uint16_t)(wListPointer_ADDR + 1), (uint8_t)(de >> 8));
}

/* poketcg/src/home/list.asm:34, falling through into SetListToNextPosition
 * (list.asm:24) whose writeback is inlined here — that label pops the hl/de its
 * fallthrough callers pushed, so it is not a routine of its own. */
void SetNextElementOfList(uint8_t a)
{
	uint16_t de = (uint16_t)(gb_read8(wListPointer_ADDR) |
	                         (gb_read8((uint16_t)(wListPointer_ADDR + 1)) << 8));

	gb_write8(de, a);
	de = (uint16_t)(de + 1);

	gb_write8((uint16_t)(wListPointer_ADDR + 1), (uint8_t)(de >> 8));
	gb_write8(wListPointer_ADDR, (uint8_t)de);
}
