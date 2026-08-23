#include "home/fighting_club_lobby.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/fighting_club_lobby.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define FightingClubLobbyAfterDuelTable 0x5c6fu
/* <<< factory statics */

/* >>> factory FightingClubLobbyAfterDuel */
FightingClubLobbyAfterDuelResult FightingClubLobbyAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(FightingClubLobbyAfterDuelTable);
	return (FightingClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory FightingClubLobbyAfterDuel */
