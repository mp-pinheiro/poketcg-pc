#include "home/science_club.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/scripting.h"
#include "generated/wram.h"
#define EVENT_BEAT_JOSEPH 0x1Bu
#define WEST 0x03u

#include "home/grass_club_entrance.h"
#define ScienceClubAfterDuelTable 0x6bf8u
/* <<< factory statics */

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
