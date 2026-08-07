#include "home/damage.h"

#include "generated/wram.h"
#include "mem.h"

/* damage.asm:2-11 */
void AddToDamage(uint8_t a)
{
	uint16_t lo = (uint16_t)((uint16_t)gb_read8(wDamage_ADDR) + a);
	gb_write8(wDamage_ADDR, (uint8_t)lo);
	uint16_t addr_hi = (uint16_t)(wDamage_ADDR + 1u);
	gb_write8(addr_hi, (uint8_t)(gb_read8(addr_hi) + (lo >> 8)));
}
