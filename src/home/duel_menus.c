#include "home/duel_menus.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/switch_rom.h"
#include "home/duel.h"
#include "generated/hram.h"
#define BANK__DrawPlayersPrizeAndBenchCards 0x02u

#include "generated/hram.h"
#include "home/switch_rom.h"
#include "home/duel.h"
#define DRAW_PLAY_AREA_TO_PLACE_PRIZE_CARDS_BANK 0x02u

#include "home/switch_rom.h"
#include "home/menus.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define BANK__DrawYourOrOppPlayAreaScreen 0x02u

#include "home/switch_rom.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define BANK__DrawAIPeekScreen 0x02u
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

/* >>> factory DrawPlayAreaToPlacePrizeCards */
void DrawPlayAreaToPlacePrizeCards(void)
{
	uint8_t saved_bank = hBankROM;
	BankswitchROM(DRAW_PLAY_AREA_TO_PLACE_PRIZE_CARDS_BANK);
	_DrawPlayAreaToPlacePrizeCards();
	BankswitchROM(saved_bank);
}
/* <<< factory DrawPlayAreaToPlacePrizeCards */

/* >>> factory DrawYourOrOppPlayAreaScreen_Bank0 */
void DrawYourOrOppPlayAreaScreen_Bank0(uint16_t hl)
{
	wCheckMenuPlayAreaWhichDuelist = (uint8_t)(hl >> 8);
	wCheckMenuPlayAreaWhichLayout = (uint8_t)hl;
	uint8_t saved_bank = hBankROM;
	BankswitchROM(BANK__DrawYourOrOppPlayAreaScreen);
	_DrawYourOrOppPlayAreaScreen();
	(void)DrawWideTextBox();
	BankswitchROM(saved_bank);
}
/* <<< factory DrawYourOrOppPlayAreaScreen_Bank0 */

/* >>> factory DrawAIPeekScreen */
/* duel_menus.asm:67-83 */
DrawAIPeekScreenResult DrawAIPeekScreen(uint8_t a, uint8_t f)
{
	uint8_t saved_bank = hBankROM;
	BankswitchROM(BANK__DrawAIPeekScreen);
	_DrawAIPeekScreen(a);
	BankswitchROM(saved_bank);
	return (DrawAIPeekScreenResult){saved_bank, f};
}
/* <<< factory DrawAIPeekScreen */
