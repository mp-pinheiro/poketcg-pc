#include "home/time.h"

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/switch_rom.h"
#include "home/time.h"
#include "home/serial.h"
#include "home/music1.h"
#include "generated/wram.h"
#include "generated/hram.h"
#define IN_TIMER 0x01u
#define BANK_SOUND_TIMER_HANDLER 0x3Du
/* <<< factory statics */

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

#define rIE 0xFFFFu
#define rIF 0xFF0Fu
#define rJOYP 0xFF00u
#define rSPD 0xFF4Du
#define B_SPD_DOUBLE 7u
#define B_SPD_PREPARE 0u

void SwitchToCGBNormalSpeed(void)
{
	if ((CheckForCGB() & 0x10u) != 0u)
		return;
	uint8_t spd = gb_read8(rSPD);
	if ((spd & (uint8_t)(1u << B_SPD_DOUBLE)) == 0u)
		return;
	uint8_t ie = gb_read8(rIE);
	gb_write8(rIE, 0u);
	gb_write8(rSPD, (uint8_t)(spd | (uint8_t)(1u << B_SPD_PREPARE)));
	gb_write8(rIF, 0u);
	gb_write8(rIE, 0u);
	gb_write8(rJOYP, 0x30u);
	(void)SetupTimer();
	gb_write8(rIE, ie);
}

void SwitchToCGBDoubleSpeed(void)
{
	if ((CheckForCGB() & 0x10u) != 0u)
		return;
	uint8_t spd = gb_read8(rSPD);
	if ((spd & (uint8_t)(1u << B_SPD_DOUBLE)) != 0u)
		return;
	uint8_t ie = gb_read8(rIE);
	gb_write8(rIE, 0u);
	gb_write8(rSPD, (uint8_t)(spd | (uint8_t)(1u << B_SPD_PREPARE)));
	gb_write8(rIF, 0u);
	gb_write8(rIE, 0u);
	gb_write8(rJOYP, 0x30u);
	(void)SetupTimer();
	gb_write8(rIE, ie);
}

#define rTMA 0xFF06u
#define rTAC 0xFF07u

TimerSetupResult SetupTimer(void)
{
	uint8_t b = 0xBCu;
	uint8_t f;
	if (wConsole != CONSOLE_CGB) {
		f = 0x10u;
	} else {
		f = 0xA0u;
	}
	gb_write8(rTMA, b);
	gb_write8(rTAC, 0x03u);
	gb_write8(rTAC, 0x07u);
	return (TimerSetupResult){0x07u, b, f};
}

/* >>> factory TimerHandler */
void TimerHandler(void)
{
	SerialTimerHandler();
	uint8_t counter = wTimerCounter;
	wTimerCounter = (uint8_t)(counter + 1u);
	if ((counter & 0x3u) != 0u)
		return;
	IncrementPlayTimeCounter();
	if ((wReentrancyFlag & (1u << IN_TIMER)) != 0u)
		return;
	wReentrancyFlag = (uint8_t)(wReentrancyFlag | (1u << IN_TIMER));
	uint8_t saved_bank = hBankROM;
	BankswitchROM(BANK_SOUND_TIMER_HANDLER);
	SoundTimerHandler();
	BankswitchROM(saved_bank);
	wReentrancyFlag = (uint8_t)(wReentrancyFlag & (uint8_t)~(1u << IN_TIMER));
}
/* <<< factory TimerHandler */
