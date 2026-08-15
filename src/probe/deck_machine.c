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

const ProbeEntry probe_entries_deck_machine[] = {
	{ "CheckIfSelectedDeckMachineEntryIsEmpty", adapt_CheckIfSelectedDeckMachineEntryIsEmpty },
	{ "SafelySwitchToSRAM1", adapt_SafelySwitchToSRAM1 },
	{ "SafelySwitchToTempSRAMBank", adapt_SafelySwitchToTempSRAMBank },
	{ "CheckIfHasEnoughCardsToBuildDeck", adapt_CheckIfHasEnoughCardsToBuildDeck },
	{ "GetSavedDeckPointers", adapt_GetSavedDeckPointers },
	{ NULL, NULL },
};
