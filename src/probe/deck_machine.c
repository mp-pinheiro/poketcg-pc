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

const ProbeEntry probe_entries_deck_machine[] = {
	{ "CheckIfSelectedDeckMachineEntryIsEmpty", adapt_CheckIfSelectedDeckMachineEntryIsEmpty },
	{ NULL, NULL },
};
