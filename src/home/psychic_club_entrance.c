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

#include "home/psychic_club_entrance.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#include "mem.h"
#define ClubEntranceAfterDuelTable 0x67FCu

#include "home/scripting.h"
#include "generated/wram.h"
#include "mem.h"
#define EVENT_MEDAL_COUNT 0x2Eu
#define RONALD_DUEL_WON 0x01u
#define RONALD_DUEL_LOST 0x02u

#define EVENT_RONALD_FIRST_CLUB_ENTRANCE_ENCOUNTER 0x4Bu
#define TRUE 0x01u
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

/* >>> factory ClubEntranceAfterDuel */
ClubEntranceAfterDuelResult ClubEntranceAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(ClubEntranceAfterDuelTable);
	return (ClubEntranceAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory ClubEntranceAfterDuel */

/* >>> factory Func_e8a0 */
Func_e8a0Result Func_e8a0(uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	if (a == RONALD_DUEL_WON) {
		wLoadNPCXPos = 0x08u;
		wLoadNPCYPos = 0x08u;
		return (Func_e8a0Result){0x08u, 0x90u};
	}
	if (a >= RONALD_DUEL_LOST) {
		return (Func_e8a0Result){a, 0x00u};
	}
	(void)TryGiveMedalPCPacks(b, c, d, e, hl);
	uint8_t medal_count = GetEventValue(EVENT_MEDAL_COUNT);
	if (medal_count == e) {
		return (Func_e8a0Result){medal_count, 0x90u};
	}
	return (Func_e8a0Result){medal_count, (uint8_t)((medal_count == 0u) ? 0x80u : 0x00u)};
}
/* <<< factory Func_e8a0 */

/* >>> factory Preload_Ronald1InClubEntrance */
PreloadRonaldInClubEntranceResult Preload_Ronald1InClubEntrance(void)
{
	/* psychic_club_entrance.asm:65-68: `cp TRUE` on the event value; carry --
	 * the encounter has not happened -- loads Ronald. */
	uint8_t a = GetEventValue(EVENT_RONALD_FIRST_CLUB_ENTRANCE_ENCOUNTER);
	uint8_t f = 0x40u;
	if (a == TRUE)
		f |= 0x80u;
	if ((a & 0x0Fu) < TRUE)
		f |= 0x20u;
	if (a < TRUE)
		f |= 0x10u;
	return (PreloadRonaldInClubEntranceResult){a, f};
}
/* <<< factory Preload_Ronald1InClubEntrance */

/* >>> factory Preload_Ronald2InClubEntrance */
PreloadRonaldInClubEntranceResult Preload_Ronald2InClubEntrance(uint8_t b, uint8_t c, uint8_t d, uint16_t hl)
{
	/* psychic_club_entrance.asm:99-101: e = 2, the medal requirement, then
	 * falls through into Func_e8a0. */
	Func_e8a0Result r = Func_e8a0(GetEventValue(EVENT_RONALD_FIRST_DUEL_STATE), b, c, d, 2u, hl);
	return (PreloadRonaldInClubEntranceResult){r.a, r.f};
}
/* <<< factory Preload_Ronald2InClubEntrance */

/* >>> factory Preload_Ronald3InClubEntrance */
PreloadRonaldInClubEntranceResult Preload_Ronald3InClubEntrance(uint8_t b, uint8_t c, uint8_t d, uint16_t hl)
{
	/* psychic_club_entrance.asm:188-191: e = 5, then Func_e8a0. */
	Func_e8a0Result r = Func_e8a0(GetEventValue(EVENT_RONALD_SECOND_DUEL_STATE), b, c, d, 5u, hl);
	return (PreloadRonaldInClubEntranceResult){r.a, r.f};
}
/* <<< factory Preload_Ronald3InClubEntrance */
