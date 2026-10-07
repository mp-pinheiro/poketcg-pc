/* --- factory MainMenu_CardPop */
/* >>> part probe_entries_main_menu */
const ProbeEntry probe_entries_main_menu[] = {
	{ "MainMenu_NewGame", adapt_MainMenu_NewGame },
	{ "MainMenu_ContinueFromDiary", adapt_MainMenu_ContinueFromDiary },
	{ "MainMenu_ContinueDuel", adapt_MainMenu_ContinueDuel },
	{ "_GameLoop", adapt__GameLoop },
	{ NULL, NULL },
};
/* <<< part probe_entries_main_menu */
