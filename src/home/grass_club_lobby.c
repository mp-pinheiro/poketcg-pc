#include "home/grass_club_lobby.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/grass_club_lobby.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define GrassClubLobbyAfterDuelTable 0x65cbu
/* <<< factory statics */

/* >>> factory GrassClubLobbyAfterDuel */
GrassClubLobbyAfterDuelResult GrassClubLobbyAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(GrassClubLobbyAfterDuelTable);
	return (GrassClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory GrassClubLobbyAfterDuel */
