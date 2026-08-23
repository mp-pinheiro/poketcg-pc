#include "home/psychic_club_entrance.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/map.h"
#include "home/scripting.h"
#include "generated/wram.h"
#define NPC_RONALD1 0x02u
#define Script_FirstRonaldEncounter_ADDR 0x6862u
/* <<< factory statics */

/* >>> factory TryFirstRonaldEncounter */
TryFirstRonaldEncounterResult TryFirstRonaldEncounter(uint8_t b, uint8_t c, uint16_t hl)
{
	wTempNPC = NPC_RONALD1;
	NPCSearchResult r = FindLoadedNPC();
	if (r.f & 0x10u)
		return (TryFirstRonaldEncounterResult){r.a, r.f, b, c, hl};
	SetNextNPCAndScriptResult r2 = SetNextNPCAndScript(Script_FirstRonaldEncounter_ADDR, hl);
	return (TryFirstRonaldEncounterResult){r2.a, r2.f, r2.b, r2.c, r2.hl};
}
/* <<< factory TryFirstRonaldEncounter */
