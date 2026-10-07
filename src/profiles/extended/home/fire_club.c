/* >>> part includes */
#include "home/fire_club.h"

#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> factory statics */
#include "home/fire_club.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define FireClubAfterDuelTable (FireClubAfterDuel__after_duel_table_ADDR)
/* <<< factory statics */

/* >>> factory FireClubAfterDuel */
FireClubAfterDuelResult FireClubAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(FireClubAfterDuelTable);
	return (FireClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory FireClubAfterDuel */
