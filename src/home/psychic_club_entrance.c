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

#include "home/map.h"
#include "home/scripting.h"
#include "generated/wram.h"
#define NPC_RONALD2 0x71u
#define EVENT_RONALD_FIRST_DUEL_STATE 0x4Cu
#define Script_FirstRonaldDuel_ADDR 0x68C0u

#include "home/psychic_club_entrance.h"
#include "home/map.h"
#include "home/scripting.h"
#define NPC_RONALD3 0x72u
#define EVENT_RONALD_SECOND_DUEL_STATE 0x4Du
#define Script_SecondRonaldDuel_ADDR 0x691Eu

#include "home/psychic_club_entrance.h"
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

/* >>> factory TryFirstRonaldDuel */
TryFirstRonaldDuelResult TryFirstRonaldDuel(uint8_t b, uint8_t c, uint16_t hl)
{
	wTempNPC = NPC_RONALD2;
	NPCSearchResult r = FindLoadedNPC();
	if (r.f & 0x10u)
		return (TryFirstRonaldDuelResult){r.a, r.f, b, c, hl};
	uint8_t event = GetEventValue(EVENT_RONALD_FIRST_DUEL_STATE);
	if (event != 0u)
		return (TryFirstRonaldDuelResult){event, 0x00u, b, c, hl};
	SetNextNPCAndScriptResult r2 = SetNextNPCAndScript(Script_FirstRonaldDuel_ADDR, hl);
	return (TryFirstRonaldDuelResult){r2.a, r2.f, r2.b, r2.c, r2.hl};
}
/* <<< factory TryFirstRonaldDuel */

/* >>> factory TrySecondRonaldDuel */
TrySecondRonaldDuelResult TrySecondRonaldDuel(uint8_t b, uint8_t c, uint16_t hl)
{
	wTempNPC = NPC_RONALD3;
	NPCSearchResult r = FindLoadedNPC();
	if (r.f & 0x10u)
		return (TrySecondRonaldDuelResult){r.a, r.f, b, c, hl};
	uint8_t event = GetEventValue(EVENT_RONALD_SECOND_DUEL_STATE);
	if (event != 0u)
		return (TrySecondRonaldDuelResult){event, 0x00u, b, c, hl};
	SetNextNPCAndScriptResult r2 = SetNextNPCAndScript(Script_SecondRonaldDuel_ADDR, hl);
	return (TrySecondRonaldDuelResult){r2.a, r2.f, r2.b, r2.c, r2.hl};
}
/* <<< factory TrySecondRonaldDuel */

/* >>> factory LoadClubEntrance */
void LoadClubEntrance(void)
{
	TryFirstRonaldDuelResult r1 = TryFirstRonaldDuel(0u, 0u, 0u);
	TrySecondRonaldDuelResult r2 = TrySecondRonaldDuel(r1.b, r1.c, r1.hl);
	TryFirstRonaldEncounterResult r3 = TryFirstRonaldEncounter(r2.b, r2.c, r2.hl);
	(void)r3;
}
/* <<< factory LoadClubEntrance */
