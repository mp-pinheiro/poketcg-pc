#include "home/lightning_club.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/lightning_club.h"
#include "home/grass_club_entrance.h"
#include "home/scripting.h"
#include "generated/wram.h"
#define LightningClubAfterDuelTable 0x63efu
#define EVENT_BEAT_JENNIFER 0x25u
#define EVENT_BEAT_NICHOLAS 0x26u
#define EVENT_BEAT_BRANDON 0x27u
#define SOUTH 0x02u
/* <<< factory statics */

/* >>> factory LightningClubAfterDuel */
LightningClubAfterDuelResult LightningClubAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(LightningClubAfterDuelTable);
	return (LightningClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory LightningClubAfterDuel */

/* >>> factory Preload_Isaac */
PreloadIsaacResult Preload_Isaac(void)
{
	uint8_t a = GetEventValue(EVENT_BEAT_JENNIFER);
	if (a == 0u)
		return (PreloadIsaacResult){a, 0x90u};
	a = GetEventValue(EVENT_BEAT_NICHOLAS);
	if (a == 0u)
		return (PreloadIsaacResult){a, 0x90u};
	a = GetEventValue(EVENT_BEAT_BRANDON);
	if (a == 0u)
		return (PreloadIsaacResult){a, 0x90u};
	a = SOUTH;
	wLoadNPCDirection = a;
	return (PreloadIsaacResult){a, 0x10u};
}
