#include "home/psychic_club_lobby.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/map.h"
#include "home/scripting.h"
#include "generated/wram.h"
#define NPC_RONALD1 0x02u
#define Script_ea02_ADDR 0x6A02u

#include "home/grass_club_entrance.h"
#define PsychicClubLobbyAfterDuelTable 0x696au

#include "home/scripting.h"
#include "mem.h"
#define EVENT_MEDAL_COUNT_540 0x2Eu
#define EVENT_RONALD_ENCOUNTER_540 0x32u

#include "home/psychic_club_lobby.h"
#include "generated/wram.h"
/* <<< factory statics */

/* >>> factory PsychicClubLobbyLoadMap */
PsychicClubLobbyLoadMapResult PsychicClubLobbyLoadMap(uint8_t b, uint8_t c, uint16_t hl)
{
	wTempNPC = NPC_RONALD1;
	NPCSearchResult r = FindLoadedNPC();
	if (r.f & 0x10u)
		return (PsychicClubLobbyLoadMapResult){r.a, r.f, b, c, hl};
	SetNextNPCAndScriptResult r2 = SetNextNPCAndScript(Script_ea02_ADDR, hl);
	return (PsychicClubLobbyLoadMapResult){r2.a, r2.f, r2.b, r2.c, r2.hl};
}
/* <<< factory PsychicClubLobbyLoadMap */

/* >>> factory PsychicClubLobbyAfterDuel */
PsychicClubLobbyAfterDuelResult PsychicClubLobbyAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(PsychicClubLobbyAfterDuelTable);
	return (PsychicClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory PsychicClubLobbyAfterDuel */

/* >>> factory _Preload_Ronald1InPsychicClubLobby */
_Preload_Ronald1InPsychicClubLobbyResult _Preload_Ronald1InPsychicClubLobby(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)TryGiveMedalPCPacks(b, c, d, e, hl);
	uint8_t medal_count = GetEventValue(EVENT_MEDAL_COUNT_540);
	if (medal_count != 4u) {
		uint8_t f = (medal_count == 0u) ? 0x80u : 0x00u;
		return (_Preload_Ronald1InPsychicClubLobbyResult){medal_count, f};
	}
	uint8_t encounter = GetEventValue(EVENT_RONALD_ENCOUNTER_540);
	if (encounter != 0u) {
		return (_Preload_Ronald1InPsychicClubLobbyResult){encounter, 0x00u};
	}
	return (_Preload_Ronald1InPsychicClubLobbyResult){0u, 0x90u};
}
/* <<< factory _Preload_Ronald1InPsychicClubLobby */

/* >>> factory Preload_Ronald1InPsychicClubLobby */
Preload_Ronald1InPsychicClubLobbyResult Preload_Ronald1InPsychicClubLobby(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	_Preload_Ronald1InPsychicClubLobbyResult r = _Preload_Ronald1InPsychicClubLobby(b, c, d, e, hl);
	if (!(r.f & 0x10u)) {
		return (Preload_Ronald1InPsychicClubLobbyResult){r.a, r.f, b, c, d, e, hl};
	}
	uint8_t y = wPlayerYCoord;
	wLoadNPCYPos = y;
	return (Preload_Ronald1InPsychicClubLobbyResult){y, r.f, b, c, d, e, hl};
}
/* <<< factory Preload_Ronald1InPsychicClubLobby */
