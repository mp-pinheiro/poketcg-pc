#include "home/lightning_club.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/lightning_club.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define LightningClubAfterDuelTable 0x63efu
/* <<< factory statics */

/* >>> factory LightningClubAfterDuel */
LightningClubAfterDuelResult LightningClubAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(LightningClubAfterDuelTable);
	return (LightningClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory LightningClubAfterDuel */
