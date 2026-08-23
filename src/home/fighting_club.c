#include "home/fighting_club.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/fighting_club.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define FightingClubAfterDuelTable 0x5daau
/* <<< factory statics */

/* >>> factory FightingClubAfterDuel */
FightingClubAfterDuelResult FightingClubAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(FightingClubAfterDuelTable);
	return (FightingClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory FightingClubAfterDuel */
