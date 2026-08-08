#include "home/serial.h"

#include "generated/wram.h"
#include "mem.h"

#define rSC 0xFF02u
#define SC_INTERNAL 0x01u
#define SC_START 0x80u

/* serial.asm:2-36. Driven at ~240 Hz by TimerHandler. The two opcode paths are
 * mutually exclusive ($29 = begin a transfer, $12 = check for timeout); any other
 * value returns immediately. Registers b/c/d/e are untouched on every path. */
void SerialTimerHandler(void)
{
	uint8_t op = gb_read8(wSerialOp_ADDR);
	if (op == 0x29u) {
		/* `ldh a, [rSC] / add a / ret c`: bit 7 of rSC (transfer in progress)
		 * lands in carry, so a transfer already active exits early. */
		if (gb_read8(rSC) & 0x80u)
			return;
		gb_write8(rSC, SC_INTERNAL);
		gb_write8(rSC, (uint8_t)(SC_START | SC_INTERNAL));
		return;
	}
	if (op != 0x12u)
		return;

	/* serial.asm:18-36. If the serial counter advanced since the last call the
	 * transfer is progressing and the timeout counter resets; otherwise it counts
	 * up and sets wSerialFlags bit 7 once it reaches 4 (~60 Hz). */
	if (gb_read8(wSerialCounter_ADDR) != gb_read8(wSerialCounter2_ADDR)) {
		gb_write8(wSerialCounter2_ADDR, gb_read8(wSerialCounter_ADDR));
		gb_write8(wSerialTimeoutCounter_ADDR, 0);
		return;
	}
	gb_write8(wSerialCounter2_ADDR, gb_read8(wSerialCounter_ADDR));
	uint8_t timeout = (uint8_t)(gb_read8(wSerialTimeoutCounter_ADDR) + 1u);
	if (timeout < 4u) {
		gb_write8(wSerialTimeoutCounter_ADDR, timeout);
		return;
	}
	gb_write8(wSerialTimeoutCounter_ADDR, timeout);
	gb_write8(wSerialFlags_ADDR, (uint8_t)(gb_read8(wSerialFlags_ADDR) | 0x80u));
}
