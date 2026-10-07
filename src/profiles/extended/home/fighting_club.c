#include "home/fighting_club.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/fighting_club.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define FightingClubAfterDuelTable (FightingClubAfterDuel__after_duel_table_ADDR)

#include "home/scripting.h"

/* fighting_club.asm:99-103, 129-133, 157-161: `cp PUPIL_DEFEATED` then `ccf`,
 * so carry -- load the pupil into the club -- means defeated. `ccf` clears N
 * and H and keeps Z. */
static PreloadPupilInFightingClubResult preload_pupil(uint8_t event)
{
	uint8_t a = GetEventValue(event);
	uint8_t f = 0u;
	if (a == PUPIL_DEFEATED)
		f |= 0x80u;
	if (a >= PUPIL_DEFEATED)
		f |= 0x10u;
	return (PreloadPupilInFightingClubResult){a, f};
}
/* <<< factory statics */

/* >>> factory FightingClubAfterDuel */
FightingClubAfterDuelResult FightingClubAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(FightingClubAfterDuelTable);
	return (FightingClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory FightingClubAfterDuel */

/* >>> factory Preload_ChrisInFightingClub */
PreloadPupilInFightingClubResult Preload_ChrisInFightingClub(void)
{
	return preload_pupil(EVENT_PUPIL_CHRIS_STATE);
}
/* <<< factory Preload_ChrisInFightingClub */

/* >>> factory Preload_MichaelInFightingClub */
PreloadPupilInFightingClubResult Preload_MichaelInFightingClub(void)
{
	return preload_pupil(EVENT_PUPIL_MICHAEL_STATE);
}
/* <<< factory Preload_MichaelInFightingClub */

/* >>> factory Preload_JessicaInFightingClub */
PreloadPupilInFightingClubResult Preload_JessicaInFightingClub(void)
{
	return preload_pupil(EVENT_PUPIL_JESSICA_STATE);
}
/* <<< factory Preload_JessicaInFightingClub */
