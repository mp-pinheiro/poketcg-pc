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

#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#include "home/copy.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/load_animation.h"
#include "home/init_menu.h"
#include "home/menus.h"
#include "home/labels.h"
#include "home/sound.h"
#include "home/process_text.h"
#include "home/random.h"
#define DOUBLE_SPACED 0x00u
#define MUSIC_PC_MAIN_MENU 0x06u
#define SYM_CURSOR_R 0x0Fu
#define SYM_SPACE 0x00u

#include "home/color.h"
#include "home/play_animation.h"
#define IsCrazyAboutPokemonAndPokemonCardCollectingText 0x0379u
#define HANDLEALLSPRITEANIMATIONS_ADDR 0x3CB4u

#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/load_animation.h"
#include "home/init_menu.h"
#include "home/save.h"
#include "home/print_text.h"
#include "home/menus.h"
#include "generated/wram.h"
#define AllDataWasDeletedText 0x0375u
#define OKToDeleteTheDataText 0x0374u
#define SavedDataAlreadyExistsText 0x0373u

#include "home/intro.h"
#include "home/intro_sequence_commands.h"
#include "home/load_animation.h"
#include "home/sound.h"
#include "generated/wram.h"
#define MUSIC_STOP 0x00u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/clear_sram.h"
#include "home/dma.h"
#include "home/lcd.h"
#include "home/overworld.h"
#include "home/frames.h"
#include "home/main_menu.h"
#include "home/serial.h"
#include "home/setup.h"
#include "home/sound.h"
#include "home/switch_sram.h"
#include "home/time.h"
#include "mem.h"
#include "runtime.h"
#define BANK_GAME_LOOP 0x01u
#define rIF 0xFF0Fu
#define rIE 0xFFFFu
#define PAD_A 0x01u
#define PAD_START 0x08u
#define SFX_CONFIRM 0x02u
#define START_MENU_CARD_POP 0x00u
#define START_MENU_CONTINUE_FROM_DIARY 0x01u
#define START_MENU_NEW_GAME 0x02u
#define START_MENU_CONTINUE_DUEL 0x03u
#define rVBK 0xFF4Fu
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

/* >>> factory HandleStartMenu */
void HandleStartMenu(void)
{
	PlaySong(MUSIC_PC_MAIN_MENU);
	DisableLCD();
	(void)InitMenuScreen();
	(void)SetupText(0x30u, 0x8Fu);
	EnableAndClearSpriteAnimations();
	wLineSeparation = DOUBLE_SPACED;
	DrawPlayerPortrait(14u, 1u); /* menus/start.asm:229 lb bc, 14, 1 */
	static const uint8_t params[17] = {
		0x00u, 0x00u, 0x0Eu, 0x04u, 0x02u, 0x02u,
		0x6Cu, 0x03u, 0xFFu, 0x01u, 0x02u, 0x02u, 0x01u,
		SYM_CURSOR_R, SYM_SPACE, 0x00u, 0x00u
	};
	for (uint8_t i = 0u; i < 17u; ++i)
		gb_write8((uint16_t)(wStartMenuParams_ADDR + i), params[i]);
	uint8_t item_count = 1u;
	uint8_t box_height = 4u;
	uint8_t text_id = 0x6Cu;
	if (wHasSaveData != 0u) {
		item_count = (uint8_t)(item_count + 2u);
		box_height = (uint8_t)(box_height + 4u);
		text_id = (uint8_t)(text_id + 1u);
		if (wHasDuelSaveData != 0u) {
			item_count = (uint8_t)(item_count + 1u);
			box_height = (uint8_t)(box_height + 2u);
			text_id = (uint8_t)(text_id + 1u);
		}
	}
	gb_write8((uint16_t)(wStartMenuParams_ADDR + 12u), item_count);
	gb_write8((uint16_t)(wStartMenuParams_ADDR + 3u), box_height);
	gb_write8((uint16_t)(wStartMenuParams_ADDR + 6u), text_id);
	gb_write8((uint16_t)(wStartMenuParams_ADDR + 7u), 0x03u);
	wTitleScreenIgnoreInputCounter = 0xFFu;
	uint8_t selected = wLastSelectedStartMenuItem;
	if (selected >= 4u && wHasSaveData != 0u)
		selected = 1u;
	InitAndPrintMenu(wStartMenuParams_ADDR, selected);
	/* start.asm:104-141: InitAndPrintMenu's menu-item print (PrintTextNoDelay
	 * -> Func_235e) spans a VBlank period on the reference -- service 1008
	 * interrupts it mid-draw (1150-frame trace: wvbc 1008; the reference
	 * burns 12 no-advance steps 997-1008 vs native 9). Consume it once per
	 * menu opening, before the white flash. */
	frame_boundary_consume_services(1u);
	(void)FlashWhiteScreen();
	runtime_mark_event(RUNTIME_EVENT_START_MENU_READY);
	for (;;) { /* .wait_input */
		DoFrameIfLCDEnabled();
		(void)UpdateRNGSources();
		HandleMenuInputResult input = HandleMenuInput();
		PrintStartMenuDescriptionTextResult description = PrintStartMenuDescriptionText(input.a, input.f, 0u, 0u, 0u, input.e, 0u);
		(void)description;
		if ((input.f & 0x10u) == 0u)
			continue;
		if (hCurMenuItem != input.e)
			continue;
		wLastSelectedStartMenuItem = hCurMenuItem;
		uint8_t choice = input.e;
		if (wHasSaveData == 0u)
			choice = (uint8_t)(choice + 2u);
		wStartMenuChoice = choice;
		return;
	}
}
/* <<< factory HandleStartMenu */

/* >>> factory DrawPlayerPortraitAndPrintNewGameText */
void DrawPlayerPortraitAndPrintNewGameText(void)
{
	DisableLCD();
	LoadConsolePaletteData();
	(void)InitMenuScreen();
	EnableAndClearSpriteAnimations();
	(void)SetDoFrameFunction(HANDLEALLSPRITEANIMATIONS_ADDR);
	DrawPlayerPortrait(7u, 3u); /* menus/start.asm:410 lb bc, 7, 3 */
	(void)FadeScreenFromWhite();
	DoFrameIfLCDEnabled();
	(void)PrintScrollableText_NoTextBoxLabel(IsCrazyAboutPokemonAndPokemonCardCollectingText);
	(void)ResetDoFrameFunction(0u);
	EnableAndClearSpriteAnimations();
}
/* <<< factory DrawPlayerPortraitAndPrintNewGameText */

/* >>> factory DeleteSaveDataForNewGame */
uint8_t DeleteSaveDataForNewGame(void)
{
	if (wHasSaveData == 0u)
		return 0x00u; /* ret z */

	DisableLCD();
	(void)InitMenuScreen();
	EnableAndClearSpriteAnimations();
	(void)FlashWhiteScreen();
	DoFrameIfLCDEnabled();
	(void)PrintScrollableText_NoTextBoxLabel(SavedDataAlreadyExistsText);
	HandleYesOrNoMenuResult result = YesOrNoMenuWithText(OKToDeleteTheDataText);
	if ((result.f & 0x10u) != 0u)
		return 0x10u; /* ret c: quit if chose "no" */
	InvalidateSaveData();
	(void)PrintScrollableText_NoTextBoxLabel(AllDataWasDeletedText);
	return 0x00u; /* or a */
}
/* <<< factory DeleteSaveDataForNewGame */

/* >>> factory HandleTitleScreen */
void HandleTitleScreen(void)
{
	if (!frame_boundary_is_installed()) {
		/* Probe world: the oracle stops pre-ret right before the intro
		 * call (start.asm:16); keep the bounded opening prefix. */
		if (wLastSelectedStartMenuItem == 0u)
			return;
		PlaySong(MUSIC_STOP);
		EnableAndClearSpriteAnimations();
		return;
	}

	if (wLastSelectedStartMenuItem != 0u) {
		for (;;) { /* .play_opening */
			PlaySong(MUSIC_STOP);
			EnableAndClearSpriteAnimations();
			PlayIntroSequence();
			LoadTitleScreenSprites();
			/* start.asm:17 calls LoadTitleScreenSprites with the LCD
			 * back on (intro.asm:52): the seven 4-tile orb copies
			 * through CopyGfxData's hblank-gated HRAM copier plus the
			 * sprite-buffer work fill most of a frame period, and the
			 * reference's ISR services twice while this chain is still
			 * running -- service 657 interrupts CopyGfxData.hblank_copy
			 * inside the GRASS copy, service 658 lands at CopyGfxData+3
			 * of the PSYCHIC copy, both inside DoFrame interval 652
			 * (700/1150-frame reference traces). The intro-side call
			 * (intro.c) runs with the LCD off and crosses nothing.
			 * Model both services here. */
			frame_boundary_consume_services(2u);
			runtime_mark_event(RUNTIME_EVENT_TITLE_READY);
			wTitleScreenOrbCounter = 0u;
			wTitleScreenIgnoreInputCounter = 0x3Cu;
			uint8_t start_menu = 0u;
			while (start_menu == 0u) { /* .loop */
				DoFrameIfLCDEnabled();
				(void)UpdateRNGSources();
				(void)AnimateRandomTitleScreenOrb();
				wTitleScreenOrbCounter++;
				if (AssertSongFinished() == 0u) {
					FadeScreenToWhite();
					break; /* jr .play_opening: replay opening */
				}
				if (wTitleScreenIgnoreInputCounter != 0u) {
					wTitleScreenIgnoreInputCounter--;
					continue;
				}
				if ((hKeysPressed & (PAD_A | PAD_START)) == 0u)
					continue;
				PlaySFX(SFX_CONFIRM);
				FadeScreenToWhite();
				start_menu = 1u; /* key fallthrough: .start_menu */
			}
			if (start_menu != 0u)
				break;
		}
	}

	for (;;) { /* jr c, HandleTitleScreen re-entries (start.asm:63-76) */
		(void)CheckIfHasSaveData();
		HandleStartMenu();
		if (wStartMenuChoice == START_MENU_NEW_GAME) {
			if ((DeleteSaveDataForNewGame() & 0x10u) != 0u)
				continue;
			break; /* jr .card_pop: not Card Pop! -> .continue_duel */
		}
		if (wStartMenuChoice == START_MENU_CONTINUE_FROM_DIARY) {
			AskToContinueFromDiaryWithDuelDataResult answer =
				AskToContinueFromDiaryWithDuelData();
			if ((answer.f & 0x10u) != 0u)
				continue;
			break;
		}
		if (wStartMenuChoice == START_MENU_CARD_POP) {
			if ((ShowCardPopCGBDisclaimer() & 0x10u) != 0u)
				continue;
			break; /* falls into .continue_duel */
		}
		break; /* .continue_duel */
	}
	ResetDoFrameFunction(0u);
	EnableAndClearSpriteAnimations();
}
/* <<< factory HandleTitleScreen */

/* >>> factory Start */
void Start(uint8_t a)
{
	gb_write8(rIF, 0);
	gb_write8(rIE, 0);
	(void)ZeroRAM();
	BankswitchROM(1u);
	BankswitchSRAM(0u);
	hBankVRAM = 0u;
	gb_write8(rVBK, 0xFEu);
	DisableLCD();
	wInitialA = a;
	(void)DetectConsole(a);
	wTileMapFill = 0x20u;
	(void)SetupVRAM();
	(void)SetupRegisters();
	(void)SetupPalettes(0u, 0u, 0u, 0u);
	SetupSound();
	(void)SetupTimer();
	ResetSerial();
	CopyDMAFunction();
	ValidateSRAM();
	BankswitchROM(BANK_GAME_LOOP);
}
/* <<< factory Start */
