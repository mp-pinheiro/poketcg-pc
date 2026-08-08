#include "home/default_palettes.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel_core.h"
#include "home/lcd.h"
#include "home/objects.h"
#include "home/palettes.h"
#include "home/switch_rom.h"
#include "mem.h"

void SetDefaultPalettes(void)
{
	gb_write8(wBGP_ADDR, 0xE4u);
	gb_write8(wOBP0_ADDR, 0xE4u);
	gb_write8(wOBP1_ADDR, 0xE4u);
	gb_write8(wTextBoxFrameType_ADDR, 4);
	uint8_t bank = gb_read8(hBankROM_ADDR);
	BankswitchROM(1);
	SetDefaultConsolePalettes();
	BankswitchROM(bank);
	FlushAllPalettes();
}

void Func_12871(void)
{
	ZeroObjectPositions();
	gb_write8(wVBlankOAMCopyToggle_ADDR, 1);
	Set_OBJ_8x8();
	SetDefaultPalettes();
	gb_write8(hSCX_ADDR, 0);
	gb_write8(hSCY_ADDR, 0);
	gb_write8(hWX_ADDR, 0);
	gb_write8(hWY_ADDR, 0);
	SetWindowOff();
}
