#include "home/lightning_club_lobby.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/lightning_club_lobby.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define LightningClubLobbyAfterDuelTable 0x6374u
/* <<< factory statics */

/* >>> factory LightningClubLobbyAfterDuel */
LightningClubLobbyAfterDuelResult LightningClubLobbyAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(LightningClubLobbyAfterDuelTable);
	return (LightningClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory LightningClubLobbyAfterDuel */
