#include "home/water_club_lobby.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/water_club_lobby.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define WaterClubLobbyAfterDuelTable 0x60a9u
/* <<< factory statics */

/* >>> factory WaterClubLobbyAfterDuel */
WaterClubLobbyAfterDuelResult WaterClubLobbyAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(WaterClubLobbyAfterDuelTable);
	return (WaterClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory WaterClubLobbyAfterDuel */
