#include "home/start.h"

#include "generated/wram.h"
#include "home/menus.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "home/text_box.h"
/* >>> factory statics */
#include "home/start.h"
#include "home/save.h"
#include "home/core.h"
#include "generated/wram.h"
#define FALSE 0x00u
#define TRUE 0x01u

#include "generated/wram.h"
#include "mem.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "home/print_stats.h"
#include "home/text_box.h"
#define ContinueFromDiarySummaryText 0x0370u
#define StartANewGameText 0x0371u
#define TheGameWillContinueFromThePointInTheDuelText 0x0372u
#define WhenYouCardPopWithFriendText 0x036fu
#define MAP_NAMES 0x7080u

#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/load_animation.h"
#include "home/init_menu.h"
#include "home/print_text.h"
#include "home/menus.h"
#include "generated/wram.h"
#define ContinueFromDiaryText 0x0377u
#define DataExistsWhenPowerWasTurnedOFFDuringDuelText 0x0376u
/* <<< factory statics */

#define CONSOLE_CGB 0x02u
#define DISCLAIMER_TEXT_ID 0x0378u
#define SYM_CURSOR_D 0x2Fu
#define SYM_BOX_BOTTOM 0x1Du

uint8_t ShowCardPopCGBDisclaimer(void)
{
	uint16_t box = 0;
	if (wConsole == CONSOLE_CGB)
		return 0xC0u;

	DrawRegularTextBox(&box, 0, 20, 8, 0, 10);
	InitTextPrinting(1, 12);
	(void)PrintTextNoDelay(DISCLAIMER_TEXT_ID, 1, 12);
	(void)SetCursorParametersForTextBox(18, 17, SYM_CURSOR_D, SYM_BOX_BOTTOM);
	return 0x10u;
}

/* >>> factory CheckIfHasSaveData */
CheckIfHasSaveDataResult CheckIfHasSaveData(void)
{
	ValidateResult first = ValidateBackupGeneralSaveData();
	uint8_t has_save = (first.f & 0x10u) ? TRUE : FALSE;
	wHasSaveData = has_save;
	if (has_save != FALSE) {
		uint8_t flags = ValidateSavedNonLinkDuelData();
		wHasDuelSaveData = (flags & 0x10u) ? FALSE : TRUE;
	} else {
		wHasDuelSaveData = FALSE;
	}
	ValidateResult final = ValidateBackupGeneralSaveData();
	return (CheckIfHasSaveDataResult){final.a, final.f};
}
/* <<< factory CheckIfHasSaveData */

/* >>> factory PrintStartMenuDescriptionText */
PrintStartMenuDescriptionTextResult PrintStartMenuDescriptionText(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t saved_b = b;
	uint8_t saved_c = c;
	uint8_t saved_d = d;
	uint8_t saved_e = e;
	uint16_t box = 0;
	uint8_t menu_item = wCurMenuItem;
	uint8_t dispatch;
	uint8_t out_a = menu_item;
	if (menu_item != wCurHighlightedStartMenuItem) {
		dispatch = menu_item;
		if (wHasSaveData == 0u)
			dispatch = (uint8_t)(dispatch + 2u);
		DrawRegularTextBox(&box, 0u, 20u, 8u, 0u, 10u);
		switch (dispatch) {
		case 1u: {
			InitTextPrinting(1u, 12u);
			TextResult text = PrintTextNoDelay(WhenYouCardPopWithFriendText, 1u, 12u);
			out_a = text.a;
			break;
		}
		case 2u: {
			uint8_t map = wCurOverworldMap;
			uint8_t offset = (uint8_t)(map + map);
			uint16_t src = (uint16_t)(MAP_NAMES - 2u + offset);
			gb_write8(wTxRam2_ADDR, gb_read8(src));
			gb_write8((uint16_t)(wTxRam2_ADDR + 1u), gb_read8((uint16_t)(src + 1u)));
			gb_write8(wTxRam3_ADDR, wMedalCount);
			gb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0u);
			InitTextPrinting(1u, 10u);
			TextResult text = PrintTextNoDelay(ContinueFromDiarySummaryText, 1u, 10u);
			out_a = text.a;
			PrintAlbumProgress_SkipGetProgress(wTotalNumCardsCollected, wTotalNumCardsToCollect, 9u, 14u);
			PrintPlayTime_SkipUpdateTime(10u, 16u);
			break;
		}
		case 3u: {
			InitTextPrinting(1u, 12u);
			TextResult text = PrintTextNoDelay(StartANewGameText, 1u, 12u);
			out_a = text.a;
			break;
		}
		case 4u: {
			InitTextPrinting(1u, 12u);
			TextResult text = PrintTextNoDelay(TheGameWillContinueFromThePointInTheDuelText, 1u, 12u);
			out_a = text.a;
			break;
		}
		default:
			break;
		}
	}
	uint8_t out_f = (menu_item == wCurHighlightedStartMenuItem) ? 0xC0u : f;
	wCurHighlightedStartMenuItem = menu_item;
	(void)a;
	(void)hl;
	return (PrintStartMenuDescriptionTextResult){out_a, out_f, saved_b, saved_c, saved_d, saved_e};
}
/* <<< factory PrintStartMenuDescriptionText */

/* >>> factory AskToContinueFromDiaryWithDuelData */
AskToContinueFromDiaryWithDuelDataResult AskToContinueFromDiaryWithDuelData(void)
{
	uint8_t a = wHasDuelSaveData;
	if (a == 0u)
		return (AskToContinueFromDiaryWithDuelDataResult){a, 0x80u};

	DisableLCD();
	(void)InitMenuScreen();
	EnableAndClearSpriteAnimations();
	(void)FlashWhiteScreen();
	DoFrameIfLCDEnabled();
	(void)PrintScrollableText_NoTextBoxLabel(DataExistsWhenPowerWasTurnedOFFDuringDuelText);
	HandleYesOrNoMenuResult menu = YesOrNoMenuWithText(ContinueFromDiaryText);
	if ((menu.f & 0x10u) != 0u)
		return (AskToContinueFromDiaryWithDuelDataResult){menu.a, menu.f};
	return (AskToContinueFromDiaryWithDuelDataResult){menu.a, menu.a == 0u ? 0x80u : 0u};
}
/* <<< factory AskToContinueFromDiaryWithDuelData */
