/* >>> part includes */
#include "home/status.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "generated/wram.h"
#include "home/print_stats.h"
#include "home/text_box.h"
#include "home/init_menu.h"
#include "home/labels.h"
#include "home/wait_keys.h"
#include "home/scenes.h"
#include "home/scripting.h"
/* <<< part includes_2 */
/* >>> part StatusScreenLabels */
#define StatusScreenLabels StatusScreenLabels_ADDR
/* <<< part StatusScreenLabels */
/* >>> part PAD_A */
#define PAD_A 0x01u
/* <<< part PAD_A */
/* >>> part PAD_B */
#define PAD_B 0x02u
/* <<< part PAD_B */
/* >>> part PAD_START */
#define PAD_START 0x08u
/* <<< part PAD_START */

/* >>> factory _PauseMenu_Status */
void _PauseMenu_Status(void)
{
	uint8_t saved_d291 = wd291;
	InitMenuRegs init = InitMenuScreen();
	wMedalScreenYOffset = 0u;
	DrawCollectedMedals();
	DrawRegularTextBox(&init.hl, 0u, 20u, 8u, 0u, 0u);
	(void)PrintLabels(StatusScreenLabels, 0u, 0u);
	SetMintSinglePalette(GetEventValue(EVENT_MEDAL_FLAGS) != 0u);
	DrawPauseMenuPlayerPortrait(1u, 1u); /* menus/status.asm:14 lb bc, 1, 1 */
	SetMintSinglePalette(0u);
	PrintAlbumProgress(12u, 4u);
	PrintPlayTime(13u, 6u);
	(void)FlashWhiteScreen();
	(void)WaitUntilKeysArePressed((uint8_t)(PAD_A | PAD_B | PAD_START));
	wd291 = saved_d291;
}
/* <<< factory _PauseMenu_Status */
