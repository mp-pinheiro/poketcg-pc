/* >>> part includes */
#include "home/input.h"

#include "home/serial.h"
#include "mem.h"
#include "generated/hram.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "generated/wram.h"
/* <<< part includes_2 */

/* >>> part JOYP */
#define JOYP 0xFF00u
/* <<< part JOYP */
/* >>> part JOYP_GET_BUTTONS */
#define JOYP_GET_BUTTONS 0x10u
/* <<< part JOYP_GET_BUTTONS */
/* >>> part JOYP_GET_CTRL_PAD */
#define JOYP_GET_CTRL_PAD 0x20u
/* <<< part JOYP_GET_CTRL_PAD */
/* >>> part JOYP_GET_NONE */
#define JOYP_GET_NONE 0x30u
/* <<< part JOYP_GET_NONE */
/* >>> part JOYP_INPUTS */
#define JOYP_INPUTS 0x0Fu
/* <<< part JOYP_INPUTS */
/* >>> part PAD_A */
#define PAD_A 0x01u
/* <<< part PAD_A */
/* >>> part PAD_B */
#define PAD_B 0x02u
/* <<< part PAD_B */
/* >>> part PAD_SELECT */
#define PAD_SELECT 0x04u
/* <<< part PAD_SELECT */
/* >>> part PAD_START */
#define PAD_START 0x08u
/* <<< part PAD_START */
/* >>> part PAD_BUTTONS */
#define PAD_BUTTONS (PAD_A | PAD_B | PAD_SELECT | PAD_START)
/* <<< part PAD_BUTTONS */

/* >>> part read_joypad */
static uint8_t read_joypad(void)
{
	return gb_read8(JOYP);
}
/* <<< part read_joypad */

/* >>> factory SaveButtonsHeld */
void SaveButtonsHeld(uint8_t c)
{
	gb_write8(hKeysHeld_ADDR, c);
	gb_write8(JOYP, JOYP_GET_NONE);
}
/* <<< factory SaveButtonsHeld */
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

/* >>> factory ClearJoypad */
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
/* <<< factory ClearJoypad */

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
