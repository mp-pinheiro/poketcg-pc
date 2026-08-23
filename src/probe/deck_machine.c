#include "home/deck_machine.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

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

/* >>> factory EmptyScreenAndDrawTextBox */
static void adapt_EmptyScreenAndDrawTextBox(ProbeState *s)
{
	(void)s;
	EmptyScreenAndDrawTextBox();
}
/* <<< factory EmptyScreenAndDrawTextBox */

/* >>> factory PrintCardToSendText */
static void adapt_PrintCardToSendText(ProbeState *s)
{
	(void)s;
	PrintCardToSendText();
}
/* <<< factory PrintCardToSendText */

/* >>> factory PrintReceivedTheseCardsText */
static void adapt_PrintReceivedTheseCardsText(ProbeState *s)
{
	(void)s;
	PrintReceivedTheseCardsText();
}
/* <<< factory PrintReceivedTheseCardsText */

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
	{ "EmptyScreenAndDrawTextBox", adapt_EmptyScreenAndDrawTextBox },
	{ "PrintCardToSendText", adapt_PrintCardToSendText },
	{ "PrintReceivedTheseCardsText", adapt_PrintReceivedTheseCardsText },
	{ NULL, NULL },
};
