#include "home/deck_machine_room.h"
#include "probe.h"
static void adapt_Func_d96c(ProbeState *s) { FuncD96cResult r = Func_d96c(s->a); s->a=r.a; s->b=r.b; s->c=r.c; s->hl=r.hl; }
static void adapt_Script_BeatAaron(ProbeState *s) { (void)s; Script_BeatAaron(); }
const ProbeEntry probe_entries_deck_machine_room[] = {
 {"Func_d96c", adapt_Func_d96c}, {"Script_BeatAaron", adapt_Script_BeatAaron}, {NULL, NULL},
};
