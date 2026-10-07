/* >>> part includes */
#include "home/lightning_club_lobby.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "home/lightning_club_lobby.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
/* <<< part includes_2 */
/* >>> part LightningClubLobbyAfterDuelTable */
#define LightningClubLobbyAfterDuelTable (LightningClubLobbyAfterDuel__after_duel_table_ADDR)
/* <<< part LightningClubLobbyAfterDuelTable */
/* >>> part includes_tail */
#include "home/scripting.h"
/* <<< part includes_tail */

/* >>> factory LightningClubLobbyAfterDuel */
LightningClubLobbyAfterDuelResult LightningClubLobbyAfterDuel(void)
{
	gb_write8(0x2000u, LightningClubLobbyAfterDuel__after_duel_table_BANK);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(LightningClubLobbyAfterDuelTable);
	return (LightningClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory LightningClubLobbyAfterDuel */

/* >>> factory Preload_ImakuniInLightningClubLobby */
/* lightning_club_lobby.asm:13-30: every `.dont_load` exit is `or a` on the value last
 * loaded (the state, the temp-duel flag or the room); the load exit is `scf`
 * over the `cp`'s Z. */
PreloadImakuniInLightningClubLobbyResult Preload_ImakuniInLightningClubLobby(void)
{
	uint8_t state = GetEventValue(EVENT_IMAKUNI_STATE);
	if (state < IMAKUNI_TALKED)
		return (PreloadImakuniInLightningClubLobbyResult){state, state == 0u ? 0x80u : 0u};
	uint8_t dueled = GetEventValue(EVENT_TEMP_DUELED_IMAKUNI);
	if (dueled != 0u)
		return (PreloadImakuniInLightningClubLobbyResult){dueled, 0u};
	uint8_t room = GetEventValue(EVENT_IMAKUNI_ROOM);
	if (room != IMAKUNI_LIGHTNING_CLUB)
		return (PreloadImakuniInLightningClubLobbyResult){room, room == 0u ? 0x80u : 0u};
	wDefaultSong = MUSIC_IMAKUNI;
	return (PreloadImakuniInLightningClubLobbyResult){MUSIC_IMAKUNI, 0x90u};
}
/* <<< factory Preload_ImakuniInLightningClubLobby */
