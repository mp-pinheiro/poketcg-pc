#include "home/fire_club.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/fire_club.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define FireClubAfterDuelTable 0x6e9au
/* <<< factory statics */

/* >>> factory FireClubAfterDuel */
FireClubAfterDuelResult FireClubAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(FireClubAfterDuelTable);
	return (FireClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory FireClubAfterDuel */
