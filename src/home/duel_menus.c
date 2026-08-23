#include "home/duel_menus.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/switch_rom.h"
#include "home/duel.h"
#include "generated/hram.h"
#define BANK__DrawPlayersPrizeAndBenchCards 0x02u
/* <<< factory statics */

/* >>> factory DrawPlayersPrizeAndBenchCards */
void DrawPlayersPrizeAndBenchCards(void)
{
	uint8_t saved_bank = hBankROM;
	BankswitchROM(BANK__DrawPlayersPrizeAndBenchCards);
	_DrawPlayersPrizeAndBenchCards();
	BankswitchROM(saved_bank);
}
/* <<< factory DrawPlayersPrizeAndBenchCards */
