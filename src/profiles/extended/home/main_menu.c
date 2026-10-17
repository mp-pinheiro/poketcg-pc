/* --- factory MainMenu_CardPop */
/* >>> factory MainMenu_NewGame */
uint8_t MainMenu_NewGame(void)
{
	runtime_mark_event(RUNTIME_EVENT_NEW_GAME_ENTERED);
	Func_c1b1();
	if (!frame_boundary_is_installed()) {
		/* Probe world: the oracle stops pre-ret right after Func_c1b1
		 * (main_menu.asm:33); the naming and portrait screens below are
		 * frame-driven and never terminate without the host loop. */
		DisplayPlayerNamingScreen();
		return 0x00u;
	}
	if (runtime_character_selection_enabled())
		PlayerGenderSelection();
	else
		runtime_set_player_gender(0);
	(void)DisplayPlayerNamingScreen();
	InitSaveData();
	if (runtime_pc_options_enabled()) {
		runtime_load_pc_config_cursors();
		SaveConfigSettings();
	}
	EnableSRAM();
	wAnimationsDisabled = sAnimationsDisabled;
	wTextSpeed = sTextSpeed;
	DisableSRAM();
	PlaySong(MUSIC_STOP);
	/* `farcall SetMainSGBBorder` (engine/sgb.asm:1-14) returns at its own
	 * first compare unless the console is SGB, and the SGB path it guards
	 * has no C body in this tree; the CGB/DMG path is a no-op. */
	wDefaultSong = MUSIC_OVERWORLD;
	(void)PlayDefaultSong();
	DrawPlayerPortraitAndPrintNewGameText();
	wGameEvent = GAME_EVENT_OVERWORLD;
	ExecuteGameEvent();
	return 0x00u; /* or a; ret */
}
/* <<< factory MainMenu_NewGame */
/* >>> factory MainMenu_ContinueFromDiary */
uint8_t MainMenu_ContinueFromDiary(void)
{
	PlaySong(MUSIC_STOP);
	if (!frame_boundary_is_installed()) {
		/* Probe world: the oracle stops pre-ret at the song stop
		 * (main_menu.asm:56-57), before backup save validation. */
		MainMenu_NewGame();
		return 0x00u;
	}
	ValidateResult backup = ValidateBackupGeneralSaveData();
	if ((backup.f & 0x10u) == 0u)
		return MainMenu_NewGame(); /* jr nc: invalid backup save */
	Func_c1ed();
	/* SetMainSGBBorder is SGB-only; see MainMenu_NewGame. */
	EnableSRAM();
	sPlayerInChallengeMachine = 0u;
	DisableSRAM();
	wGameEvent = GAME_EVENT_OVERWORLD;
	ExecuteGameEvent();
	return 0x00u; /* or a; ret */
}
/* <<< factory MainMenu_ContinueFromDiary */
/* >>> factory _GameLoop */
typedef uint8_t (*MainMenuFunction)(void);

/* main_menu.asm:26-30 */
static const MainMenuFunction MainMenuFunctionTable[] = {
	MainMenu_ContinueFromDiary,
	MainMenu_NewGame,
	MainMenu_ContinueDuel,
};

void _GameLoop(void)
{
	for (;;) { /* jr _GameLoop: virtually restart game (main_menu.asm:20) */
		ZeroObjectPositions();
		wVBlankOAMCopyToggle = (uint8_t)(wVBlankOAMCopyToggle + 1u);
		/* `farcall SetIntroSGBBorder` (engine/sgb.asm:17-21) is SGB-only;
		 * the non-SGB early return is what runs, so it is a no-op here. */
		wLastSelectedStartMenuItem = 0xFFu;
		if (!frame_boundary_is_installed()) {
			/* Probe world: the oracle stops pre-ret before
			 * .main_menu_loop (main_menu.asm:11); keep the bounded
			 * prefix instead of dispatching into the menu table. */
			HandleTitleScreen();
			return;
		}
		for (;;) { /* .main_menu_loop */
			hWhoseTurn = PLAYER_TURN;
			Func_c1f8();
			HandleTitleScreen();
			if (wStartMenuChoice == START_MENU_PC_OPTIONS)
				continue;
			if ((MainMenuFunctionTable[wStartMenuChoice]() & 0x10u) != 0u)
				continue; /* jr c: return to main menu */
			break; /* jr _GameLoop */
		}
	}
}
/* <<< factory _GameLoop */
/* === factory MainMenu_ContinueDuel */
