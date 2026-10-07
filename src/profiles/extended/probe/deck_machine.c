/* >>> part includes */
#include "home/deck_machine.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory CheckIfSelectedDeckMachineEntryIsEmpty */
static void adapt_CheckIfSelectedDeckMachineEntryIsEmpty(ProbeState *s)
{
	s->f = CheckIfSelectedDeckMachineEntryIsEmpty();
}
/* <<< factory CheckIfSelectedDeckMachineEntryIsEmpty */

/* >>> factory SafelySwitchToSRAM1 */
static void adapt_SafelySwitchToSRAM1(ProbeState *s)
{
	(void)s;
	SafelySwitchToSRAM1();
}
/* <<< factory SafelySwitchToSRAM1 */

/* >>> factory SafelySwitchToTempSRAMBank */
static void adapt_SafelySwitchToTempSRAMBank(ProbeState *s)
{
	(void)s;
	SafelySwitchToTempSRAMBank();
}
/* <<< factory SafelySwitchToTempSRAMBank */

/* >>> factory CheckIfHasEnoughCardsToBuildDeck */
static void adapt_CheckIfHasEnoughCardsToBuildDeck(ProbeState *s)
{
	DeckBuildCheckResult r = CheckIfHasEnoughCardsToBuildDeck(&s->hl);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CheckIfHasEnoughCardsToBuildDeck */

/* >>> factory GetSavedDeckPointers */
static void adapt_GetSavedDeckPointers(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	GetSavedDeckPointers(&s->hl, &de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory GetSavedDeckPointers */

/* >>> factory GetSavedDeckCount */
static void adapt_GetSavedDeckCount(ProbeState *s)
{
	(void)s;
	GetSavedDeckCount();
}
/* <<< factory GetSavedDeckCount */

/* >>> factory GetSelectedSavedDeckPtr */
static void adapt_GetSelectedSavedDeckPtr(ProbeState *s)
{
	uint16_t de = GetSelectedSavedDeckPtr();
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory GetSelectedSavedDeckPtr */

/* >>> factory SafelySwitchToSRAM0 */
static void adapt_SafelySwitchToSRAM0(ProbeState *s)
{
	(void)s;
	SafelySwitchToSRAM0();
}
/* <<< factory SafelySwitchToSRAM0 */

/* >>> factory DrawListScrollArrows */
static void adapt_DrawListScrollArrows(ProbeState *s)
{
	DrawListScrollArrows();
	(void)s;
}
/* <<< factory DrawListScrollArrows */

/* >>> factory SetDeckMachineTitleText */
static void adapt_SetDeckMachineTitleText(ProbeState *s)
{
	SetDeckMachineTitleTextResult r = SetDeckMachineTitleText();
	s->hl = r.hl;
}
/* <<< factory SetDeckMachineTitleText */

/* >>> factory FindFirstEmptyDeckSlot */
static void adapt_FindFirstEmptyDeckSlot(ProbeState *s)
{
	FindFirstEmptyDeckSlotResult r = FindFirstEmptyDeckSlot();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory FindFirstEmptyDeckSlot */

/* >>> factory PrintNumSavedDecks */
static void adapt_PrintNumSavedDecks(ProbeState *s)
{
	(void)s;
	PrintNumSavedDecks();
}
/* <<< factory PrintNumSavedDecks */

/* >>> factory CheckIfCanBuildSavedDeck */
static void adapt_CheckIfCanBuildSavedDeck(ProbeState *s)
{
	DeckBuildCheckResult r = CheckIfCanBuildSavedDeck(s->a, s->b);
	s->a = r.a; s->f = r.f;
}
/* <<< factory CheckIfCanBuildSavedDeck */

/* >>> factory PrintDeckMachineEntry */
static void adapt_PrintDeckMachineEntry(ProbeState *s)
{
	PrintDeckMachineEntryResult r = PrintDeckMachineEntry(s->a, s->d, s->e);
	s->a = r.a; s->f = r.f;
}
/* <<< factory PrintDeckMachineEntry */

/* >>> factory TryDeleteSavedDeck */
static void adapt_TryDeleteSavedDeck(ProbeState *s)
{
	TryDeleteSavedDeckResult result = TryDeleteSavedDeck();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory TryDeleteSavedDeck */

/* >>> factory HandleDeckMissingCardsList */
static void adapt_HandleDeckMissingCardsList(ProbeState *s)
{
	/* ProbeState splits de into the d and e bytes; the routine takes the pair. */
	uint16_t de = (uint16_t)(((uint16_t)s->d << 8) | s->e);
	HandleDeckMissingCardsListResult r = HandleDeckMissingCardsList(s->hl, de);

	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandleDeckMissingCardsList */

/* >>> factory HandleDismantleDeckToMakeSpace */
static void adapt_HandleDismantleDeckToMakeSpace(ProbeState *s)
{
	HandleDismantleDeckToMakeSpaceResult result = HandleDismantleDeckToMakeSpace();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory HandleDismantleDeckToMakeSpace */

/* >>> factory PrintVisibleDeckMachineEntries */
static void adapt_PrintVisibleDeckMachineEntries(ProbeState *s)
{
	PrintVisibleDeckMachineEntriesResult r = PrintVisibleDeckMachineEntries(s->f);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory PrintVisibleDeckMachineEntries */

/* >>> factory ClearScreenAndDrawDeckMachineScreen */
static void adapt_ClearScreenAndDrawDeckMachineScreen(ProbeState *s)
{
	(void)s;
	ClearScreenAndDrawDeckMachineScreen();
}
/* <<< factory ClearScreenAndDrawDeckMachineScreen */

/* >>> factory DrawDeckMachineScreen */
static void adapt_DrawDeckMachineScreen(ProbeState *s)
{
	DrawDeckMachineScreenResult r = DrawDeckMachineScreen();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory DrawDeckMachineScreen */

/* >>> factory HandleDeckMachineSelection */
static void adapt_HandleDeckMachineSelection(ProbeState *s)
{
	HandleDeckMachineSelectionResult r = HandleDeckMachineSelection();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandleDeckMachineSelection */

/* >>> factory UpdateDeckMachineScrollArrowsAndEntries */
static void adapt_UpdateDeckMachineScrollArrowsAndEntries(ProbeState *s)
{
	PrintVisibleDeckMachineEntriesResult result =
		UpdateDeckMachineScrollArrowsAndEntries(s->f);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory UpdateDeckMachineScrollArrowsAndEntries */

/* >>> factory SaveDeckInDeckSaveMachine */
static void adapt_SaveDeckInDeckSaveMachine(ProbeState *s)
{
	SaveDeckInDeckSaveMachineResult result = SaveDeckInDeckSaveMachine();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory SaveDeckInDeckSaveMachine */

/* >>> factory TryBuildDeckMachineDeck */
static void adapt_TryBuildDeckMachineDeck(ProbeState *s)
{
	TryBuildDeckMachineDeckResult r = TryBuildDeckMachineDeck();

	s->a = r.a;
	s->f = r.f;
}
/* <<< factory TryBuildDeckMachineDeck */

/* >>> factory HandleAutoDeckMenu */
static void adapt_HandleAutoDeckMenu(ProbeState *s)
{
	HandleAutoDeckMenuResult r = HandleAutoDeckMenu();

	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandleAutoDeckMenu */

/* >>> factory InitDeckMachineDrawingParams */
static void adapt_InitDeckMachineDrawingParams(ProbeState *s)
{
	InitDeckMachineDrawingParamsResult r =
		InitDeckMachineDrawingParams(s->d, s->e);
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory InitDeckMachineDrawingParams */

/* >>> factory HandleDeckSaveMachineMenu */
static void adapt_HandleDeckSaveMachineMenu(ProbeState *s)
{
	HandleDeckSaveMachineMenuResult result = HandleDeckSaveMachineMenu();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory HandleDeckSaveMachineMenu */

/* >>> part probe_entries_deck_machine */
const ProbeEntry probe_entries_deck_machine[] = {
	{ "CheckIfSelectedDeckMachineEntryIsEmpty", adapt_CheckIfSelectedDeckMachineEntryIsEmpty },
	{ "SafelySwitchToSRAM1", adapt_SafelySwitchToSRAM1 },
	{ "SafelySwitchToTempSRAMBank", adapt_SafelySwitchToTempSRAMBank },
	{ "CheckIfHasEnoughCardsToBuildDeck", adapt_CheckIfHasEnoughCardsToBuildDeck },
	{ "GetSavedDeckPointers", adapt_GetSavedDeckPointers },
	{ "GetSavedDeckCount", adapt_GetSavedDeckCount },
	{ "GetSelectedSavedDeckPtr", adapt_GetSelectedSavedDeckPtr },
	{ "SafelySwitchToSRAM0", adapt_SafelySwitchToSRAM0 },
	{ "DrawListScrollArrows", adapt_DrawListScrollArrows },
	{ "SetDeckMachineTitleText", adapt_SetDeckMachineTitleText },
	{ "FindFirstEmptyDeckSlot", adapt_FindFirstEmptyDeckSlot },
	{ "PrintNumSavedDecks", adapt_PrintNumSavedDecks },
	{ "CheckIfCanBuildSavedDeck", adapt_CheckIfCanBuildSavedDeck },
	{ "PrintDeckMachineEntry", adapt_PrintDeckMachineEntry },
	{ "TryDeleteSavedDeck", adapt_TryDeleteSavedDeck },
	{ "HandleDeckMissingCardsList", adapt_HandleDeckMissingCardsList },
	{ "HandleDismantleDeckToMakeSpace", adapt_HandleDismantleDeckToMakeSpace },
	{ "PrintVisibleDeckMachineEntries", adapt_PrintVisibleDeckMachineEntries },
	{ "ClearScreenAndDrawDeckMachineScreen", adapt_ClearScreenAndDrawDeckMachineScreen },
	{ "DrawDeckMachineScreen", adapt_DrawDeckMachineScreen },
	{ "HandleDeckMachineSelection", adapt_HandleDeckMachineSelection },
	{ "UpdateDeckMachineScrollArrowsAndEntries", adapt_UpdateDeckMachineScrollArrowsAndEntries },
	{ "SaveDeckInDeckSaveMachine", adapt_SaveDeckInDeckSaveMachine },
	{ "TryBuildDeckMachineDeck", adapt_TryBuildDeckMachineDeck },
	{ "HandleAutoDeckMenu", adapt_HandleAutoDeckMenu },
	{ "InitDeckMachineDrawingParams", adapt_InitDeckMachineDrawingParams },
	{ "HandleDeckSaveMachineMenu", adapt_HandleDeckSaveMachineMenu },
	{ NULL, NULL },
};
/* <<< part probe_entries_deck_machine */
