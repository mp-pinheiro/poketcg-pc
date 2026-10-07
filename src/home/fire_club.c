/* >>> part includes */
#include "home/fire_club.h"

#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "home/fire_club.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
/* <<< part includes_2 */
/* >>> part FireClubAfterDuelTable */
#define FireClubAfterDuelTable (FireClubAfterDuel__after_duel_table_ADDR)
/* <<< part FireClubAfterDuelTable */

/* >>> factory FireClubAfterDuel */
FireClubAfterDuelResult FireClubAfterDuel(void)
{
	gb_write8(0x2000u, FireClubAfterDuel__after_duel_table_BANK);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(FireClubAfterDuelTable);
	return (FireClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory FireClubAfterDuel */
