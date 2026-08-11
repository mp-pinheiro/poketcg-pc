#include "home/game_loop.h"

#include "generated/wram.h"
#include "home/duel_core.h"
#include "home/lcd.h"
#include "home/process_text.h"
#include "home/tiles.h"

void SetupResetBackUpRamScreen(void)
{
	wTileMapFill = 0;
	DisableLCD();
	LoadSymbolsFont();
	SetDefaultConsolePalettes();
	SetupText(0x38, 0x7F);
}
