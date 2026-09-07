#include "home/fighting_club_lobby.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/fighting_club_lobby.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define FightingClubLobbyAfterDuelTable 0x5c6fu
#include "home/scripting.h"
#define EVENT_RECEIVED_LEGENDARY_CARDS 0x22u
#define TRUE 0x01u
#define EVENT_TEMP_DUELED_IMAKUNI 0x03u
#define EVENT_IMAKUNI_STATE 0x13u
#define EVENT_IMAKUNI_ROOM 0x34u
#define IMAKUNI_NOT_MENTIONED 0x00u
#define IMAKUNI_MENTIONED 0x01u
#define IMAKUNI_TALKED 0x02u
#define IMAKUNI_FIGHTING_CLUB 0x00u
#define MUSIC_IMAKUNI 0x10u
/* <<< factory statics */

/* >>> factory FightingClubLobbyAfterDuel */
FightingClubLobbyAfterDuelResult FightingClubLobbyAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(FightingClubLobbyAfterDuelTable);
	return (FightingClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory FightingClubLobbyAfterDuel */

/* >>> factory Preload_Granny1 */
/* fighting_club_lobby.asm:182-185: `cp TRUE` on the event value; carry loads the NPC. */
PreloadGranny1Result Preload_Granny1(void)
{
	uint8_t a = GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS);
	uint8_t f = 0x40u;
	if (a == TRUE)
		f |= 0x80u;
	if ((a & 0x0Fu) < (TRUE & 0x0Fu))
		f |= 0x20u;
	if (a < TRUE)
		f |= 0x10u;
	return (PreloadGranny1Result){a, f};
}
/* <<< factory Preload_Granny1 */

/* >>> factory Preload_ImakuniInFightingClubLobby */
/* fighting_club_lobby.asm:78-96: every `.dont_load` exit is `or a` on the value last
 * loaded (the state, the temp-duel flag or the room); the load exit is `scf`
 * over the `cp`'s Z. */
PreloadImakuniInFightingClubLobbyResult Preload_ImakuniInFightingClubLobby(void)
{
	uint8_t state = GetEventValue(EVENT_IMAKUNI_STATE);
	if (state == IMAKUNI_MENTIONED) {
		wDefaultSong = MUSIC_IMAKUNI;
		return (PreloadImakuniInFightingClubLobbyResult){MUSIC_IMAKUNI, 0x90u};
	}
	if (state == IMAKUNI_NOT_MENTIONED)
		return (PreloadImakuniInFightingClubLobbyResult){state, 0x80u};
	uint8_t dueled = GetEventValue(EVENT_TEMP_DUELED_IMAKUNI);
	if (dueled != 0u)
		return (PreloadImakuniInFightingClubLobbyResult){dueled, 0u};
	uint8_t room = GetEventValue(EVENT_IMAKUNI_ROOM);
	if (room != IMAKUNI_FIGHTING_CLUB)
		return (PreloadImakuniInFightingClubLobbyResult){room, room == 0u ? 0x80u : 0u};
	wDefaultSong = MUSIC_IMAKUNI;
	return (PreloadImakuniInFightingClubLobbyResult){MUSIC_IMAKUNI, 0x90u};
}
/* <<< factory Preload_ImakuniInFightingClubLobby */
