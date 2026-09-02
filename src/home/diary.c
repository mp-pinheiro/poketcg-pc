#include "home/diary.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/overworld.h"
#include "home/print_stats.h"
#include "home/text_box.h"
#include "home/init_menu.h"
#include "home/sound.h"
#include "home/labels.h"
#include "home/print_text.h"
#include "home/save.h"
#include "home/menus.h"
#include "generated/wram.h"
#define SFX_SAVE_GAME 0x56u
#define PlayerDiarySaveCancelText 0x0346u
#define PlayerDiarySaveConfirmText 0x0345u
#define PlayerDiarySaveQuestionText 0x0344u
/* <<< factory statics */

/* >>> factory _PauseMenu_Diary */
void _PauseMenu_Diary(void)
{
	uint8_t saved_d291 = wd291;
	InitMenuRegs init = InitMenuScreen();
	DrawRegularTextBox(&init.hl, 0u, 20u, 12u, 0u, 0u);
	LabelsResult labels = PrintLabels(0x40F7u, 0u, 0u);
	DrawPauseMenuPlayerPortrait(1u, 3u); /* menus/diary.asm:11 lb bc, 1, 3 */
	PrintAlbumProgress(12u, 8u);
	PrintPlayTime(13u, 10u);
	PrintMedalCount(16u, 6u, labels.d, labels.e, labels.hl);
	(void)FlashWhiteScreen();
	HandleYesOrNoMenuResult menu = YesOrNoMenuWithText_SetCursorToYes(PlayerDiarySaveQuestionText);
	uint16_t result_text = PlayerDiarySaveConfirmText;
	if ((menu.f & 0x10u) != 0u)
	{
		result_text = PlayerDiarySaveCancelText;
	}
	else
	{
		BackupPlayerPosition();
		SaveAndBackupData();
		PlaySFX(SFX_SAVE_GAME);
	}
	(void)PrintScrollableText_NoTextBoxLabel(result_text);
	wd291 = saved_d291;
}
/* <<< factory _PauseMenu_Diary */
