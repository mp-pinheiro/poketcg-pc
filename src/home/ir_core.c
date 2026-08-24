#include "home/ir_core.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/ir_core.h"
#include "mem.h"
#define RP_ADDR 0xFF56u
#define RP_ENABLE 0xC0u
#define RP_WRITE_HIGH 0x01u
#define RP_WRITE_LOW 0x00u

#include "home/ir_core.h"
#include "mem.h"
#define RP_ADDR_470 0xFF56u
#define B_RP_DATA_IN_470 1u

#include "home/ir_core.h"
#include "mem.h"
/* <<< factory statics */

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

/* >>> factory TransmitIRBit */
TransmitIRBitResult TransmitIRBit(uint8_t a, uint8_t f, uint16_t hl)
{
	(void)a;
	uint8_t flags = (uint8_t)(f & 0x10u);
	if ((f & 0x10u) != 0u) {
		flags = 0xD0u;
	} else {
		gb_write8(hl, (uint8_t)(RP_WRITE_HIGH | RP_ENABLE));
		gb_write8(hl, (uint8_t)(RP_WRITE_LOW | RP_ENABLE));
		flags = 0xC0u;
	}
	return (TransmitIRBitResult){0x00u, flags};
}
/* <<< factory TransmitIRBit */

/* >>> factory ReturnZFlagUnsetAndCarryFlagSet2 */
ReturnZFlagUnsetAndCarryFlagSetResult ReturnZFlagUnsetAndCarryFlagSet2(void)
{
	ReturnZFlagUnsetAndCarryFlagSetResult result = ReturnZFlagUnsetAndCarryFlagSet();
	return result;
}
/* <<< factory ReturnZFlagUnsetAndCarryFlagSet2 */

/* >>> factory ReceiveByteThroughIR */
ReceiveByteThroughIRResult ReceiveByteThroughIR(void)
{
	uint8_t loop_count = 0u;
	for (;;) {
		uint8_t rp = gb_read8(RP_ADDR_470);
		if ((rp & (1u << B_RP_DATA_IN_470)) == 0u)
			break;
		loop_count = (uint8_t)(loop_count - 1u);
		if (loop_count != 0u)
			continue;
		return (ReceiveByteThroughIRResult){0xFFu, 0x90u};
	}

	uint8_t d = 0u;
	for (uint8_t e = 8u; e != 0u; e--) {
		uint8_t bit_val = 1u;
		uint8_t rp = gb_read8(RP_ADDR_470);
		if ((rp & (1u << B_RP_DATA_IN_470)) == 0u)
			bit_val = 0u;
		for (uint8_t inner = 9u; inner != 0u; inner--) {
			rp = gb_read8(RP_ADDR_470);
			if ((rp & (1u << B_RP_DATA_IN_470)) == 0u)
				bit_val = 0u;
		}
		d = (uint8_t)((d >> 1) | (uint8_t)(bit_val << 7));
	}
	uint8_t result_a = d;
	uint8_t result_f = (result_a == 0u) ? 0x80u : 0x00u;
	return (ReceiveByteThroughIRResult){result_a, result_f};
}
/* <<< factory ReceiveByteThroughIR */

/* >>> factory ReceiveByteThroughIR_ZeroIfUnsuccessful */
ReceiveByteThroughIRResult ReceiveByteThroughIR_ZeroIfUnsuccessful(void)
{
	ReceiveByteThroughIRResult r = ReceiveByteThroughIR();
	if (r.f & 0x10u)
		return (ReceiveByteThroughIRResult){0u, 0x80u};
	return r;
}
/* <<< factory ReceiveByteThroughIR_ZeroIfUnsuccessful */
