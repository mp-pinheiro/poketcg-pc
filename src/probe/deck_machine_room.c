#include "home/deck_machine_room.h"
#include "probe.h"

/* >>> factory Func_d96c */
static void adapt_Func_d96c(ProbeState *s)
{
	FuncD96cResult r = Func_d96c(s->a);
	s->a = r.a;
	s->b = r.b;
	s->c = r.c;
	s->hl = r.hl;
}
/* <<< factory Func_d96c */

/* >>> factory Script_BeatAaron */
static void adapt_Script_BeatAaron(ProbeState *s)
{
	(void)s;
	Script_BeatAaron();
}
/* <<< factory Script_BeatAaron */

/* >>> factory DeckMachineRoomCloseTextBox */
static void adapt_DeckMachineRoomCloseTextBox(ProbeState *s)
{
	(void)s;
	DeckMachineRoomCloseTextBox();
}
/* <<< factory DeckMachineRoomCloseTextBox */

/* >>> factory DeckMachineRoomAfterDuel */
static void adapt_DeckMachineRoomAfterDuel(ProbeState *s)
{
	DeckMachineRoomAfterDuelResult r = DeckMachineRoomAfterDuel();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory DeckMachineRoomAfterDuel */

const ProbeEntry probe_entries_deck_machine_room[] = {
	{ "Func_d96c", adapt_Func_d96c },
	{ "Script_BeatAaron", adapt_Script_BeatAaron },
	{ "DeckMachineRoomCloseTextBox", adapt_DeckMachineRoomCloseTextBox },
	{ "DeckMachineRoomAfterDuel", adapt_DeckMachineRoomAfterDuel },
	{ NULL, NULL },
};
