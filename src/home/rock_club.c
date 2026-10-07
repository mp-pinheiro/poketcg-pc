#include "home/rock_club.h"

#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/rock_club.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define RockClubAfterDuelTable (RockClubAfterDuel__after_duel_table_ADDR)
/* <<< factory statics */

/* >>> factory RockClubAfterDuel */
RockClubAfterDuelResult RockClubAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(RockClubAfterDuelTable);
	return (RockClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory RockClubAfterDuel */
