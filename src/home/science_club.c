/* >>> part includes */
#include "home/science_club.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "home/scripting.h"
#include "generated/wram.h"

#include "home/grass_club_entrance.h"
/* <<< part includes_2 */
/* >>> part ScienceClubAfterDuelTable */
#define ScienceClubAfterDuelTable (ScienceClubAfterDuel__after_duel_table_ADDR)
/* <<< part ScienceClubAfterDuelTable */

/* >>> factory Preload_Joseph */
PreloadJosephResult Preload_Joseph(void)
{
	uint8_t event = GetEventValue(EVENT_BEAT_JOSEPH);
	if (event != 0u) {
		uint8_t x = wLoadNPCXPos;
		uint8_t new_x = (uint8_t)(x + 2u);
		uint8_t z = (new_x == 0u) ? 0x80u : 0x00u;
		wLoadNPCXPos = new_x;
		wLoadNPCDirection = WEST;
		return (PreloadJosephResult){WEST, (uint8_t)(z | 0x10u)};
	}
	return (PreloadJosephResult){event, 0x90u};
}
/* <<< factory Preload_Joseph */

/* >>> factory ScienceClubAfterDuel */
ScienceClubAfterDuelResult ScienceClubAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(ScienceClubAfterDuelTable);
	return (ScienceClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory ScienceClubAfterDuel */
