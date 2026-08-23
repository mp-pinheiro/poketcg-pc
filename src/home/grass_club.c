#include "home/grass_club.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/grass_club.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define GrassClubAfterDuelTable 0x66eeu
/* <<< factory statics */

/* >>> factory GrassClubAfterDuel */
GrassClubAfterDuelResult GrassClubAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(GrassClubAfterDuelTable);
	return (GrassClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory GrassClubAfterDuel */
