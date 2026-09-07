#include "home/rock_club_lobby.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/rock_club_lobby.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define RockClubLobbyAfterDuelTable 0x5edcu
#include "home/scripting.h"
#define EVENT_RECEIVED_LEGENDARY_CARDS 0x22u
#define TRUE 0x01u
#define EVENT_PUPIL_CHRIS_STATE 0x17u
#define PUPIL_DEFEATED 0x08u
/* <<< factory statics */

/* >>> factory RockClubLobbyAfterDuel */
RockClubLobbyAfterDuelResult RockClubLobbyAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(RockClubLobbyAfterDuelTable);
	return (RockClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory RockClubLobbyAfterDuel */

/* >>> factory Preload_Lass3 */
/* rock_club_lobby.asm:149-152: `cp TRUE` on the event value; carry loads the NPC. */
PreloadLass3Result Preload_Lass3(void)
{
	uint8_t a = GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS);
	uint8_t f = 0x40u;
	if (a == TRUE)
		f |= 0x80u;
	if ((a & 0x0Fu) < (TRUE & 0x0Fu))
		f |= 0x20u;
	if (a < TRUE)
		f |= 0x10u;
	return (PreloadLass3Result){a, f};
}
/* <<< factory Preload_Lass3 */

/* >>> factory Preload_ChrisInRockClubLobby */
/* rock_club_lobby.asm:18-23: `or a` returns an inactive pupil with Z; otherwise
 * `cp PUPIL_DEFEATED`, whose carry -- not yet defeated -- loads the pupil. */
PreloadChrisInRockClubLobbyResult Preload_ChrisInRockClubLobby(void)
{
	uint8_t a = GetEventValue(EVENT_PUPIL_CHRIS_STATE);
	if (a == 0u)
		return (PreloadChrisInRockClubLobbyResult){a, 0x80u};
	uint8_t f = 0x40u;
	if (a == PUPIL_DEFEATED)
		f |= 0x80u;
	if ((a & 0x0Fu) < (PUPIL_DEFEATED & 0x0Fu))
		f |= 0x20u;
	if (a < PUPIL_DEFEATED)
		f |= 0x10u;
	return (PreloadChrisInRockClubLobbyResult){a, f};
}
/* <<< factory Preload_ChrisInRockClubLobby */
