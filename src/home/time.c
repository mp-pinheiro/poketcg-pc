#include "home/time.h"

#include "generated/wram.h"
#include "mem.h"

#define CONSOLE_CGB 0x02u

/* time.asm:40-67. Byte 3 counts mod 256 (ret nz), not 60, and only rolls into
 * byte 4 when it wraps. */
void IncrementPlayTimeCounter(void)
{
	if (!wPlayTimeCounterEnable)
		return;

	uint16_t base = wPlayTimeCounter_ADDR;
	uint8_t b0 = (uint8_t)(gb_read8(base) + 1u);
	gb_write8(base, b0);
	if (b0 < 60u)
		return;
	gb_write8(base, 0);

	uint16_t a1 = (uint16_t)(base + 1u);
	uint8_t b1 = (uint8_t)(gb_read8(a1) + 1u);
	gb_write8(a1, b1);
	if (b1 < 60u)
		return;
	gb_write8(a1, 0);

	uint16_t a2 = (uint16_t)(base + 2u);
	uint8_t b2 = (uint8_t)(gb_read8(a2) + 1u);
	gb_write8(a2, b2);
	if (b2 < 60u)
		return;
	gb_write8(a2, 0);

	uint16_t a3 = (uint16_t)(base + 3u);
	uint8_t b3 = (uint8_t)(gb_read8(a3) + 1u);
	gb_write8(a3, b3);
	if (b3 != 0u)
		return;

	uint16_t a4 = (uint16_t)(base + 4u);
	gb_write8(a4, (uint8_t)(gb_read8(a4) + 1u));
}

/* time.asm:88-93. Returns the exit F register: Z/C encode the CGB check. */
uint8_t CheckForCGB(void)
{
	uint8_t a = wConsole;
	if (a == CONSOLE_CGB)
		return (uint8_t)(0x40u | 0x80u);
	return 0x10u;
}

#define rTMA 0xFF06u
#define rTAC 0xFF07u
#define rSPD 0xFF4Du
#define SPD_DOUBLE 0x80u

TimerSetupResult SetupTimer(void)
{
	uint8_t b = 0xBCu;
	uint8_t f;
	if (wConsole != CONSOLE_CGB) {
		f = 0x10u;
	} else if (gb_read8(rSPD) & SPD_DOUBLE) {
		/* `and SPD_DOUBLE` always sets H and clears N/C; a non-zero result
		 * leaves Z clear, so the double-speed exit is H alone. */
		b = 0x78u;
		f = 0x20u;
	} else {
		f = 0xA0u;
	}
	gb_write8(rTMA, b);
	gb_write8(rTAC, 0x03u);
	gb_write8(rTAC, 0x07u);
	return (TimerSetupResult){0x07u, b, f};
}
