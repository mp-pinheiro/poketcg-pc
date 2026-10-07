/* >>> part includes */
#include "home/rock_club.h"

#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "home/rock_club.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
/* <<< part includes_2 */
/* >>> part RockClubAfterDuelTable */
#define RockClubAfterDuelTable (RockClubAfterDuel__after_duel_table_ADDR)
/* <<< part RockClubAfterDuelTable */

/* >>> factory RockClubAfterDuel */
RockClubAfterDuelResult RockClubAfterDuel(void)
{
	gb_write8(0x2000u, RockClubAfterDuel__after_duel_table_BANK);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(RockClubAfterDuelTable);
	return (RockClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory RockClubAfterDuel */
