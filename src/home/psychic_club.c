#include "home/psychic_club.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/psychic_club.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define PsychicClubAfterDuelTable 0x6a4du
/* <<< factory statics */

/* >>> factory PsychicClubAfterDuel */
PsychicClubAfterDuelResult PsychicClubAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(PsychicClubAfterDuelTable);
	return (PsychicClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory PsychicClubAfterDuel */
