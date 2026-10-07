/* >>> part includes */
#include "home/lightning_club.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> factory statics */
#include "home/lightning_club.h"
#include "home/grass_club_entrance.h"
#include "home/scripting.h"
#include "generated/wram.h"
#define LightningClubAfterDuelTable (LightningClubAfterDuel__after_duel_table_ADDR)
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
/* <<< factory Preload_Isaac */
