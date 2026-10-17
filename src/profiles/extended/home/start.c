/* >>> part includes_BANK_GAME_LOOP */
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/load_animation.h"
#include "home/init_menu.h"
#include "home/save.h"
#include "home/print_text.h"
#include "home/menus.h"
#include "generated/wram.h"

#include "home/intro.h"
#include "home/intro_sequence_commands.h"
#include "home/game_loop.h"
#include "home/load_animation.h"
#include "home/sound.h"
#include "generated/wram.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/clear_sram.h"
#include "home/dma.h"
#include "home/lcd.h"
#include "home/overworld.h"
#include "home/frames.h"
#include "home/main_menu.h"
#include "home/setup.h"
#include "home/sound.h"
#include "home/switch_sram.h"
#include "home/time.h"
#include "mem.h"
#include "runtime.h"
/* <<< part includes_BANK_GAME_LOOP */
/* --- part DISCLAIMER_TEXT_ID */
/* --- part SYM_BOX_BOTTOM */
/* --- factory ShowCardPopCGBDisclaimer */
/* >>> factory CheckIfHasSaveData */
CheckIfHasSaveDataResult CheckIfHasSaveData(void)
{
	ValidateResult first = ValidateBackupGeneralSaveData();
	uint8_t has_save = (first.f & 0x10u) ? TRUE : FALSE;
	wHasSaveData = has_save;
	if (has_save != FALSE) {
		ValidateSavedDuelDataResult duel = ValidateSavedDuelData(sCurrentDuel_ADDR);
		uint8_t flags = duel.f;
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
	if (runtime_pc_options_enabled() &&
	    menu_item == start_menu_pc_index()) {
		if (menu_item != wCurHighlightedStartMenuItem) {
			DrawRegularTextBox(&box, 0u, 20u, 8u, 0u, 10u);
			print_host_text("Configure PC options.", 1u, 12u);
		}
		uint8_t out_f = (menu_item == wCurHighlightedStartMenuItem) ? 0xC0u : f;
		wCurHighlightedStartMenuItem = menu_item;
		(void)a;
		(void)hl;
		return (PrintStartMenuDescriptionTextResult){out_a, out_f,
			saved_b, saved_c, saved_d, saved_e};
	}
	if (menu_item != wCurHighlightedStartMenuItem) {
		dispatch = menu_item;
		if (wHasSaveData == 0u)
			dispatch = (uint8_t)(dispatch + 1u);
		DrawRegularTextBox(&box, 0u, 20u, 8u, 0u, 10u);
		switch (dispatch) {
		case 0u: {
			uint8_t map = wCurOverworldMap;
			uint8_t offset = (uint8_t)(map + map);
			uint16_t src = (uint16_t)(OVERWORLD_MAP_NAMES + offset);
			gb_write8(wTxRam2_ADDR, gb_read8(src));
			gb_write8((uint16_t)(wTxRam2_ADDR + 1u), gb_read8((uint16_t)(src + 1u)));
			gb_write8(wTxRam3_ADDR, wMedalCount);
			gb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0u);
			InitTextPrinting(1u, 10u);
			TextResult text = PrintTextNoDelay(ContinueFromDiarySummaryText, 1u, 10u);
			(void)text;
			PrintAlbumProgress_SkipGetProgress(9u, 14u,
				gb_read8((uint16_t)(wTotalNumCardsCollected_ADDR + 1u)),
				gb_read8(wTotalNumCardsCollected_ADDR),
				(uint16_t)(gb_read8(wTotalNumCardsToCollect_ADDR) |
					((uint16_t)gb_read8((uint16_t)(wTotalNumCardsToCollect_ADDR + 1u)) << 8)));
			PrintPlayTime_SkipUpdateTime(10u, 16u);
			break;
		}
		case 1u: {
			InitTextPrinting(1u, 12u);
			TextResult text = PrintTextNoDelay(StartANewGameText, 1u, 12u);
			(void)text;
			break;
		}
		case 2u: {
			InitTextPrinting(1u, 12u);
			TextResult text = PrintTextNoDelay(TheGameWillContinueFromThePointInTheDuelText, 1u, 12u);
			(void)text;
			break;
		}
		default:
			break;
		}
	}
	/* start.asm:267-268: every path falls through .skip, which reloads
	 * `a` from wCurMenuItem, so the dispatched print's own return value
	 * never reaches the caller. The dispatch path's F is the flag state
	 * the printed branch left behind; PrintTextNoDelay does not surface
	 * it (TextResult has no f member, src/home/print_text.h:54-57), so
	 * only the skip path's F is modeled here. */
	uint8_t out_f = (menu_item == wCurHighlightedStartMenuItem) ? 0xC0u : f;
	wCurHighlightedStartMenuItem = menu_item;
	(void)a;
	(void)hl;
	return (PrintStartMenuDescriptionTextResult){out_a, out_f, saved_b, saved_c, saved_d, saved_e};
}
/* <<< factory PrintStartMenuDescriptionText */
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
		(uint8_t)NewGameText, (uint8_t)(NewGameText >> 8), 0xFFu, 0x01u, 0x02u, 0x02u, 0x01u,
		SYM_CURSOR_R, SYM_SPACE, 0x00u, 0x00u
	};
	for (uint8_t i = 0u; i < 17u; ++i)
		gb_write8((uint16_t)(wStartMenuParams_ADDR + i), params[i]);
	static const uint16_t text_ids[3] = {
		NewGameText, ContinueDiaryNewGameText, ContinueDiaryNewGameContinueDuelText
	};
	uint8_t item_count = 1u;
	uint8_t box_height = 4u;
	uint8_t e = 0u;
	if (wHasSaveData != 0u) {
		e++;
		item_count++;
		box_height = (uint8_t)(box_height + 2u);
		if (wHasDuelSaveData != 0u) {
			e++;
			item_count++;
			box_height = (uint8_t)(box_height + 2u);
		}
	}
	uint16_t text_id = text_ids[e];
	uint8_t pc_options = (uint8_t)runtime_pc_options_enabled();
	uint8_t native_item_count = item_count;
	uint8_t list_top = 2u;
	if (pc_options != 0u) {
		item_count++;
		box_height = (uint8_t)(box_height + 2u);
		if (item_count == 5u) {
			list_top = 1u;
			box_height = 11u;
		}
	}
	gb_write8((uint16_t)(wStartMenuParams_ADDR + 5u), list_top);
	gb_write8((uint16_t)(wStartMenuParams_ADDR + 10u), list_top);
	gb_write8((uint16_t)(wStartMenuParams_ADDR + 12u), item_count);
	gb_write8((uint16_t)(wStartMenuParams_ADDR + 3u), box_height);
	gb_write8((uint16_t)(wStartMenuParams_ADDR + 6u), (uint8_t)text_id);
	gb_write8((uint16_t)(wStartMenuParams_ADDR + 7u), (uint8_t)(text_id >> 8));
	wTitleScreenIgnoreInputCounter = 0xFFu;
	uint8_t selected = wLastSelectedStartMenuItem;
	if (selected >= 4u)
		selected = 0u;
	InitAndPrintMenu(wStartMenuParams_ADDR, selected);
	if (pc_options != 0u)
		print_host_text("PC OPTIONS", 2u,
			(uint8_t)(list_top + native_item_count * 2u));
	/* start.asm:104-141: InitAndPrintMenu's menu-item print (PrintTextNoDelay
	 * -> Func_235e) spans a VBlank period on the reference -- service 1008
	 * interrupts it mid-draw (1150-frame trace: wvbc 1008; the reference
	 * burns 12 no-advance steps 997-1008 vs native 9). Consume it once per
	 * menu opening, before the white flash. */
	/* start.asm:104-141: the description print spans two service periods
	 * on the reference (cursor+box in one, text body in the next;
	 * 1150-frame trace: wvbc 1007 mid-box, 1008 mid-text). */
	frame_boundary_consume_services(2u);
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
		if (pc_options != 0u && choice == native_item_count) {
			wStartMenuChoice = START_MENU_PC_OPTIONS;
			return;
		}
		if (wHasSaveData == 0u)
			choice = (uint8_t)(choice + 1u);
		wStartMenuChoice = choice;
		return;
	}
}
/* <<< factory HandleStartMenu */
/* >>> factory DrawPlayerPortraitAndPrintNewGameText */
void DrawPlayerPortraitAndPrintNewGameText(void)
{
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
		PlayIntroSequence();
		return;
	}

title_screen:
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

	(void)CheckIfHasSaveData();
	if (runtime_pc_options_enabled() && wHasSaveData != 0u)
		LoadEventsFromSRAM();
	HandleStartMenu();
	if (wStartMenuChoice == START_MENU_PC_OPTIONS) {
		run_pc_options_from_title();
		wLastSelectedStartMenuItem = 0u;
		goto title_screen;
	}
	if (wStartMenuChoice == START_MENU_NEW_GAME) {
		if ((DeleteSaveDataForNewGame() & 0x10u) != 0u)
			goto title_screen;
	} else if (wStartMenuChoice == START_MENU_CONTINUE_FROM_DIARY) {
		AskToContinueFromDiaryWithDuelDataResult answer = AskToContinueFromDiaryWithDuelData();
		if ((answer.f & 0x10u) != 0u)
			goto title_screen;
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
	BankswitchROM(GameLoop_BANK);
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
	CopyDMAFunction();
	ValidateSRAM();
	BankswitchROM(BANK_GAME_LOOP);
	if (!frame_boundary_is_installed())
		GameLoop();
}
/* <<< factory Start */
