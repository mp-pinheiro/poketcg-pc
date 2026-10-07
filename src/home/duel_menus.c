/* >>> part includes */
#include "home/duel_menus.h"
#include "home/play_area.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "home/switch_rom.h"
#include "home/duel.h"
#include "generated/hram.h"
/* <<< part includes_2 */
/* >>> part BANK__DrawPlayersPrizeAndBenchCards */
#define BANK__DrawPlayersPrizeAndBenchCards 0x02u
/* <<< part BANK__DrawPlayersPrizeAndBenchCards */

/* >>> part includes_DRAW_PLAY_AREA_TO_PLACE_PRIZE_CARDS_BANK */
#include "generated/hram.h"
#include "home/switch_rom.h"
#include "home/duel.h"
/* <<< part includes_DRAW_PLAY_AREA_TO_PLACE_PRIZE_CARDS_BANK */
/* >>> part DRAW_PLAY_AREA_TO_PLACE_PRIZE_CARDS_BANK */
#define DRAW_PLAY_AREA_TO_PLACE_PRIZE_CARDS_BANK 0x02u
/* <<< part DRAW_PLAY_AREA_TO_PLACE_PRIZE_CARDS_BANK */

/* >>> part includes_BANK__DrawYourOrOppPlayAreaScreen */
#include "home/switch_rom.h"
#include "home/menus.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"
/* <<< part includes_BANK__DrawYourOrOppPlayAreaScreen */
/* >>> part BANK__DrawYourOrOppPlayAreaScreen */
#define BANK__DrawYourOrOppPlayAreaScreen 0x02u
/* <<< part BANK__DrawYourOrOppPlayAreaScreen */

/* >>> part includes_BANK__DrawAIPeekScreen */
#include "home/switch_rom.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"
/* <<< part includes_BANK__DrawAIPeekScreen */
/* >>> part BANK__DrawAIPeekScreen */
#define BANK__DrawAIPeekScreen 0x02u
/* <<< part BANK__DrawAIPeekScreen */

/* >>> part includes_BANK__SelectPrizeCards */
#include "home/switch_rom.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"
/* <<< part includes_BANK__SelectPrizeCards */
/* >>> part BANK__SelectPrizeCards */
#define BANK__SelectPrizeCards 0x02u
/* <<< part BANK__SelectPrizeCards */

/* >>> part includes_BANK__HandlePeekSelection */
#include "generated/hram.h"
#include "home/duel.h"
#include "home/overworld.h"
#include "home/switch_rom.h"
/* <<< part includes_BANK__HandlePeekSelection */
/* >>> part BANK__HandlePeekSelection */
#define BANK__HandlePeekSelection 0x02u
/* <<< part BANK__HandlePeekSelection */

/* >>> part includes_tail */
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/overworld.h"
/* <<< part includes_tail */

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

/* >>> factory SelectPrizeCards */
void SelectPrizeCards(uint8_t a)
{
	wNumberOfPrizeCardsToSelect = a;
	uint8_t saved_bank = hBankROM;
	BankswitchROM(BANK__SelectPrizeCards);
	_SelectPrizeCards();
	BankswitchROM(saved_bank);
}
/* <<< factory SelectPrizeCards */

/* >>> factory HandlePeekSelection */
HandlePeekSelectionV2Result HandlePeekSelection(uint8_t f)
{
	uint8_t saved_bank = hBankROM;
	BankswitchROM(BANK__HandlePeekSelection);
	HandlePeekSelectionResult inner = _HandlePeekSelection();
	BankswitchROM(saved_bank);
	return (HandlePeekSelectionV2Result){inner.a, f};
}
/* <<< factory HandlePeekSelection */

/* >>> factory OpenDuelCheckMenu */
/* duel_menus.asm:1-9: the menu itself was missing between the bankswitch and
 * the restore, so nothing below it could ever run. */
void OpenDuelCheckMenu(void)
{
	uint8_t saved_bank = hBankROM;
	BankswitchROM(2u);
	_OpenDuelCheckMenu();
	BankswitchROM(saved_bank);
}
/* <<< factory OpenDuelCheckMenu */

/* >>> factory OpenInPlayAreaScreen_FromSelectButton */
uint8_t OpenInPlayAreaScreen_FromSelectButton(void)
{
	uint8_t saved_bank = hBankROM;
	OpenInPlayAreaScreenResult screen;

	BankswitchROM(6u);
	wInPlayAreaFromSelectButton = 1u;
	/* duel_menus.asm:11-20: the screen itself was missing between the flag
	 * write and the bank restore. */
	screen = OpenInPlayAreaScreen();
	BankswitchROM(saved_bank);
	return screen.f;
}
/* <<< factory OpenInPlayAreaScreen_FromSelectButton */
