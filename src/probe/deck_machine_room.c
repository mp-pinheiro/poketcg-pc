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
	ScriptBeatAaronResult r = Script_BeatAaron();
	s->a = r.a;
	s->c = r.c;
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

/* >>> factory Script_da76 */
static void adapt_Script_da76(ProbeState *s)
{
	(void)s;
	Script_da76();
}
/* <<< factory Script_da76 */

/* >>> factory Script_da1c */
static void adapt_Script_da1c(ProbeState *s)
{
	(void)s;
	Script_da1c();
}
/* <<< factory Script_da1c */

/* >>> factory Script_d9c2 */
static void adapt_Script_d9c2(ProbeState *s)
{
	(void)s;
	Script_d9c2();
}
/* <<< factory Script_d9c2 */

/* >>> factory Script_d9ef */
static void adapt_Script_d9ef(ProbeState *s)
{
	(void)s;
	Script_d9ef();
}
/* <<< factory Script_d9ef */

const ProbeEntry probe_entries_deck_machine_room[] = {
	{ "Func_d96c", adapt_Func_d96c },
	{ "Script_BeatAaron", adapt_Script_BeatAaron },
	{ "DeckMachineRoomCloseTextBox", adapt_DeckMachineRoomCloseTextBox },
	{ "DeckMachineRoomAfterDuel", adapt_DeckMachineRoomAfterDuel },
	{ "Script_da76", adapt_Script_da76 },
	{ "Script_da1c", adapt_Script_da1c },
	{ "Script_d9c2", adapt_Script_d9c2 },
	{ "Script_d9ef", adapt_Script_d9ef },
	{ NULL, NULL },
};
