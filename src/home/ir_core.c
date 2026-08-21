#include "home/ir_core.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"

/* >>> factory StoreRegistersInIRDataBuffer */
/* ir_core.asm:483-506 */
void StoreRegistersInIRDataBuffer(uint8_t a, uint8_t f, uint8_t b, uint8_t c,
	uint8_t d, uint8_t e, uint16_t *hl)
{
	uint16_t saved_hl = *hl;
	uint16_t addr = wIRDataBuffer_ADDR;

	gb_write8(addr++, f);
	gb_write8(addr++, a);
	gb_write8(addr++, (uint8_t)saved_hl);
	gb_write8(addr++, (uint8_t)(saved_hl >> 8));
	gb_write8(addr++, e);
	gb_write8(addr++, d);
	gb_write8(addr++, c);
	gb_write8(addr, b);
	*hl = addr;
}
/* <<< factory StoreRegistersInIRDataBuffer */

/* >>> factory LoadRegistersFromIRDataBuffer */
/* ir_core.asm:510-531 */
IRRegisterState LoadRegistersFromIRDataBuffer(void)
{
	uint16_t addr = wIRDataBuffer_ADDR;
	IRRegisterState r;
	uint8_t l;
	uint8_t h;

	r.f = (uint8_t)(gb_read8(addr++) & 0xf0u);
	r.a = gb_read8(addr++);
	l = gb_read8(addr++);
	h = gb_read8(addr++);
	r.hl = (uint16_t)(l | (uint16_t)h << 8);
	r.e = gb_read8(addr++);
	r.d = gb_read8(addr++);
	r.c = gb_read8(addr++);
	r.b = gb_read8(addr);
	return r;
}
/* <<< factory LoadRegistersFromIRDataBuffer */

/* >>> factory ReturnZFlagUnsetAndCarryFlagSet */
ReturnZFlagUnsetAndCarryFlagSetResult ReturnZFlagUnsetAndCarryFlagSet(void)
{
	return (ReturnZFlagUnsetAndCarryFlagSetResult){0xFFu, 0x10u};
}
/* <<< factory ReturnZFlagUnsetAndCarryFlagSet */
