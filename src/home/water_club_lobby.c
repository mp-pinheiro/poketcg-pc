#include "home/water_club_lobby.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/water_club_lobby.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define WaterClubLobbyAfterDuelTable 0x60a9u
#include "home/scripting.h"
#define EVENT_JOSHUA_STATE 0x33u
#define JOSHUA_DEFEATED 0x02u
#define EVENT_TEMP_DUELED_IMAKUNI 0x03u
#define EVENT_IMAKUNI_STATE 0x13u
#define EVENT_IMAKUNI_ROOM 0x34u
#define IMAKUNI_TALKED 0x02u
#define IMAKUNI_WATER_CLUB 0x03u
#define MUSIC_IMAKUNI 0x10u
/* <<< factory statics */

/* >>> factory WaterClubLobbyAfterDuel */
WaterClubLobbyAfterDuelResult WaterClubLobbyAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(WaterClubLobbyAfterDuelTable);
	return (WaterClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory WaterClubLobbyAfterDuel */

/* >>> factory Preload_Man2 */
/* water_club_lobby.asm:81-84: `cp JOSHUA_DEFEATED` on the event value; carry loads the NPC. */
PreloadMan2Result Preload_Man2(void)
{
	uint8_t a = GetEventValue(EVENT_JOSHUA_STATE);
	uint8_t f = 0x40u;
	if (a == JOSHUA_DEFEATED)
		f |= 0x80u;
	if ((a & 0x0Fu) < (JOSHUA_DEFEATED & 0x0Fu))
		f |= 0x20u;
	if (a < JOSHUA_DEFEATED)
		f |= 0x10u;
	return (PreloadMan2Result){a, f};
}
/* <<< factory Preload_Man2 */

/* >>> factory Preload_ImakuniInWaterClubLobby */
/* water_club_lobby.asm:13-30: every `.dont_load` exit is `or a` on the value last
 * loaded (the state, the temp-duel flag or the room); the load exit is `scf`
 * over the `cp`'s Z. */
PreloadImakuniInWaterClubLobbyResult Preload_ImakuniInWaterClubLobby(void)
{
	uint8_t state = GetEventValue(EVENT_IMAKUNI_STATE);
	if (state < IMAKUNI_TALKED)
		return (PreloadImakuniInWaterClubLobbyResult){state, state == 0u ? 0x80u : 0u};
	uint8_t dueled = GetEventValue(EVENT_TEMP_DUELED_IMAKUNI);
	if (dueled != 0u)
		return (PreloadImakuniInWaterClubLobbyResult){dueled, 0u};
	uint8_t room = GetEventValue(EVENT_IMAKUNI_ROOM);
	if (room != IMAKUNI_WATER_CLUB)
		return (PreloadImakuniInWaterClubLobbyResult){room, room == 0u ? 0x80u : 0u};
	wDefaultSong = MUSIC_IMAKUNI;
	return (PreloadImakuniInWaterClubLobbyResult){MUSIC_IMAKUNI, 0x90u};
}
/* <<< factory Preload_ImakuniInWaterClubLobby */
