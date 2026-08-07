#include "home/input.h"

#include "mem.h"
#include "generated/hram.h"

#define JOYP 0xFF00u
#define JOYP_GET_BUTTONS 0x10u
#define JOYP_GET_CTRL_PAD 0x20u
#define JOYP_GET_NONE 0x30u
#define JOYP_INPUTS 0x0Fu

static uint8_t read_joypad(void)
{
	return (uint8_t)(gb_read8(JOYP) | JOYP_INPUTS);
}

void SaveButtonsHeld(uint8_t c)
{
	gb_write8(hKeysHeld_ADDR, c);
	gb_write8(JOYP, JOYP_GET_NONE);
}

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
	SaveButtonsHeld(c);
}

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
