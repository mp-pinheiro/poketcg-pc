#include "home/input.h"

#include "home/serial.h"
#include "mem.h"
#include "generated/hram.h"
/* >>> factory statics */
#include "generated/wram.h"
/* <<< factory statics */

#define JOYP 0xFF00u
#define JOYP_GET_BUTTONS 0x10u
#define JOYP_GET_CTRL_PAD 0x20u
#define JOYP_GET_NONE 0x30u
#define JOYP_INPUTS 0x0Fu
#define PAD_A 0x01u
#define PAD_B 0x02u
#define PAD_SELECT 0x04u
#define PAD_START 0x08u
#define PAD_BUTTONS (PAD_A | PAD_B | PAD_SELECT | PAD_START)

static uint8_t read_joypad(void)
{
	return gb_read8(JOYP);
}

void SaveButtonsHeld(uint8_t c)
{
	gb_write8(hKeysHeld_ADDR, c);
	gb_write8(JOYP, JOYP_GET_NONE);
}
/* >>> factory ReadJoypad */
void ReadJoypad(void)
{
	uint8_t buttons;
	uint8_t c;
	uint8_t held;

	gb_write8(JOYP, JOYP_GET_CTRL_PAD);
	(void)read_joypad();
	buttons = (uint8_t)(~read_joypad() & JOYP_INPUTS);
	buttons = (uint8_t)(buttons << 4);
	gb_write8(JOYP, JOYP_GET_BUTTONS);
	(void)read_joypad();
	(void)read_joypad();
	(void)read_joypad();
	(void)read_joypad();
	(void)read_joypad();
	c = (uint8_t)(~read_joypad() & JOYP_INPUTS);
	c |= buttons;
	held = gb_read8(hKeysHeld_ADDR);
	gb_write8(hKeysReleased_ADDR, (uint8_t)((held ^ c) & (uint8_t)~c));
	gb_write8(hKeysPressed_ADDR, (uint8_t)((held ^ c) & c));
	if ((held & PAD_BUTTONS) == PAD_BUTTONS) {
		/* A + B + Start + Select: reset game (input.asm:36-41) */
		ResetSerial();
		(void)Reset();
		return; /* SaveButtonsHeld is skipped: hKeysHeld keeps the combo */
	}
	SaveButtonsHeld(c);
}
/* <<< factory ReadJoypad */

void ClearJoypad(uint16_t *hl)
{
	uint16_t address = hDPadRepeat_ADDR;

	gb_write8(address++, 0);
	gb_write8(address++, 0);
	gb_write8(address++, 0);
	gb_write8(address++, 0);
	gb_write8(address, 0);
	(void)hl;
}

/* >>> factory Reset */
/* input.asm:43-46: `ld a, [wInitialA]; di; jp Start`. The C port cannot
 * abandon its call stack, so Reset delegates to the boot-restart hook; the
 * host loop (src/runtime.c run_game) installs it with a setjmp guard and
 * re-runs Start(wInitialA); GameLoop();. The NULL default keeps probe runs
 * bounded and preserves the pre-ret observable `a = wInitialA`. */
void (*poketcg_request_boot_restart)(void) = NULL;

uint8_t Reset(void)
{
	if (poketcg_request_boot_restart != NULL)
		poketcg_request_boot_restart();
	return wInitialA;
}
/* <<< factory Reset */
