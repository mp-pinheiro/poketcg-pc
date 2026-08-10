#include "home/init_menu.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/color.h"
#include "home/default_palettes.h"
#include "home/empty_screen.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/objects.h"
#include "home/palettes.h"
#include "home/process_text.h"
#include "home/switch_sram.h"
#include "home/tiles.h"
#include "mem.h"

#define rSCX 0xFF43u
#define rSCY 0xFF42u
#define LCDC_ON 0x80u

InitMenuRegs InitMenuScreen(void)
{
	TileCopyResult symbols;
	InitMenuRegs result;

	wTileMapFill = 0;
	EmptyScreen();
	symbols = LoadSymbolsFont();
	SetupText(0x30, 0x7F);
	Set_OBJ_8x8();
	if (!(wLCDC & LCDC_ON)) {
		gb_write8(rSCX, 0);
		gb_write8(rSCY, 0);
	}
	SetDefaultPalettes();
	ZeroObjectPositions();
	result.b = 0;
	result.c = 0x10;
	result.d = (uint8_t)(symbols.de >> 8);
	result.e = (uint8_t)symbols.de;
	result.hl = 0x6CE8u;
	return result;
}

InitMenuRegs FlashWhiteScreen(void)
{
	InitMenuRegs result;
	uint8_t object_palettes[64];
	uint8_t bank = hBankSRAM;
	for (uint8_t i = 0; i < 64; i++)
		object_palettes[i] = gb_read8((uint16_t)(wObjectPalettesCGB_ADDR + i));

	BankswitchSRAM(1);
	CopyPalsToSRAMBuffer();
	DisableSRAM();
	SetWhitePalettes();
	FlushAllPalettes();
	EnableLCD();
	DoFrameIfLCDEnabled();
	LoadPalsFromSRAMBuffer();
	for (uint8_t i = 0; i < 64; i++)
		wObjectPalettesCGB_PTR[i] = object_palettes[i];
	FlushAllPalettes();
	BankswitchSRAM(bank);
	DisableSRAM();
	result.b = 0;
	result.c = 0x10;
	result.d = 0x93;
	result.e = 0x80;
	result.hl = 0x6CE8u;
	return result;
}

