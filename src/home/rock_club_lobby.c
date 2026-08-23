#include "home/rock_club_lobby.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/rock_club_lobby.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define RockClubLobbyAfterDuelTable 0x5edcu
/* <<< factory statics */

/* >>> factory RockClubLobbyAfterDuel */
RockClubLobbyAfterDuelResult RockClubLobbyAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(RockClubLobbyAfterDuelTable);
	return (RockClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory RockClubLobbyAfterDuel */
