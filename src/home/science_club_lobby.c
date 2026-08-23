#include "home/science_club_lobby.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/science_club_lobby.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define ScienceClubLobbyAfterDuelTable 0x6b5eu
/* <<< factory statics */

/* >>> factory ScienceClubLobbyAfterDuel */
ScienceClubLobbyAfterDuelResult ScienceClubLobbyAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(ScienceClubLobbyAfterDuelTable);
	return (ScienceClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory ScienceClubLobbyAfterDuel */
